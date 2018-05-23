#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 15:10:49 2018

@author: admin
"""

print("Content-Type: text/html")
print()


import cgi, cgitb
import nltk, csv, operator,string
from nltk.stem import PorterStemmer
from collections import defaultdict


input_w = "how to get help"
cgitb.enable()




def load_stopwords():
    f = open("stopwords.txt").read()
    stop_list = f.split('\n')
    puncations = list(set(string.punctuation))
    for i in puncations:
        stop_list += i
    return stop_list

def valid_input(word):
    stopwords = load_stopwords()
    input_ls = word.split(" ")
    filtered_words = [word for word in input_ls if word not in stopwords] #remove stopped words
    porter = PorterStemmer()
    ported_words = [porter.stem(word) for word in filtered_words]
    return ported_words

input_ls = valid_input(input_w)

def retrieve(words):

    with open('invindex.dat','r') as input_file:
        reader = csv.reader(input_file, delimiter='>')
        inverted_index_dict = dict((rows[0], rows[1:]) for rows in reader)

    words = valid_input(words)

    documents_explored = 0
    text_fre = 0

    text_frequency_dict = defaultdict(list)
    frequency_dict = defaultdict(list)

    for word in words:
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
    sorted_frequency_dict = sorted(frequency_dict.items(), key=operator.itemgetter(1))
    sorted_frequency_dict.reverse()

    fixed_list = []

    for item in sorted_frequency_dict:
        fixed_list.append(item[0])
    print("<p>" + str(len(sorted_frequency_dict)) + " webpages is searched." + "<p>")

    return fixed_list

results = retrieve(input_w)

def search(words):
    word = valid_input(words)
    results = retrieve(words)
    return results


form = cgi.FieldStorage()
query = form.getfirst("query","test_default").lower()



print("<html>")
print("<head>")
print("<meta charset='UTF-8'>")
print("<title>Mental Health Search Engine </title>")
print("</head>")
print("")
print("	<style>")
print("      .center {")
print("	  display: block")
print("      margin: auto;")
print("      width: 50%;")
print("      }")
print("")
print("	.input[type=text] {")
print("    width: 600px;")
print("    box-sizing: border-box;")
print("    border: 2px solid #ccc;")
print("    font-size: 16px;")
print("    background-color: white;")
print("    background-image: url('searchicon.png');")
print("    background-position: 20px 5px; ")
print("    background-repeat: no-repeat;")
print("    padding: 12px 20px 12px 40px;")
print("    -webkit-transition: width 0.4s ease-in-out;")
print("    transition: width 0.4s ease-in-out;")
print("}")
print("")
print("      input[type=text]:focus {")
print("    width: 100%;")
print("	}")
print("	</style>")

print("	")
print("<body>")
print("")
print("<img src='americanhealth.jpg' width='600' height='300' class='center'>")
result = search(query)
print ("<p>" + str(len(results)) + " results found for search query: "+ query+"</p>")

for result in results:
    unknow_pages = 1
    if result is None:
        print("<p> unknown pages is found </p><br>")
    else:
        print("<p> result is found <p>")

print("	")
print("</body>")
print("</html>")
