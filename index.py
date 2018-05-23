#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 02 18:24:35 2018

@author: admin
"""


import bs4, nltk, re,string
from bs4 import BeautifulSoup
import nltk.stem.porter as p
import networkx as nx
import lxml.html, os
from nltk.stem import PorterStemmer

def load_stopwords():
    f = open("stopwords.txt").read()
    stop_list = f.split('\n')
    puncations = list(set(string.punctuation))
    for i in puncations:
        stop_list += i
    stop_list.append('...')
    return stop_list

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    return True


def read_file(file):
    with open("htmls/" + file, encoding="utf8",errors="ignore") as f:
        html_f = f.read()
        
        doc = html_f.replace('&nbsp;', ' ')
        doc = doc.replace('\n',' ')
        
        soup = BeautifulSoup(doc, 'lxml')
        content = soup.findAll(text=True)
        
        handled_content = filter(visible, content)
        printable = set(string.printable)
        
        new_word = ""
        
        for content in handled_content:
            for letter in content:
                if letter in printable:
                    new_word = new_word + letter.lower()
        
        
       
        tokenization = nltk.word_tokenize(new_word)
        stopwords = load_stopwords()
        removed_stopwords = [word.lower() for word in tokenization if word not in stopwords]
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(token) for token in removed_stopwords]
    return stemmed_words

#f = read_file("1")


def get_page_title(file):
    try:
        soup = bs4.BeautifulSoup(open("htmls/" + file, "r", encoding="UTF-8").read(),"lxml")
        title = soup.title.string
        title = re.sub(r'[^a-zA-z0-9:. |]', '', title)
        return title
    except:
        print("error")
       

def indexer():
    
    docs_dat = {}
    
    inverted_dict= {}
    
    with open("index.dat","r") as df:
        data = df.readlines()
        
        for line in data:
            ind_file = str(line.split()[0]) + ".html"
            links = line.split()[1]
            content = read_file(ind_file)
            
            docs_dat[ind_file] = {}
            docs_dat[ind_file] = str(len(content)) + " " + str(get_page_title(ind_file)).replace(' ','_') +" "+ str(links)
            
            #from CLFraction
            for item in content:
                word = str(item)
                if word in inverted_dict:
                    tep_word = inverted_dict[word].split()
                    files_visited = []
                    for i in range(0, len(tep_word)):
                        files_visited.append(tep_word[i].split(':')[0])
                        if tep_word[i].split(':')[0] == ind_file:
                            n_updated = int(tep_word[i].split(':')[1]) + 1 
                            entry_updated = ind_file + ":" + str(n_updated)
                            del tep_word[i]
                            tep_word.append(entry_updated)
                            update = ' '.join(tep_word)
                            inverted_dict[word] = update
                            break
                        if ind_file not in files_visited:
                            update = ' '.join(tep_word) + ' ' + ind_file + ":1"
                            inverted_dict[word] = update
                 
                else:
                    new_entry = ind_file + ":1"
                    inverted_dict[word] = new_entry
    



        with open("doc.dat","w",encoding="UTF-8") as docs:
            for key in docs_dat:
                    docs.write(key+ "&" + docs_dat[key] + '\n')
        
        with open("inverted.dat","w",encoding="UTF-8") as idocs:
            for key in inverted_dict:
                idocs.write(key + ">"+inverted_dict[key]+'\n')
        
i = indexer()
