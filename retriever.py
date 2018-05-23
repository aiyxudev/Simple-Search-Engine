#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon April 30 22:39:31 2018

@author: admin
"""
import csv
import string,operator,random
#from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict

def load_stopwords():
    f = open("stopwords.txt").read()
    stop_list = f.split('\n')
    puncations = list(set(string.punctuation))
    for i in puncations:
        stop_list += i
    return stop_list

# mode = or, return pages that include any of the keywords 
# mode = and, return pages that include all of the keywords 
# mode = most, return pages that include most of the keywords
def valid_input(words):
    stopwords = load_stopwords()
    filtered_words = [word for word in input_ls if word not in stopwords] #remove stopped words
    porter = PorterStemmer()
    ported_words = [porter.stem(word) for word in filtered_words]
    return ported_words     


def get_pr(word):
    
    with open('invindex.dat','r') as input_file:
        reader = csv.reader(input_file, delimiter='>')
        inverted_index_dict = dict((rows[0], rows[1:]) for rows in reader)

    text_fre = 0
    
    frequency_dict = defaultdict(list)
    
    if word in inverted_index_dict:
        text_list = inverted_index_dict[word]
        text_fre = 0
        for text in text_list:
            item_list = text.split(' ')
            for item in item_list: 
                htmlind, sep, fre = item.partition(':')
                text_fre += int(fre)
                    
                if htmlind in frequency_dict:
                    frequency_dict[htmlind] += (float(fre)/text_fre)
                else:
                    frequency_dict[htmlind] = (float(fre)/text_fre)
    return frequency_dict


def retriever(mode, words):   
    words = valid_input(words)
    text_fre_dict = defaultdict(list)
    
    for word in words: 
        word_fre = get_pr(word)
        if word not in text_fre_dict: 
            text_fre_dict[word] = word_fre
        else:
            text_fre_dict[word] = ""
    
    if mode == "and" :
        return text_fre_dict
    elif mode == "or":
        return text_fre_dict[random.choice(list(text_fre_dict.keys()))]
    elif mode == "most":
        for key in text_fre_dict:
            fre_dict = text_fre_dict[key]
            sorted_frequency_dict = sorted(fre_dict.items(), key=operator.itemgetter(1))
        return sorted_frequency_dict[-1]
    else:
        print("Please enter valid values.")
    
    
        
if __name__ == "__main__":
    input_ls  = ["current","skip"]
    rm = retriever("or",input_ls)


