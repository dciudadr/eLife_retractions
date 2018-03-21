import re
import random

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#from nltk.stem import WordNetLemmatizer
#lemmatizer = WordNetLemmatizer() # Checking all_words later, I think it doesn't work properly

from nltk.stem import PorterStemmer
ps = PorterStemmer()

# We will keep words from stopwords that could be used when criticing
stop_words = set(stopwords.words('english')) - set(["while", "against", "before", "after", "just", "don", 
                                                    "don't", "should", "should've", "no", "nor", "not",
                                                    "ain", "aren", "aren't", "couldn", "couldn't", "didn",
                                                    "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn",
                                                    "hasn't", "haven", "haven't", "isn", "isn't", "ma",
                                                    "mightn", "mightn't", "mustn", "mustn't", "needn", 
                                                    "needn't", "shan", "shan't", "shouldn", "shouldn't",
                                                    "wasn", "wasn't", "weren", "weren't", "won"," won't",
                                                    "wouldn", "wouldn't"])


def get_stemmed_sentence(list_sentences):
    list_stemmed_sentences = []
    for sentence in list_sentences:    
        filtered_sentence = []
        word_tokens = word_tokenize(sentence)
        for word in word_tokens:
            word = re.sub("[\d?, '\W+]", "", word) #Let's remove any number
            if (len(word) > 2) and (not word in stop_words):
                filtered_sentence.append(ps.stem(word.lower()))    
        list_stemmed_sentences.append(filtered_sentence)    
    return list_stemmed_sentences


def get_stemmed_sentences_and_list_words(list_sentences, classification):
    list_all_words = []
    document_stemmed = []
    for sentence in list_sentences:
        filtered_sentence = []
        word_tokens = word_tokenize(sentence)
        for word in word_tokens:
            word = re.sub("[\d?, '\W+]", "", word) #Let's remove any number
            if (len(word) > 2) and (not word in stop_words):
                filtered_sentence.append(ps.stem(word.lower()))    
                list_all_words.append(ps.stem(word.lower()))  
        document_stemmed.append((filtered_sentence, classification))
        
    bigrams = []
    for document in document_stemmed:
        doc, clas = document
        bigrams = bigrams + list(nltk.bigrams(doc)) # nlt.birgrams gives a bigram generator, but it produces the list when asking for it. https://stackoverflow.com/questions/32446892/the-function-bigrams-in-python-nltk-not-working
        
    return document_stemmed, list_all_words, bigrams


    

def get_tuple_articles_stemmed_classified_and_list_words(list_sentences_before, list_sentences_after, label_before = 'before', label_after = 'after'):

    document_before, list_words_before, list_bigrams_before = get_stemmed_sentences_and_list_words(list_sentences_before, label_before)

    document_after, list_words_after, list_bigrams_after = get_stemmed_sentences_and_list_words(list_sentences_after, label_after)

    documents_before_and_after = document_before +  document_after
    random.shuffle(documents_before_and_after)

    list_all_words = sorted(list_words_before + list_words_after) #sorted(list(set(list_all_words_before + list_all_words_after)))
    list_all_bigrams = sorted(list_bigrams_before + list_bigrams_after)
    
    return(documents_before_and_after, list_all_words, list_all_bigrams)
    