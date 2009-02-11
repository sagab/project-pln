import nltk
from nltk.corpus import brown

class Tagger:
	def __init__(self):
		
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
	
	def tag (self, tokenlist):
		return self.bigram_tagger.tag(tokenlist)


raw = "The boy had his lovely car parked outside his house. He changed its oil."
tokens = nltk.word_tokenize(raw.lower())
t = Tagger()
tokens = t.tag(tokens)
print tokens
