from stopwords import StopWords
from stemmer import Stemmer

def read_xml():
	return "I am sleeping and I like fishing"

class XMLProcessing:
	def __init__(self):
		self.stemmer = Stemmer()
		self.sw = StopWords()
		self.fin = read_xml()

	def stemming(self, word):
		return self.stemmer.stem(word)

	def process(self):
		for token in self.sw.getWords2(self.fin):
			token = self.stemming(token)
			print token

ana = XMLProcessing()
ana.process()
