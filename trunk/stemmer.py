"""
PLN Toolkit Project

Clasa Stemmer implementeaza operatiile de stemming
pentru:

- un cuvant dat printr-un string

- toate cuvintele dintr-un fisier chat XML dat ca parametru, cu
	output alt fisier XML

"""

import nltk
from xmlReader import XMLReader
from stopwords import StopWords

class Stemmer:
	def __init__(self):
		self.reader = XMLReader()
		self.stemmer = nltk.PorterStemmer()
		self.stopworder = StopWords()
	
	# stem a single word given as a string
	def stem (self, word):
		return self.stemmer.stem(word)

	# stems a whole XML chat file and outputs the results
	# prior steps: tokenize, stopword elimination
	def stemXML (self, fname_in, fname_out):
		self.reader.read(fname_in)
		
		doc = self.reader.xmldoc
		de = doc.documentElement
		
		# verific daca exista sectiunea Analysis
		if len(de.getElementsByTagName('Analysis')) == 0:
			el = doc.createElement('Analysis')
			de.appendChild(el)
		
		anod = de.getElementsByTagName('Analysis')[0]
		
		# verific daca exista sectiunea Stemming. daca da, o sterg.
		# pentru a reface tot Stemming-ul
		if len(anod.getElementsByTagName('Stemming')) > 0:
			snod = anod.getElementsByTagName('Stemming')[0]
			anod.removeChild(snod)
		
		snod = doc.createElement('Stemming')
		anod.appendChild(doc.createTextNode('\n'))
		anod.appendChild(snod)
		anod.appendChild(doc.createTextNode('\n'))
		
		# iau fiecare Utterance din document si o stemmez dupa ce fac pe ea
		# tokenize + stop words
		for u in self.reader.doc:
			stuel = doc.createElement('StemUt')
			
			# pun id-ul elementuliu StemUt sa referentieze id-ul replicii originale <Utterance>
			stuel.setAttribute('id', u.id)
			
			snod.appendChild(doc.createTextNode('\n\t'))
			snod.appendChild(stuel)
			
			# fac stop words elimin si obtin o lista de cuvinte
			stems = self.stopworder.getWords2(u.text)
			
			text = ''
			for w in stems:
				text += self.stem(w) + ' '
			
			# adaug textul obtinut din stemming
			stuel.appendChild(doc.createTextNode(text))
		
		# scriu continutul DOM in fisierul de output
		file = open(fname_out, 'w')
		self.reader.xmldoc.writexml(file)
		file.close()
		self.reader.close()

