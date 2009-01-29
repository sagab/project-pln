
import nltk.corpus
from nltk.corpus import brown

from nltk import *

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):  
	if not backoff:  
		backoff = tagger_classes[0](tagged_sents)  
		del tagger_classes[0]  
   
	for cls in tagger_classes:  
		tagger = cls(tagged_sents, backoff=backoff)  
		backoff = tagger  
   
	return backoff 

tokens = "John saw three polar bears that quickly moved through the dense forest and i just finished my PLN project.".split()
def_tag = DefaultTagger('NN')
a = def_tag.tag(tokens)
print a


conll_sents = nltk.corpus.conll2000.tagged_sents()  
conll_train = list(conll_sents[:4000])  
conll_test = list(conll_sents[4000:8000])

ubt_tagger = backoff_tagger(conll_train, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger])
b = ubt_tagger.tag(tokens)
print b
