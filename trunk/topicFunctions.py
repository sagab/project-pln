import xmlReader
from general import *
from nltk.corpus import wordnet as wn
import stemmer
import sys

# obtin lista de bigrame dandu-se un dictionar sortat de bigrame in fct de frecventa
def topicBigrams(bfreq_dict):
	stemmer = Stemmer()

	# unificare bigrame prin stem
	temp_list = []
	len_bfreq_dict = len(bfreq_dict)
	i=j=0
	while i < len_bfreq_dict:
		w1 = bfreq_dict[i]
		stemmed_w1a = stemmer.stem(w1[0].split()[0])
		stemmed_w1b = stemmer.stem(w1[0].split()[1])
		freq_w1 = w1[1]

		print 'Verific stem pentru',bfreq_dict[i][0]
		j=i+1
		while j < len_bfreq_dict:
			#print j,'!'	
			w2 = bfreq_dict[j]
			stemmed_w2a = stemmer.stem(w2[0].split()[0])
			stemmed_w2b = stemmer.stem(w2[0].split()[1])

			if(stemmed_w1a == stemmed_w2a and stemmed_w1b == stemmed_w2b):
				print 'Unific [',w1[0],'] cu [',w2[0],']'
				freq_w1+=w2[1] # cresc frecventa
				len_bfreq_dict-=1
				bfreq_dict.remove(w2) # scot elementul adaugat
				#i-=1
				#break
			j+=1
		#print 'adaug',w1[0],'i:',i,'j',j
		temp_list.append((w1[0],freq_w1))
		i+=1;


	#rezultat bigrame
	return temp_list



def topicTrigrams(tfreq_dict):
	stemmer = Stemmer()
	
	# unificare trigrame prin stem
	temp_list = []
	len_tfreq_dict = len(tfreq_dict)
	i=j=0
	while i < len_tfreq_dict:
		w1 = tfreq_dict[i]
		stemmed_w1a = stemmer.stem(w1[0].split()[0])
		stemmed_w1b = stemmer.stem(w1[0].split()[1])
		stemmed_w1c = stemmer.stem(w1[0].split()[2])
		freq_w1 = w1[1]
	
		print 'Verific stem pentru',tfreq_dict[i][0]
		j=i+1
		while j < len_tfreq_dict:
			#print j,'!'	
			w2 = tfreq_dict[j]
			stemmed_w2a = stemmer.stem(w2[0].split()[0])
			stemmed_w2b = stemmer.stem(w2[0].split()[1])
			stemmed_w2c = stemmer.stem(w2[0].split()[2])
	
			if(stemmed_w1a == stemmed_w2a and stemmed_w1b == stemmed_w2b and stemmed_w1c == stemmed_w2c):
				print 'Unific [',w1[0],'] cu [',w2[0],']'
				freq_w1+=w2[1] # cresc frecventa
				len_tfreq_dict-=1
				tfreq_dict.remove(w2) # scot elementul adaugat
				#i-=1
				#break
			j+=1
		#print 'adaug',w1[0],'i:',i,'j',j
		temp_list.append((w1[0],freq_w1))
		i+=1;
	
	#rezultat trigrame
	return temp_list




def topicUnigrams(freq_dict):

	stemmer = Stemmer()

	# unificare cuvinte similare dpdv al stem-ului
	temp_list = []
	len_freq_dict = len(freq_dict)
	i=j=0
	while i < len_freq_dict:
		w1 = freq_dict[i]
		stemmed_w1 = stemmer.stem(w1[0])
		freq_w1 = w1[1]

		print 'Verific stem pentru',w1[0]
		j=i+1
		while j < len_freq_dict:
			#print j,'!'	
			w2 = freq_dict[j]
			stemmed_w2 = stemmer.stem(w2[0])
	
			if(stemmed_w1==stemmed_w2):
				print 'Unific [',w1[0],'] cu [',w2[0],']'
				freq_w1+=w2[1] # cresc frecventa
				len_freq_dict-=1
				freq_dict.remove(w2) # scot elementul adaugat
				#i-=1
				#break
			j+=1
		#print 'adaug',w1[0],'i:',i,'j',j
		temp_list.append((w1[0],freq_w1))
		i+=1;
	
	
	
	
	# creare lista sinonime
	freq_dict = []
	for tw in temp_list:
		syn_list = []
		for synset in wn.synsets(tw[0]):
			if(synset.lemmas[0].name.lower() not in syn_list):
				syn_list.append(synset.lemmas[0].name.lower())
		
		freq_dict.append((tw,syn_list))
	
	freq_dict.append((('test_bayes',1),['bayes','naive']))
	#for fw in freq_dict:
	#	print fw[0], fw[1]
	
	
	
	# iterare lista sinonime si unificare
	temp_list = []
	len_freq_dict = len(freq_dict)
	i=j=0
	while i < len_freq_dict:
		w1 = freq_dict[i][0]
		w1_syn_list = freq_dict[i][1]
		freq_w1 = w1[1]
	
		print 'Verific sinonime pentru',w1[0]
		j=i+1
		while j < len_freq_dict:
			if(i==j):
				j+=1			
				continue		
			#print j,'!'	
			w2 = freq_dict[j][0]
			w2_syn_list =  freq_dict[j][1]
	
			if( w2[0] in w1_syn_list or w1[0] in w2_syn_list):
				print 'Unific [',w1[0],'] cu [',w2[0],']'
				freq_w1+=w2[1] # cresc frecventa
				len_freq_dict-=1
				freq_dict.remove((w2,w2_syn_list)) # scot elementul adaugat
				w1_syn_list += w2_syn_list
				j=-1
				
			j+=1
	
		temp_list.append(((w1[0],freq_w1),w1_syn_list))
		i+=1;
		
	return temp_list

# primeste ca parametru o lista de forma [(word,word_freq),[sinonim1,sin2,..]]
# returneaza primele max intrari sub forma [freq_word,word,sinonim1,sin2..]
def getUnigramTopList(fd,max_entries=5):
	rez = []	
	for i in range(0,min(len(fd),max_entries)):
		t = []
		t.append(fd[i][0][1])
		t.append(fd[i][0][0])
		rez.append(t+fd[i][1])
	return rez

def getMultigramTopList(fd,max_entries=5):
	rez = []	
	for i in range(0,min(len(fd),max_entries)):
		t = []
		t.append(fd[i][1])
		t.append(fd[i][0])
		rez.append(t)
	return rez
