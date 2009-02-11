#
# PLN Toolkit Project
# 
# Class Tagger realizeaza POST pe
# replicile dintr-un XML de chat si face outputul intr-un
# fisier ce retine continutul primului si adauga replicile tagged
#
# Se poate folosi si pentru tagging pe o lista de tokens pasata ca
# parametru. Prin token se intelege un cuvant stocat ca string.
#

import nltk
from nltk.corpus import brown
from xmlReader import XMLReader

class Tagger:
	def __init__(self):
		# pentru parsare xml input
		self.reader = XMLReader()
		
		# creeaza pattern pentru Reg Exp Tagger
		self.regpat = [
		(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),	# cardinal (numeral)
		(r'(The|the|A|a|An|an)$', 'AT'),	# article
		(r'.*able$', 'JJ'),			# adjective
		(r'.*ness$', 'NN'),			# nouns from adjectives
		(r'.*ly$', 'RB'),			# adverbs
		(r'.*s$', 'NNS'),			# plural nouns
		(r'.*ing$', 'VBG'),			# gerunds
		(r'.*ed$', 'VBD'),			# past tense verbs
		(r'.*', 'NN')]				# nouns (default)
		
		# default tagger pune doar NN la fiecare token
		self.default_tagger = nltk.DefaultTagger('NN')
		
		# regexp inlocuieste tagurile dupa patterns, si foloseste default_tagger daca nu e match
		self.regexp_tagger = nltk.RegexpTagger(self.regpat, backoff = self.default_tagger)
		
		# training set ce foloseste brown corpus
		brown_train = brown.tagged_sents(categories='news')[:500]
		
		# unigram tagger asigneaza tag dupa un training set cu tokens deja tagged
		# cand apare un token necunoscut, face regexp tagging
		self.unigram_tagger = nltk.UnigramTagger(brown_train, backoff = self.regexp_tagger)
		
		# bigram tagger
		self.bigram_tagger = nltk.BigramTagger(brown_train, backoff = self.unigram_tagger)
	
	# face tagging pe o lista de tokeni si intoarce rezultatul ca o lista de ('token', 'tag')
	def tag (self, tokenlist):
		return self.bigram_tagger.tag(tokenlist)

	# face tagging la un fisier chat XML si scrie outputul in alt fisier
	def tagXML (self, fname_in, fname_out):
		
		#read the input xml chat
		self.reader.read(fname_in)
		
		doc = self.reader.xmldoc
		de = doc.documentElement
		
		# verific daca exista sectiunea Analysis
		if len(de.getElementsByTagName('Analysis')) == 0:
			el = doc.createElement('Analysis')
			de.appendChild(el)
		
		anod = de.getElementsByTagName('Analysis')[0]
		
		# verific daca exista sectiunea POST. daca da, o sterg.
		# pentru a reface tot POST
		if len(anod.getElementsByTagName('POST')) > 0:
			pnod = anod.getElementsByTagName('POST')[0]
			anod.removeChild(pnod)
		
		pnod = doc.createElement('POST')
		anod.appendChild(doc.createTextNode('\n'))
		anod.appendChild(pnod)
		anod.appendChild(doc.createTextNode('\n'))
		
		# parcurg toata lista de Utterances
		for u in self.reader.doc:
			uel = doc.createElement('TagUt')
			pnod.appendChild(doc.createTextNode('\n\t'))
			pnod.appendChild(uel)
			uel.setAttribute("id", u.id)
			
			# tokenizare
			tok = nltk.word_tokenize(u.text)
			
			# POST
			tok = self.tag(tok)
			
			tags = ''
			for tup in tok:
				tags += nltk.tag.tuple2str(tup, '/') + ' '
				
			# adaug tags in nodul Element
			uel.appendChild(doc.createTextNode(tags))
			
			
		pnod.appendChild(doc.createTextNode('\n'))
			
		# write modified xml DOM tree in fisier
		file = open(fname_out, 'w')
		self.reader.xmldoc.writexml(file)
		file.close()
		
		self.reader.close()
		
t = Tagger()
t.tagXML('xml/4.xml', 'xml/test.xml')