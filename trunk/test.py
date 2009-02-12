import xmlReader
import tagger
import stopwords
import lexChains 
from general import *
from nltk.corpus import wordnet as wn
from xmlReader import XMLReader
from lexChains import LexChains		
from interference import *

def getChains():
	words=[]
	lex = LexChains("xml/4.xml")

	for msg in lex.r.doc:
		words.append(msg.id)
		words.append(msg.text)
		word = stripStopWords_split(msg.text)
		for wd in word:
			aux = wd.split('/')
			if(aux[1] == "NN" or aux[1] == "NNS" or aux[1] == "VBD"):
				if(aux[0]!=""):
					if(aux[0] not in stopwords.stop_words and aux[0] not in stopwords.alt_stop_words):
						syn = wn.synsets(aux[0], pos='n')
						if(syn != []):
							print syn[0]," ",msg.id
							if( lex.testFirst(msg.id, syn[0]) == 0):
								# luam fiecare lant lexical si cautam cu maxim 10 propozitii in urma cuvinte puternic similare 
								# si cu 5 prop in urma cele similare medium
								# calculam pentru fiecare lant apropierea 
								lex.addToChainList(msg.id, syn[0])

	#lex.writeLexChains('xml/testLC.xml')
	inf = lex.getInterference()
	inf.calcInf()
	inf.writeInterf("xml/testInf.xml")




print '-------------------------------------------------'

getChains()

print ''

print 'END'
