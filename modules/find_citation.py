import re 
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from lxml import etree
from nltk.tokenize import sent_tokenize


def is_cited(text, reference_id):
    cited_in_text = False
    if re.search(reference_id, str(text), re.IGNORECASE) != None:
        cited_in_text = True
    return cited_in_text


def sentences(text, reference_id, number_of_additional_sentences_after_citation = 0):
    list_sentences_citing = []
    list_index = []
    
    sentences = sent_tokenize(str(text))
    enumerated_sentences = enumerate(sentences)
    
    for (index, sentence) in enumerated_sentences:
        if reference_id in sentence:
            #sentences_citing.append(sentence)
            list_index.append(index)
    
    for index in list_index:
        
        to_index = index + number_of_additional_sentences_after_citation + 1
        if to_index > len(sentences):
            to_index = len(sentences)
            
        list_sentences_citing = list_sentences_citing + sentences[index: to_index]
        
    list_sentences_citing_without_repetitions = list(set(list_sentences_citing)) 
    
    return list_sentences_citing_without_repetitions
    #list_sentences_citing = []
    #for (index, sentence) in list_enumerated_sentences_citing_without_repetitions:
    #    list_sentences_citing = list_sentences_citing + sentence
    
    
    #return sentences_citing


