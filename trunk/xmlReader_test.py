import xmlReader
from general import *
from nltk.corpus import wordnet as wn


print '-------------------------------------------------'
#dictionar
freq_dict = {}


r = xmlReader.XMLReader()
r.read('xml/4.xml')

for msg in r.doc:
	#print msg.id,":",msg.refid,":",msg.nick," : ",stripStopWords_split(msg.text)," || ",msg.text
	updateFreqList(stripStopWords_split(msg.text),freq_dict)


print ''
print ''

freq_dict = sort_freq_dict(freq_dict,50)
print freq_dict
word = freq_dict[0]
word2 = freq_dict[7]
print word[0];



print 'START'

w1 = wn.synsets(word[0])[0];
w2 = wn.synsets(word2[0])[0];
print w1,w2
print w1.lch_similarity(w2);


print ''
#print freq_dict
print 'END'
