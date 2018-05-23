#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat April 28 13:20:44 2018

@author: admin
"""

from collections import deque
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import urllib.request
import http.client

#mkdir htmls
#variables are given

url = "http://www.mentalhealthamerica.net/"
maxPages = 100
drt = "htmls/" 

queue = deque([])
visited_list = []


def crawl(url, maxPages, algo):
    
    visited_list.append(url)
    if len(queue) > maxPages:
        return

    urlf = urllib.request.urlopen(url)
    urlf = urlf.read()
    soup = bs(urlf,'lxml')
    urls = soup.findAll("a", href=True)

    for i in urls:
        flag = 0
        complete_url = urljoin(url, i["href"]).rstrip('/')

        # complete_url in queue
        for j in queue:
            if j == complete_url:
                flag = 1
                break
        # complete_url not in queue
        if flag == 0:
            if len(queue) > maxPages:
                return
            if (visited_list.count(complete_url)) == 0:
                queue.append(complete_url)

    #bfs 
    if algo == "bfs":
        current = queue.pop(0)
    elif algo == "dfs":
        current = queue.pop()
    #current = queue[0]
    crawl(current,maxPages)

# record the index of url in index.dat file
with open("index.dat","a") as wd:
    for url in queue:
        wd.write(str(queue.index(url)) + " " + url + "\n")


# download url into [index].html and save in htmls folder
for url in queue:
    try: 
        link = urllib.request.urlopen(url)
        html = link.read()
    except(http.client.IncompleteRead) as e:
        html = e.partial
    
        
    n_doc = drt + str(queue.index(url)) + '.html'
    if url == 'http://www.myplanmylife.com':
        continue
    else: 
        with open(n_doc,"wb") as wf:
            wf.write(html)
            
'''
There is one page in BFS is no longer existed. Therefore the request is denied.
This is what I used to create new ones 

for url in queue: 
    if queue.index(url) > 90:
        link = urllib.request.urlopen(url)
        html = link.read()
        
        n_doc = drt + str(queue.index(url)) + '.html'
        with open(n_doc, "wb") as wf:
            wf.write(html)
'''
 
#if __name__ == '__main__':
#    crawl(url,maxPages,"bfs")