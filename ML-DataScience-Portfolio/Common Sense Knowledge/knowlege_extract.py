import sys
import re
inputFile = 'output.txt'
outputFile = 'extractorOut.txt'

aux_verbs = ['am', 'is', 'are' ,'was' ,'were', 'being', 'been', 'does', 'do', 'did' , 'has', 'have', 'had' , 'having' , 'can', 'could', 'may', 'might', 'must', 'ought to', 'shall', 'should', 'will', 'would']
connectors = ['therefore', 'as a consequence', 'for this reason', 'for all these reasons', 'thus', 'because', 'because of', 'since', 'on account of', 'due to', 'for the reason', 'so, that', 'so that', 'when']

file = open(sys.argv[1],"r")
fileOut =open(outputFile,"w")
parse_list = []
temp_list = []

def getWord(dep_tuple):
    return dep_tuple.split('(')[1].split(',')[1].split(')')[0]

def breakConn(list):
    str = ''
    for i,v in enumerate(list):
        word_with_no = getWord(v)
        word = getWord(v).split('-')[0]

        if i==0:
            str += word
        else:
            prev_word_with_no = getWord(list[i-1])
            if(word_with_no != prev_word_with_no):
                str += word

    str = str.strip()

    conn = ''
    for i in connectors:
        if re.search(i, str):
            conn = i
            break
    
    low = 0
    up = 0

    conn_arr = conn.split(' ')
    str_arr = str.split(' ')
    #print conn_arr
    #print str_arr
    for i,v in enumerate(str_arr):
        count = 0
        for j,w in enumerate(conn_arr):
            if w == str_arr[i+j]:
                count+=1
        if count == len(conn_arr):
            low = 1 + (i)
            up = 1 + (i + len(conn_arr) - 1)
            break

    d = {'front':[], 'end':[]}
    # print low , up
    # print list
    # print len(list)

    for i,v in enumerate(list):
        # print i
        word_with_no = getWord(v)
        # print v, '------', word_with_no, '------', int(word_with_no.split('-')[1])
        if int(word_with_no.split('-')[1]) < low:
            d['front'].append(v)
        if int(word_with_no.split('-')[1]) > up:
            d['end'].append(v)

    return d


def createKnowledge(item):
	print "here"
	reg_1F = re.compile('^nsubj.*')
	reg_2F = re.compile('^(dobj|case|iobj).*')
	reg_3F = re.compile('^neg.*')
	reg_1E = re.compile('^nsubj.*')
	reg_2E = re.compile('^(advcl|admod).*')
	reg_3E = re.compile('^(dobj|iobj|case).*')
    
	res1F = filter(reg_1F.match,item['front'])
	res2F = filter(reg_2F.match,item['front'])
	res3F = filter(reg_3F.match,item['front'])
	res1E = filter(reg_1E.match,item['end'])
	res2E = filter(reg_2E.match,item['end'])
	res3E= filter(reg_3E.match,item['end'])
    
	if(len(res1F)==0 or len(res2F)==0 or len(res1E)==0 or (len(res2E)==0 and len(res3E)==0) ):	
		print 'Missing dep,Knowledge not created!!'
		return
	nsubj_1F_verb = res1F[0].split(',')[0].split('(')[1].split('-')[0]
	nsubj_1F_agent = res1F[0].split(',')[1].split('-')[0]

	if len(res2F) == 0:
		print 'dobj does not exist!!'
		return
	dobj_2F_tag = res2F[0].split('(');
	if(dobj_2F_tag[0] == 'case'):
		dobj_2F_object = res2F[0].split(',')[0].split('(')[1].split('-')[0]
		dobj_2F_verb = res2F[0].split(',')[1].split('-')[0]
	else:
		dobj_2F_verb = res2F[0].split(',')[0].split('(')[1].split('-')[0]
		dobj_2F_object = res2F[0].split(',')[1].split('-')[0]
	
			   
	nsubj_1E_verb = res1E[0].split(',')[0].split('(')[1].split('-')[0]
	nsubj_1E_agent = res1E[0].split(',')[1].split('-')[0]
	
	advcl_2E_verb = res2E[0].split(',')[0].split('(')[1].split('-')[0]
	advcl_2E_prop = res2E[0].split(',')[1].split('-')[0]
	prop = "NULL"
	if len(res3E) != 0:
		dobj_3E_verb = res3E[0].split(',')[0].split('(')[1].split('-')[0]
		dobj_3E_object = res3E[0].split(',')[1].split('-')[0]
	    	if(nsubj_1E_verb == dobj_3E_verb):
			prop =  dobj_3E_object
	else:
		prop = advcl_2E_prop    
	
	if prop == "NULL":
		print "object not found for action"
		return
	agent = nsubj_1F_agent
	object = dobj_2F_object
	action = nsubj_1F_verb
	propActor = nsubj_1E_agent

	if(nsubj_1F_verb == advcl_2E_verb):
		if len(res3F) != 0:
			str = propActor+"."+prop+" = false may cause execution of "+action+" ["+agent+","+object+"]"
	       	else:
			str = propActor+"."+prop+" = true may cause execution of "+action+" ["+agent+","+object+"]"
	   	print str
		fileOut.write(str+'\n')
	else:
	        print 'knowledge not created!!'

for line in file:
    if line == "\n":
        #print breakConn(temp_list)
        #print '\n\n\n'
        parse_list.append(breakConn(temp_list))
        temp_list = []
    else:
        line = line.replace("\n","")
        temp_list.append(line)


#print parse_list
for item in parse_list:
	createKnowledge(item)
