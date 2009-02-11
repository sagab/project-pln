from stopwords import stop_words,alt_stop_words
from stemmer import Stemmer
from operator import itemgetter

def stemming(self, word):
	return self.stemmer.stem(word)

def isStopWord(token):
	return ((token in stop_words) or (token in alt_stop_words))

# strip la un string si return tot string
def stripStopWords_nosplit(text):
	rez = text 
	for token in text.split():
		if len(token) > 1 and isStopWord(token):
			rez = rez.replace(token,'')
	return rez

# strip la un string si return lista de tokens
def stripStopWords_split(text):
	rez = [] 
	for token in text.split():
		if len(token) > 1 and not isStopWord(token):
			rez.append(token)
	return rez

# token_list este o lista de cuvinte, freq_dict dictionar de frecvente
# o apelez la fiecare linie si imi produce un dict de genul 'naive':56 , 'kmeans':33 etc in fct de ce cuv primeste
def updateFreqList(token_list,freq_dict):
	for token in token_list:
		token=token.lower()
		if token not in freq_dict:
			freq_dict[token]= 0
		freq_dict[token] += 1

# sorteaza un dictionar de frecvente si il taie la primele max_entries, daca e dat parametrul
# returneaza un array de liste de forma (cuv1,23) (cuv2,22) etc
def sort_freq_dict(freq_dict,max_entries=0):
	fd_items = freq_dict.items()	
	fd_items.sort(key = itemgetter(1),reverse=True)
	if(max_entries != 0):
		return fd_items[:max_entries]
	else:
		return fd_items


