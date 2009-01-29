from stopwords import stop_words
from stemmer import PorterStemmer

def read_xml():
	return "I am sleeping and I like fishing"

class XMLProcessing:
	def __init__(self):
		self.stemmer = PorterStemmer()
		self.fin = read_xml()

	def stemming(self, word):
		return self.stemmer.stem(word, 0, len(word) - 1)

	def process(self): 
		for token in self.fin.split():
			if len(token) > 1 and not token in stop_words:
				token = self.stemming(token)
				print token

ana = XMLProcessing()
ana.process()
