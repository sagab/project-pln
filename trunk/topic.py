import xmlReader
from general import *
from nltk.corpus import wordnet as wn
import stemmer
import re
from tagger import Tagger


class Topics:

	egrams=[]
	
	# obtin lista de bigrame dandu-se un dictionar sortat de bigrame in fct de frecventa
	def topicBigrams(self,bfreq_dict):
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


	#detectare trigrame ca topic
	def topicTrigrams(self,tfreq_dict):
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



	#detectare unigrame ca topic
	def topicUnigrams(self,freq_dict):

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
	def getUnigramTopList(self,fd,max_entries=5):
		rez = []	
		for i in range(0,min(len(fd),max_entries)):
			t = []
			t.append(fd[i][0][1])
			t.append(fd[i][0][0])
			rez.append(t+fd[i][1])
		return rez
		
	# similar pt multigrame
	def getMultigramTopList(self,fd,max_entries=5):
		rez = []	
		for i in range(0,min(len(fd),max_entries)):
			t = []
			t.append(fd[i][1])
			t.append(fd[i][0])
			rez.append(t)
		return rez
		
	# fct experimentala (manual)
	def experiment(self,text,cueword):
		tagger = Tagger()
		lst = tagger.tag(re.split(r"[\s\.,\'\?]+",text));

		i=0
		while i<len(lst)-1:

			if (len(lst[i][0])<3 or len(lst[i+1][0])<3):
				i+=1;
				continue;
			if (lst[i][0]==cueword or lst[i+1][0]==cueword):
				i+=1;
				continue;

			if (lst[i][1].find('NN')!=-1 and lst[i+1][1].find('NN')!=-1):
				self.egrams.append(str(lst[i])+" "+str(lst[i+1]))
			if (lst[i][1].find('RB')!=-1 and lst[i+1][1].find('NN')!=-1):
				self.egrams.append(str(lst[i])+" "+str(lst[i+1]))
			i+=1


		i=0
		while i<len(lst)-2:
		#print lst[i][1]
		
			if (len(lst[i][0])<3 or len(lst[i+1][0])<3 or len(lst[i+2][0])<3):
				i+=1;
				continue;
			if (lst[i][0]==cueword or lst[i+1][0]==cueword or lst[i+2][0]==cueword):
				i+=1;
				continue;

			if (lst[i][1].find('NN')!=-1 and lst[i+1][1].find('NN')!=-1 and lst[i+2][1].find('NN')!=-1):
				self.egrams.append(str(lst[i])+" "+str(lst[i+1])+" "+str(lst[i+2]))
			if (lst[i][1].find('RB')!=-1 and lst[i+1][1].find('NN')!=-1 and lst[i+2][1].find('NN')!=-1):
				self.egrams.append(str(lst[i])+" "+str(lst[i+1])+" "+str(lst[i+2]))
			if (lst[i][1].find('NN')!=-1 and lst[i+1][1].find('JJ')!=-1 and lst[i+2][1].find('NN')!=-1):
				self.egrams.append(str(lst[i])+" "+str(lst[i+1])+" "+str(lst[i+2]))
			i+=1
	
	
	def flatten(self, lst):
		rez = ""
		for el in lst:
			rez+=el+' '
		return rez
		
	# functia principala
	# fin fisier intrare, fout fisier iesire		
	def topics(self,fin,fout):
		#dictionare 
		freq_dict = {}
		bfreq_dict = {}
		tfreq_dict = {}


		r = xmlReader.XMLReader()
		r.read(fin)

		for msg in r.doc:

			#eliminare fraze chat standard
			if(msg.text.startswith('joins the room') or msg.text.startswith('leaves the room')):
				continue
	
			#metoda experimentala manuala
			if(msg.text.find('about')!=-1 ):		
				self.experiment(msg.text,'about');
			if(msg.text.lower().startswith('what') ):		
				self.experiment(msg.text,'what');

			updateFreqList(stripStopWords_split(msg.text),freq_dict)
			updateFreqList(getBigramList(stripStopWords_nosplit(msg.text)),bfreq_dict)
			updateFreqList(getTrigramList(stripStopWords_nosplit(msg.text)),tfreq_dict)
	

		freq_dict = sort_freq_dict(freq_dict,50)
		tfreq_dict = sort_freq_dict(tfreq_dict,15)
		bfreq_dict = sort_freq_dict(bfreq_dict,15)

		a = self.topicUnigrams(freq_dict)
		b = self.topicBigrams(bfreq_dict)
		c = self.topicTrigrams(tfreq_dict) 
		
		
		ugrams = self.getUnigramTopList(a,5)
		bgrams = self.getMultigramTopList(b,5)
		tgrams = self.getMultigramTopList(c,5)
		
		
		print '\n\nUnigrame -------------'
		print ugrams
		
		print '\n\nBigrame --------------'
		print bgrams
		
		print '\n\nTrigrame -------------'
		print tgrams
		
		

		doc = r.xmldoc
		de = doc.documentElement
		# verific daca exista sectiunea Topics
		if len(de.getElementsByTagName('Topics')) == 0:
			el = doc.createElement('Topics')
			de.appendChild(el)
	
		anod = de.getElementsByTagName('Topics')[0]
	
		
		if len(anod.getElementsByTagName('Unigram')) > 0:
			pnod = anod.getElementsByTagName('Unigram')[0]
			anod.removeChild(pnod)
	
		#scriu unigrame
		unod = doc.createElement('Unigram')		
		anod.appendChild(unod)		
		for ugram in ugrams:
			topicnod = doc.createElement('Topic')
			topicnod.setAttribute("freq", str(ugram[0]))
			if len(ugram)>2:
				topicnod.setAttribute("synlist",str(self.flatten(set(ugram[2:]))))
			topicnod.appendChild(doc.createTextNode(ugram[1]))
			unod.appendChild(topicnod)
		
		#scriu bigrame
		bnod = doc.createElement('Bigram')		
		anod.appendChild(bnod)		
		for bgram in bgrams:
			topicnod = doc.createElement('Topic')
			topicnod.setAttribute("freq", str(bgram[0]))
			topicnod.appendChild(doc.createTextNode(bgram[1]))
			bnod.appendChild(topicnod)
		
		#scriu trigrame
		tnod = doc.createElement('Trigram')		
		anod.appendChild(tnod)		
		for tgram in tgrams:
			topicnod = doc.createElement('Topic')
			topicnod.appendChild(doc.createTextNode(tgram[1]))
			tnod.appendChild(topicnod)
			
		#scriu experimental
		enod = doc.createElement('Exp')		
		anod.appendChild(enod)		
		for egram in self.egrams:
			topicnod = doc.createElement('Topic')
			topicnod.appendChild(doc.createTextNode(egram))
			enod.appendChild(topicnod)
			
		# write modified xml DOM tree in fisier
		ofile = open(fout, 'w')
		r.xmldoc.writexml(ofile)
		ofile.close()
		r.close()
		

t = Topics()
t.topics('xml/4.xml','xml/4t.xml')






