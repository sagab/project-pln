"""
PLN Toolkit Project

Clasa CorefRes este o implementare a algoritmului
de gasire a coreferintelor dintr-un text prin metoda
clusterizarii Cardie Wagstaff.

"""

from tagger import Tagger
from nltk.corpus import wordnet as wn
from xmlReader import XMLReader
import nltk
import nltk.tag
import math

# o clasa pentru stocarea atributelor fiecarui NP impreuna cu textul propriu zis
class NP:
	
	# primeste ca parametri un NP ca lista tagged tuples si contextul in care apare
	# (ca sa pot calcula pozitia si sa vad daca e intre virgule -> appositive).
	def __init__(self, tagtext, context, pos):
		self.tags = tagtext
		self.context = context
		
		# un dictionar ca sa regasesc rapid un feature
		self.features = {'words':0, 'headnoun':1,'position':2,
			'pronoun':3,'article':4, 'wordsub':5,'appositive':6,'number':7,
			'proper':8, 'semclass':9, 'gender':10,'animacy':11}
		
		# default values for each feature
		self.values = [0, '', pos, 'AMB', 'NONE', 0, 0, 1, 0, 'object', 'N', 0]
		
		# folosesc pointeri la functiile de calcul a incompatibilitatii
		# pe fiecare feature
		self.functions = [self.f1, self.f2, self.f3, self.f4, 
			self.f5, self.f6, self.f7, self.f8, 
			self.f9, self.f10, self.f11, self.f12]
		
		# reprezentarea -inf, +inf
		self.min = -600.0
		self.max = 600.0
		
		# o raza default pentru calculul distantei
		self.r = 2.0
		
		# weight pt fiecare feature
		self.weights = [10.0, 1.0, 5.0, self.r, self.r, self.min, self.min, self.max, self.max, 
			self.max, self.max, self.max ]
		
		# clasele de sensuri
		self.sclasses = ['time', 'city', 'animal', 'human', 'object']
		self.synsets = []

		for s in self.sclasses:
			self.synsets.append(wn.synsets(s)[0])
			
	
	# seteaza o noua raza pentru calculul distantei
	def setRadius (self, rad):
		self.r = rad
		self.weights[3:4] = rad
		
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 1: words
	def f1 (self, otherNP):
		l1 = len(self.tags)
		l2 = len(otherNP.tags)
		
		# aflu care are cele mai multe cuvinte
		maxnr = l1
		if l2 > maxnr:
			maxnr = l2
			
		# nr de cuvinte care sunt diferite,
		# pronumele se iau ca wildcards
		mismatches = 0.0 + maxnr
		
		# o lista cu toate cuvintele din celalalt NP
		t = []
		for w in otherNP.tags:
			t.append(w[0])
		
		# verific cate cuvinte din acest NP se regasesc in celalalt
		for w in self.tags:
			if w[1][0:2] != 'PP' and w[0] in t:
				mismatches -= 1
		
		return mismatches / maxnr
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 2: daca headnoun e acelasi sau nu
	def f2 (self, otherNP):
		v1 = self.values[self.features['headnoun']]
		v2 = otherNP.values[self.features['headnoun']]
		
		if  v1 != v2:
			return 1
		else:
			return 0
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 3: pozitia relativa
	def f3 (self, otherNP):
		p1 = self.values[self.features['position']]
		p2 = otherNP.values[self.features['position']]
		
		nr = len(self.context['tagged'])
		
		return math.fabs(p1 - p2) / nr
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 4: tipul de pronume
	def f4 (self, otherNP):
		p1 = self.values[self.features['pronoun']]
		p2 = otherNP.values[self.features['pronoun']]
		
		if p1 != 'NONE' and p2 == 'NONE':
			return 1
		else:
			return 0
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 5: article
	def f5 (self, otherNP):
		a2 = otherNP.values[self.features['article']]
		appo2 = otherNP.values[self.features['appositive']]
		
		if a2 == 'INDEF' and appo2 == 0:
			return 1
		else:
			return 0
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 6: word substring
	def f6 (self, otherNP):
		
		# o lista cu toate cuvintele din acest NP
		list1 = []
		for w in self.tags:
			list1.append(w[0])

		# o lista cu toate cuv din otherNP
		list2 = []
		for w in otherNP.tags:
			list2.append(w[0])
		
		# verifica daca otherNP e cuprins complet in acest NP
		for w in list2:
			if w not in list1:
				return 0
		
		return 1
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 7: appositive
	def f7 (self, otherNP):
		pos1 = self.values[self.features['position']]
		pos2 = otherNP.values[self.features['position']]
		appo2 = otherNP.values[self.features['appositive']]
		
		if pos1 == pos2 - 1 and appo2 == 1:
			return 1
		else:
			return 0
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 8: number
	def f8 (self, otherNP):
		nr1 = self.values[self.features['number']]
		nr2 = otherNP.values[self.features['number']]
		
		if nr1 != nr2:
			return 1
		else:
			return 0
		
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 9: proper name
	def f9 (self, otherNP):
		pn1 = self.values[self.features['proper']]
		pn2 = otherNP.values[self.features['proper']]
		
		# trebuie ambele sa fie proper names
		if pn1 != 1 or pn2 != 1:
			return 0
		
		# daca apare vreun match intre cele 2 nume proprii, return 0
		# o lista cu toate cuvintele din acest NP
		list1 = []
		for w in self.tags:
			list1.append(w[0])

		# o lista cu toate cuv din otherNP
		list2 = []
		for w in otherNP.tags:
			list2.append(w[0])
		
		for w in list1:
			if w in list2:
				return 0
		
		return 1
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 10: semantic class
	def f10 (self, otherNP):
		sc1 = self.values[self.features['semclass']]
		sc2 = otherNP.values[self.features['semclass']]
		
		if sc1 != sc2:
			return 1
		else:
			return 0
		
		
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 11: gender
	def f11 (self, otherNP):
		g1 = self.values[self.features['gender']]
		g2 = otherNP.values[self.features['gender']]
		
		# genul Either face match pe orice
		if g1 == 'E':
			return 0
		
		if g2 == 'E':
			return 0
		
		if g1 != g2:
			return 1
		else:
			return 0
	
	# returneaza valoarea de incompatibilitate intre acest NP si altul 
	# pentru feature-ul 12: animacy
	def f12 (self, otherNP):
		a1 = self.values[self.features['animacy']]
		a2 = otherNP.values[self.features['animacy']]
		
		if a1 != a2:
			return 1
		else:
			return 0
	
		
	# returneaza distanta intre acest NP si alt NP
	def dist (self, otherNP):
		d = 0
		for i in range(len(self.weights)):
			inc = self.functions[i](otherNP)
			
			val = inc * self.weights[i]
			
			# cap la + inf
			if val > self.max:
				val = self.max
			
			# cap la -inf
			if val < self.min:
				val = self.min
			
			# daca gasesc +inf, nu mai conteaza restul
			if val == self.max:
				return self.max
			
			if val == self.min:
				d = self.min
			
			# daca d e deja self.min nu conteaza ca mai adaug o cantitate fixa
			# daca d e deja self.min, adaugand self.min ramane la aceeasi val
			if d != self.min:
				d += val
				
		return d
	
	# analizeaza tags si contextul si face un update la cateva valori pentru features
	def updateValues (self):
		l = len(self.tags)
		
		# find the head noun
		self.values[self.features['headnoun']] = self.tags[l-1][0]
		
		for i in range(l):
			# ce tip de pronume e

			if self.tags[i][1]=='PPO':
				self.values[self.features['pronoun']] = 'ACC'	# acuzativ
			elif self.tags[i][1]=='PP$$' or self.tags[i][1]=='PP$':
				self.values[self.features['pronoun']] = 'POSS'	# posesiv
			elif self.tags[i][1][0:2]=='PN':
				self.values[self.features['pronoun']] = 'NOM'	# nominativ
			elif self.tags[i][0] == 'it' or self.tags[i][0] == 'you':
				self.values[self.features['pronoun']] = 'AMB'
			
			# ce tip de articol e
			if self.tags[i][0] == 'a' or self.tags[i][0]=='an':
				self.values[self.features['article']] = 'INDEF'
			elif self.tags[i][0] == 'the':
				self.values[self.features['article']] = 'DEF'
				
			# verifica daca poate fi plural
			if self.tags[i][0][-1] == 's':
				self.values[self.features['number']] = 2
		
			# verifica daca poate fi nume propriu
			if self.tags[i][1][0:2] == 'NP':
				self.values[self.features['proper']] = 1
			
			# caut semclasa noun
			if self.tags[i][1][0] == 'N':
				
				try:
					# obtin syn-ul pentru noun 
					syn = wn.synsets(self.tags[i][0])[0]
				
					# semclass
					cl = 0
					maxsim = -1
					
					# aflu maximul valorii de similitudine
					for k in range(len(self.sclasses)):
						val = wn.lch_similarity(syn, self.synsets[k])
						if val >= maxsim:
							cl = k
							maxsim = val
						
					self.values[self.features['semclass']] = self.sclasses[cl]
				except Exception:
					self.values[self.features['semclass']] = 'unk'
					
				# gender
				# se face cu wup/etc similarity intre female si male
				# dar nu functioneaza pe WordNet :|
			
				# animacy - se face pe baza clasei anterioare
				cl = self.values[self.features['semclass']]
				if cl == 'animal' or cl == 'human':
					self.values[self.features['animacy']] = 1
				else:
					self.values[self.features['animacy']] = 0
				
				
		# verifica daca e apozitiv (cuprins intre virgule, are un articol
		# si dupa ea urmeaza tot un NP
		if self.values[self.features['article']] == 0:
			self.values[self.features['appositive']] = 0


