import pickle
file = open('pos_uni.pkl','rb')
file1 = open('pos_bi.pkl','rb')
file2 = open('last.pkl','rb')
file3 = open('dictionary.pkl','rb')
pos_uni = pickle.load(file)
pos_bi = pickle.load(file1)
last = pickle.load(file2)
dictionary = pickle.load(file3)
POS_Tags = []
file4 = open('input.txt','rb')
contents = file4.readlines()
contents = [i.split() for i in contents]
sentences = []
sentence = []
whatever = []
file5 = open('output.txt','wb')
for i in contents:
	if(i!=[]):
		whatever.append(i)
for i in range(len(whatever)):
	if whatever[i] ==['.']:
		sentences.append(sentence)
		sentence = []
	else:
		sentence.append(whatever[i][0])
for z in sentences:
	words = z 
	viterbi = [[0 for i in range(len(words))]for j in range(35)]
	for i in range(len(words)):
		if(words[i] not in dictionary):
			words[i] = '<UNK>'

	for i in pos_uni:
		if(i!='END' and i!='START'):
			POS_Tags.append(i)

	backtrace = [[0 for i in range(len(words))]for j in range(35)]
	for i in range(35):
		backtrace[i][0] = 0
		priori = 0
		likelihood = 0
		if(POS_Tags[i] in pos_bi['START']):
			priori = float(pos_bi['START'][POS_Tags[i]]+1)/float(pos_uni['START']+35)
		else:
			priori = float(1)/float(pos_uni['START']+35)
		if(words[0] in last[POS_Tags[i]]):
			likelihood = float(last[POS_Tags[i]][words[0]]+1)/float(pos_uni[POS_Tags[i]]+35)
		else:
			likelihood = float(1)/float(pos_uni[POS_Tags[i]]+35)
		viterbi[i][0] = priori*likelihood


	for t in range(1,len(words)):
		for s in range(35):
			likelihood = 0
			if(words[t] in last[POS_Tags[s]]):
				likelihood = float(last[POS_Tags[s]][words[t]]+1)/float(pos_uni[POS_Tags[s]]+35)
			else:
				likelihood = float(1)/float(pos_uni[POS_Tags[s]]+35)
			element = 0
			maximum = -1
			for sdash in range(35):
				one = viterbi[sdash][t-1]
				two = 0
				if(POS_Tags[s] in pos_bi[POS_Tags[sdash]]):
					two = float(pos_bi[POS_Tags[sdash]][POS_Tags[s]]+1)/float(pos_uni[POS_Tags[sdash]]+35)
				else:
					two = float(1)/float(pos_uni[POS_Tags[sdash]]+35)
				prod = one*two
				if(prod>maximum):
					maximum = prod 
					element = sdash
			viterbi[s][t] = maximum*likelihood
			backtrace[s][t] = element 
	outer_max = -1
	outer_element = 0
	for s in range(35):
		prev = 0
		end = 0
		prev = viterbi[s][len(words)-1]
		if('END' in pos_bi[POS_Tags[s]]):
			end = float(pos_bi[POS_Tags[s]]['END']+1)/float(35+pos_uni[POS_Tags[s]])
		else:
			end = float(1)/(pos_uni[POS_Tags[j]]+35)
		prod = prev*end 
		if(prod>outer_max):
			outer_element = s
			outer_max = prod 
	counter = len(words)
	current = outer_element
	answer = []
	answer.append(current)
	while(counter>1):
		current = backtrace[current][counter-1]
		answer.append(current)
		counter-=1

	reversed_POS_Tags = []
	for i in range(len(answer)-1,-1,-1):
		reversed_POS_Tags.append(POS_Tags[answer[i]])
	for i in range(len(words)):
		file5.write(words[i]+"\t"+reversed_POS_Tags[i]+"\n")
	file5.write("."+"\t"+".\n")
	file5.write("\n")




