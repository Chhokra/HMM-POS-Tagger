import pickle 
file = open('training_set.txt')
contents = file.readlines()
contents = [i.split() for i in contents]
yo = []
for i in contents:
	if (i!=[]):
		yo.append(i)
appended_yo = []
appended_yo.append(['<START>','START'])
length = 0
for i in yo:
	if(i==['.','.']):
		appended_yo.append(['<END>','END'])
		appended_yo.append(['<START>','START'])
	else:
		appended_yo.append(i)
appended_yo.pop()
sentences = []
sentence = []
for i in appended_yo:
	sentence.append(i)
	if(i==['<END>','END']):
		sentences.append(sentence)
		sentence = []
pos_uni = {}
for i in sentences:
	for j in i:
			if(j[1] not in pos_uni):
				pos_uni[j[1]] = 1
			else:
				pos_uni[j[1]] +=1
pos_bi = {}
for i in range(len(sentences)):
	for j in range(len(sentences[i])-1):
		if(sentences[i][j][1] not in pos_bi):
			pos_bi[sentences[i][j][1]] = {}
			pos_bi[sentences[i][j][1]][sentences[i][j+1][1]] = 1
		else:
			if(sentences[i][j+1][1] not in pos_bi[sentences[i][j][1]]):
				pos_bi[sentences[i][j][1]][sentences[i][j+1][1]] = 1
			else:
				pos_bi[sentences[i][j][1]][sentences[i][j+1][1]] += 1
dictionary = {}
for i in appended_yo:
	if(i!=['<END>','END'] and i!=['<START>','START']):
		if(i[0] not in dictionary):
			dictionary[i[0]]=1
		else:
			dictionary[i[0]]+=1

for i in appended_yo:
	if(i!=['<END>','END'] and i!=['<START>','START']):
		if(dictionary[i[0]]<=2):
			i[0] = '<unk>'

sentences1 = []
sentence1 = []
for i in appended_yo:
	sentence1.append(i)
	if(i==['<END>','END']):
		sentences1.append(sentence1)
		sentence1 = []
last = {}

for i in range(len(sentences1)):
	for j in range(len(sentences1[i])):
		if(sentences1[i][j][1] not in last):
			last[sentences1[i][j][1]] = {}
			last[sentences1[i][j][1]][sentences1[i][j][0]] = 1
		else:
			if(sentences1[i][j][0] not in last[sentences1[i][j][1]]):
				last[sentences1[i][j][1]][sentences1[i][j][0]] = 1
			else:
				last[sentences1[i][j][1]][sentences1[i][j][0]]+=1
updated_dictionary = {}
for i in appended_yo:
	if(i!=['<END>','END'] and i!=['<START>','START']):
		if(i[0] not in updated_dictionary):
			updated_dictionary[i[0]]=1
		else:
			updated_dictionary[i[0]]+=1

file = open('pos_uni.pkl','wb')
pickle.dump(pos_uni,file)
file1 = open('pos_bi.pkl','wb')
pickle.dump(pos_bi,file1)
file2 = open('last.pkl','wb')
pickle.dump(last,file2)
file3 = open('dictionary.pkl','wb')
pickle.dump(updated_dictionary,file3)