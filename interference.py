import xmlReader
import tagger
from general import *
from nltk.corpus import wordnet as wn
from xmlReader import XMLReader
import cuephrases
from cuephrases import *
		
class Interference:
	def __init__(self, inFile):
		self.inFile = inFile
		self.listInt={}
		self.finalCon=[]
		self.words={}
		r = xmlReader.XMLReader()
		r.read(inFile)
		for msg in r.doc:
			self.words[msg.id] = msg.text
		r.close()
	
	def addInf(self, id1, id2, sim):
		aux = []
		aux.append(id2)
		aux.append(sim)
		if id1 not in self.listInt:
			self.listInt[id1]= []
		self.listInt[id1].append(aux)

	def sortInf(self, inf):
		listSim=[]
		while(len(self.listInt[inf])>0):
			maxSim= self.listInt[inf][0]
			for items in self.listInt[inf]:
				if(items[1]>maxSim[1]):
					maxSim=items	
			listSim.append(maxSim)
			self.listInt[inf].remove(maxSim)
		self.listInt[inf] = listSim
		#print self.listInt[inf]
		return listSim

	def invertInf(self, inf):
		listSim=[]
		i=len(self.listInt[inf])-1
		while i>=0:
			listSim.append(self.listInt[inf][i])
			i=i-1 
		self.listInt[inf] = listSim
		return listSim

	def cond(self, repl, word, tip):
		if(tip==2 and self.typeInf(word)=="afirmation"):
			return 1
		return 0

	def typeInf(self, word):
		if (word in consequence):
			return "consequence"
		if (word in elaboration):
			return "elaboration"
		if (word in confirmation):
			return "confirmation"
		if (word in conclusion):
			return "conclusion"
		if (word in timing):
			return "timing"
		if (word in contrast):
			return "contrast"
		return "anaphor"

	def calcInf(self):
		for inf in self.listInt:
			phrase = self.words[inf]
			#print inf," - ",phrase
			self.sortInf(inf)
			word = phrase.split(" ")
			i=0
			gasit=-1
			if(len(word)>0):
				if(word[0] in cue_phrases):
					gasit =0 
			if(len(word)>1):			
				if(word[1] in cue_phrases):
					gasit =1 
			if(len(word)>2):
				if(word[2] in cue_phrases):
					gasit =2 
			if(gasit!= -1 and self.cond(phrase, word[gasit],1)==0):
				#avem o legatura intre inf si prima intrare din lista
				aux=[]
				aux.append(self.listInt[inf][0][0])
				aux.append(inf)
				aux.append(phrase)
				aux.append(self.typeInf(word[gasit]))   #cautam in ce lista se afla cuvantul gasit
				self.finalCon.append(aux)
				#print aux
				break
			while i< len(self.listInt[inf]):
				leg = self.listInt[inf][i][0]
				if str(leg) in self.words: 	
					phraseAux = self.words[str(leg)]
					wordAux = phraseAux.split(" ")
					gasit=-1
					if(wordAux[len(wordAux)-1] in cue_phrases):
						gasit =1
					
					if(gasit!= -1 and self.cond(self.words[wordAux[len(wordAux)-1]], wordAux[len(wordAux)-1], 2)==0):
					#avem legartura intre inf si leg
					#vedem ce tip are lagatura
						aux=[]
						aux.append(leg)
						aux.append(inf)
						aux.append(self.words[str(self.listInt[inf][i][0])])
						aux.append(self.typeInf(wordAux[len(wordAux)-1]))  
						self.finalCon.append(aux)
						print aux
						print "gasit ",wordAux[len(wordAux)-1]
						break
				i=i+1

	def writeInterf(self,outFile):
			reader = XMLReader()
			reader.read(self.inFile)			
			doc = reader.xmldoc
			de = doc.documentElement
			# verific daca exista sectiunea Analysis
			if len(de.getElementsByTagName('Analysis')) == 0:
				el = doc.createElement('Analysis')
				de.appendChild(el)
		
			anod = de.getElementsByTagName('Analysis')[0]
		
			if len(anod.getElementsByTagName('Interference')) > 0:
				pnod = anod.getElementsByTagName('Interference')[0]
				anod.removeChild(pnod)
		
			pnod = doc.createElement('Interference')
			anod.appendChild(doc.createTextNode('\n'))
			anod.appendChild(pnod)
			anod.appendChild(doc.createTextNode('\n'))
		
			# parcurg toata lista de interferente
			for con in self.finalCon:
				aux = doc.createElement('Infer')
				pnod.appendChild(doc.createTextNode('\n\t'))
				pnod.appendChild(aux)
				pnod.appendChild(doc.createTextNode('\n\t'))
			
				uel = doc.createElement('TextUt')
				aux.appendChild(doc.createTextNode('\n\t'))
				aux.appendChild(uel)
				uel.setAttribute("from", str(con[0]))
				uel.setAttribute("to", str(con[1]))
				uel.setAttribute("type", str(con[3]))
				uel.appendChild(doc.createTextNode(str(con[2])))
				
				aux.appendChild(doc.createTextNode('\n'))
			
			anod.appendChild(doc.createTextNode('\n'))
			
			# write modified xml DOM tree in fisier
			file = open(outFile, 'w')
			reader.xmldoc.writexml(file)
			file.close()
			reader.close()
			
		