# clasa pentru rularea algoritmului de clusterizare Cardie Wagstaff
class CorefRes:
	def __init__(self):
		self.tagger = Tagger()
		self.reader = XMLReader()
		
	# extrage o lista de NP dintr-un string ce contine mai multe propozitii
	def extractNP(self, string):
		toks = nltk.word_tokenize(string)
		lista = self.tagger.tag(toks)
		
		NP = []
		listaNP = []
		
		# parcurg toata lista de cuvinte tagged si in adaug cuvinte la un NP
		# pana cand dau de ceva ce face break
		for i in range(len(lista)):
			
			# am gasit un noun sau pronume
			if lista[i][1][0] == 'N' or lista[i][1][0:2] == 'PP':
				NP.append(lista[i])
				listaNP.append(NP)
				NP = []
				
			# am dat de articol sau determinant
			elif lista[i][1] == 'AT' or lista[i][1] == 'DT':
				NP.append(lista[i])
			
			else:	# poate fi verb sau altceva
				if len(NP) > 0:
					listaNP.append(NP)
				NP = []
		
		if len(NP) > 0:
			listaNP.append(NP)
			
		return listaNP
	
	# run the algorithm on the given string with the given radius for clusters
	def clusterize (self, string, radius):
		
		# lista de tagged strings
		list = self.extractNP(string)
		
		# in caz ca am nevoie in clasa NP de context
		context = {'text':string, 'tagged':list}
		
		# aici o sa pastrez indice pentru clusterul caruia ii apartine
		# NP-ul cu indicele respectiv
		clusters = []
		
		# lista cu toate NP-urile
		NPlist = []
		
		# creez pentru fiecare NP cate o instanta
		for i in range(len(list)):
			np = NP(list[i], context, i+1)
			np.r = radius
			
			# calculez valorile pentru features
			np.updateValues()
			
			NPlist.append(np)
			clusters.append(i+1)	# la inceput, fiecare NP e in propriul cluster
		
		# iau NPlist in ordine inversa
		r = range(len(NPlist))
		r.reverse()
		
		# pentru fiecare NPj de la n la 0
		for j in r:
			
			# lista de NP ce o preced pe NP curenta
			prec = range(j)
			
			# pentru fiecare NPi precedenta
			for i in prec:
				d = NPlist[i].dist( NPlist[j])
				ci = clusters[i]
				cj = clusters[j]
				
				# verific daca trebuie sa fac reuniunea cj = ci + cj
				if d < radius and self.all_NPS_compat(ci, cj, NPlist, clusters) == 1:
					for c in range(len(clusters)):
						if clusters[c] == ci:
							clusters[c] = cj
					
		return [NPlist, clusters]
						
	# intoarce 1 daca toate NP din clasa ci sunt compatibile cu cj
	def all_NPS_compat (self, ci, cj, NPlist, clusters):
		l1 = range(len(clusters))
		
		for i in l1:
			l2 = range(i+1, len(clusters))
			for j in l2:
				if clusters[i] == ci and clusters[j] == cj:
					if NPlist[j].dist(NPlist[i]) == NPlist[j].max:
						return 0
		
		return 1


	# ia un fisier XML chat si adauga o sectiune cu coreferinte intre replicile
	# care sunt referentiate deja
	def corefXML(self, fname_in, fname_out, radius = 50.0):
		
		#read the input xml chat
		self.reader.read(fname_in)
		
		doc = self.reader.xmldoc
		de = doc.documentElement
		
		# verific daca exista sectiunea Analysis
		if len(de.getElementsByTagName('Analysis')) == 0:
			el = doc.createElement('Analysis')
			de.appendChild(el)
		
		anod = de.getElementsByTagName('Analysis')[0]
		
		# verific daca exista sectiunea Coref. daca da, o sterg.
		# pentru a reface tot Coref
		if len(anod.getElementsByTagName('Coref')) > 0:
			cnod = anod.getElementsByTagName('Coref')[0]
			anod.removeChild(cnod)
		
		cnod = doc.createElement('Coref')
		anod.appendChild(doc.createTextNode('\n'))
		anod.appendChild(cnod)
		anod.appendChild(doc.createTextNode('\n'))
		
		# procesare
		# se iau toate utterances la rand, daca descopar una care are o referinta,
		# se proceseaza impreuna cu clusterize() altfel trec peste replici
		for i in range(len(self.reader.doc)):
			u = self.reader.doc[i]
			if u.refid != -1:
				
				# cauta replica la care este legata
				j = i
				while j >= 0 and self.reader.doc[j].id != u.refid:
					j = j - 1
				
				# verific daca a fost gasita referinta
				if j > 0:
					print 'clusterizing utterance ',self.reader.doc[j].id,' + ',self.reader.doc[i].id
					
					# concatenez replicile
					s = self.reader.doc[j].text + ' ' + self.reader.doc[i].text
					
					# aplic clusterizarea
					result = self.clusterize(s, radius)
					
					# creez un nou element in xml output
					el = doc.createElement('CorefUt')
					cnod.appendChild(doc.createTextNode('\n\t'))
					cnod.appendChild(el)
					
					# pun ca atribute replicile pe care s-a rulat algoritmul
					ut = doc.createElement('RefUt1')
					el.appendChild(doc.createTextNode('\n\t\t'))
					el.appendChild(ut)
					ut.appendChild(doc.createTextNode(str(i)))
					
					ut = doc.createElement('RefUt2')
					el.appendChild(doc.createTextNode('\n\t\t'))
					el.appendChild(ut)
					ut.appendChild(doc.createTextNode(str(j)))
					
					# pun lista de NP gasita
					l = range(len(result[0]))
					for npi in l:
						nel = doc.createElement('NP')
						el.appendChild(nel)
						
						nel.setAttribute('id',str(npi+1))
						
						# aici pun intr-un string continutul NP-ului
						npstring = ''
						
						# parcurg continutul NP-ului npi din result[0]
						for kap in result[0][npi].tags:
							npstring +=  nltk.tag.util.tuple2str(kap,'/') + ' '
						
						nel.appendChild(doc.createTextNode(npstring))
					
					# pun lista de clustere
					clusters = []
					nodes = []
					for cli in range(len(result[1])):
						
						# daca e un cluster nou, trebuie creat un nod
						clj = 0
						while (clj < len(clusters) and clusters[clj] != result[1][cli]):
							clj = clj+1
						
						if clj >= len(clusters):
							# trebuie creat un nod nou
							clusters.append(result[1][cli])
							no = doc.createElement('Cluster')
							el.appendChild(doc.createTextNode('\n\t\t'))
							el.appendChild(no)
							nodes.append(no)
							clj = len(nodes) - 1
							no.setAttribute('id', str(clj + 1))

							
						cel = doc.createElement('NPid')
						cel.setAttribute('id',str(cli+1))
						nodes[clj].appendChild(cel)
		
		# output part
		file = open(fname_out, 'w')
		doc.writexml(file)
		file.close()
		
		# inchid reader
		self.reader.close()


#c = CorefRes()
#print c.clusterize('Jerry has a Corvette. It looks great because he polishes it every day.', 50.0)