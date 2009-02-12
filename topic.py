import xmlReader
from general import *
from nltk.corpus import wordnet as wn
import stemmer
import sys
from topicFunctions import *

#dictionare 
freq_dict = {}
bfreq_dict = {}
tfreq_dict = {}


r = xmlReader.XMLReader()
r.read('xml/4.xml')

for msg in r.doc:
	#eliminare fraze chat standard
	if(msg.text.startswith('joins the room') or msg.text.startswith('leaves the room')):
		continue
	updateFreqList(stripStopWords_split(msg.text),freq_dict)
	updateFreqList(getBigramList(stripStopWords_nosplit(msg.text)),bfreq_dict)
	updateFreqList(getTrigramList(stripStopWords_nosplit(msg.text)),tfreq_dict)

freq_dict = sort_freq_dict(freq_dict,50)
tfreq_dict = sort_freq_dict(tfreq_dict,15)
bfreq_dict = sort_freq_dict(bfreq_dict,15)

a = topicUnigrams(freq_dict)
b = topicBigrams(bfreq_dict)
c = topicTrigrams(tfreq_dict) 
#print b
print getMultigramTopList(b,5)

#print a
print getUnigramTopList(a,5)


