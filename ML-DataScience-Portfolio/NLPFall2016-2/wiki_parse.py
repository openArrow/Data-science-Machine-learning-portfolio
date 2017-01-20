import re
import check_ambiguity as ca
from nltk.tag.stanford import StanfordPOSTagger

aux_verbs = ['am', 'is', 'are' ,'was' ,'were', 'being', 'been', 'does', 'do', 'did' , 'has', 'have', 'had' , 'having' , 'can', 'could', 'may', 'might', 'must', 'ought to', 'shall', 'should', 'will', 'would']
connectors = ['therefore', 'as a consequence', 'for this reason', 'for all these reasons', 'thus', 'because', 'because of', 'since', 'on account of', 'due to', 'for the reason', 'so, that', 'so that']

def getTags(sen_arr):
	tag_arr = []
	st = StanfordPOSTagger(' '.join(sen_arr).srtip())
	for i in st:
		tag = i[1].encode("utf-8")
		tag_arr.append(tag)

	return tag_arr

def isValid(sen1_arr, sen1_tags, sen2_arr, sen2_tags):
	sen1_arr_t = []
	sen1_tags_t = [] 
	sen2_arr_t = [] 
	sen2_tags_t = []

	# print '------------------------'
	# print len(sen1_arr) , sen1_arr
	# print len(sen1_tags), sen1_tags
	# print len(sen2_arr) , sen2_arr
	# print len(sen2_tags), sen2_tags
	# print '------------------------'
	
	for i,v in enumerate(sen1_arr):
		if v in aux_verbs :
			continue
		sen1_arr_t.append(v)
		sen1_tags_t.append(sen1_tags[i]) 

	for i,v in enumerate(sen2_arr):
		if v in aux_verbs :
			continue
		sen2_arr_t.append(v)
		sen2_tags_t.append(sen2_tags[i])

	sen1_tags_t = ' '.join(sen1_tags_t).strip()
	sen2_tags_t = ' '.join(sen2_tags_t).strip()

	# search1 = re.search('^[^(VB)]*(VB)[^(VB)]*$',sen1_tags_t)
	# search2 = re.search('^[^(JJ)]*(JJ)[^(JJ)]*$',sen2_tags_t)
	# search3 = re.search('^[^(VB)]*(VB)[^(VB)]*$',sen2_tags_t)
	# if search1 and (search2 or search3):
	# 	return True
	
	sen1_tags_t = getTags(sen1_arr_t)
	sen2_tags_t = getTags(sen2_arr_t) 
	
	result = ca.checkIfUnambigous(sen1_arr_t, sen1_tags_t, sen2_arr_t, sen2_tags_t)
	
	if result:
		# print '00000 : ' , sen1_tags_t
		return True

	return False

def formSen(sen_arr, sen_tags):
	sen = ""
	for i,v in enumerate(sen_arr):
		sen += " " + v
	return sen

def printCheck(sentence, sen_arr, sen_tags):
	for i in connectors:
		if str(' '+ i +' ') in sentence:
			# print i, ' :- ' , sentence.split(' ')[0].strip()
			if sentence.strip().split(' ')[0].strip() == i.strip() or sentence.strip().split(' ')[-1].strip() == i.strip() :
				continue

			sen1 = sentence.split(' '+ i +' ')[0]
			sen1_arr  = sen1.strip().split(' ')
			sen1_tags = sen_tags[0:len(sen1_arr)]

			len_conn = len(i.split(' '))

			sen2 = sentence.split(' '+ i +' ')[1]
			sen2_arr  = sen2.strip().split(' ')
			sen2_tags = sen_tags[len(sen1_tags) + len_conn :len(sen_arr)]

			if isValid(sen1_arr, sen1_tags, sen2_arr, sen2_tags) == False:
				continue

			# print "------------------------------------------------"
			# print "------------------------------------------------"
			# print i 
			# print '\n'
			# print sentence
			# print sen_tags
			# print sen_arr
			# print '\n'
			# print '1 --> ' , sen1
			# print '      ' , sen1_tags
			# print '      ' , sen1_arr
			# print '\n'
			# print '2 --> ' , sen2
			# print '      ' , sen2_tags
			# print '      ' , sen2_arr
			# print "------------------------------------------------"
			# print "------------------------------------------------"

			return True

count = 0 
file = 'englishEtiquetado_0_10000'

output = open("wiki_sentences.txt", "a")

with open(file) as f :
	sen = []
	sen_tags = []
	for line in f :
		if line[0] == '<':
			continue
		if line == '\n':
			count +=1
			#print '\n'
			#print sen
			#print sen_tags
			sentence = formSen(sen, sen_tags)
			if printCheck(sentence, sen, sen_tags):
				sentence = sentence.replace(',','').replace('-', '').replace('"', '').replace(':', '')
				print sentence
				output.write(sentence)
			sen = []
			sen_tags = []

		else:
			try:
				sen.append(line.split(' ')[0])
				sen_tags.append(line.split(' ')[-2])
			except Exception as e:
				sen = []
				sen_tags = []
				