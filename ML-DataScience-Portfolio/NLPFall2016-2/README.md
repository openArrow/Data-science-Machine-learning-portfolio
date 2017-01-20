# NLPFall2016 (This is the Phase 1 Code)
This branch contains the implementation fo First Approach .
check_ambiguity.py takes the POS tagged sentences from the corpus and returns unambigous lines.

The output from check_ambiguity.py is sent to stanford dependency parser to get dependency parse of all ambigous sentnces.
knowlege_extract.py takes input the file containing the dependency parsed input and produces common sennse knowledge.
