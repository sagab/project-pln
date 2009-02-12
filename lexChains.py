import xmlReader
import tagger
from general import *
from nltk.corpus import wordnet as wn
from xmlReader import XMLReader
import cuephrases
import interference
from interference import *
from cuephrases import *

class LexChains:
	def __init__(self, inFile):
		self.semChains=[]
		self.fname_in = inFile
		r = xmlReader.XMLReader()
		r.read(inFile)
		post = tagger.Tagger()
		post.tagXML(inFile,'xml/post.xml')
		self.r = xmlReader.XMLReader()
		self.r.readPOST('xml/post.xml')
		self.infer = Interference(inFile)

	def writeLexChains(self,outFile):
			reader = XMLReader()
			reader.read(self.fname_in)			
			doc = reader.xmldoc
			de = doc.documentElement
			# verific daca exista sectiunea Analysis
			if len(de.getElementsByTagName('Analysis')) == 0:
				el = doc.createElement('Analysis')
				de.appendChild(el)
		
			anod = de.getElementsByTagName('Analysis')[0]
		
			# verific daca exista sectiunea LexChain. daca da, o sterg.
			# pentru a reface tot LexChain
			if len(anod.getElementsByTagName('LexChains')) > 0:
				pnod = anod.getElementsByTagName('LexChains')[0]
				anod.removeChild(pnod)
		
			pnod = doc.createElement('LexChains')
			anod.appendChild(doc.createTextNode('\n'))
			anod.appendChild(pnod)
			anod.appendChild(doc.createTextNode('\n'))
		
			# parcurg toata lista de Lexical Chains
			for semChain in self.semChains:
				print " for 1", len(semChain)
				if(len(semChain) >= 2):
					print " if "
					aux = doc.createElement('Chain')
					pnod.appendChild(doc.createTextNode('\n\t'))
					pnod.appendChild(aux)
					pnod.appendChild(doc.createTextNode('\n\t'))
			
					for chain in semChain:
						print chain[1]," ",chain[0]
						uel = doc.createElement('TextUt')
						aux.appendChild(doc.createTextNode('\n\t'))
						aux.appendChild(uel)
						uel.setAttribute("id", str(chain[0]))
						uel.appendChild(doc.createTextNode(str(chain[1])))
					print "la"
					aux.appendChild(doc.createTextNode('\n'))
			
			anod.appendChild(doc.createTextNode('\n'))
			
			# write modified xml DOM tree in fisier
			file = open(outFile, 'w')
			reader.xmldoc.writexml(file)
			file.close()
			reader.close()


	def addToChainList(self, id, text):
		aux = []
		aux.append(id)
		aux.append(text)
		i = 0
		legmax = 1.5
		gasit = -1
		legGasit=-1
		for chain in self.semChains:
			#luam fiecare cuvant din chain in care id-ul propozitiei e cu max 10 in urma
			st=0
			j = len(chain)-1
			while j>=0 :
				dif = int(id) - int(chain[j][0])
				leg = text.lch_similarity(chain[j][1])
				if(dif > 7):
					break
				if(leg>3):
					#daca legatura este foarte puternica il adaugam in primul gasit
					gasit = i
					st = 1
					legmax=leg
					legGasit=chain[j][0]
					break
				if(dif <= 4):
					if(leg>legmax):
						legmax = leg
						gasit = i
						legGasit=chain[j][0]
				j=j-1
			i=i+1
			if (st == 1):
				break
		if(gasit != -1):
			# am gasit un lant semantic cu legatura pentru cuvant
			# avem o legatura intre replica gasit si legGasit cu similitudinea legmax
			self.infer.addInf(legGasit, gasit, legmax)
			self.semChains[gasit].append(aux)
			return gasit
		newChain=[]
		newChain.append(aux)
		self.semChains.append(newChain)
		return -1	

	def testFirst(self, mid, mtext):
		if(self.semChains==[]): # daca lista de lanturi este goala cream un nou lant
			#aduagam pe prima pozitie idul propozitiei din care face parte cuvantul
			chain=[]
			chain.append(mid)
			chain.append(mtext)
			newChain = []
			newChain.append(chain)
			self.semChains.append(newChain)
			print self.semChains
			return 1
		return 0	

	def getInterference(self):
		return self.infer






