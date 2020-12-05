#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:37 2020

@author: rohit
"""
from bs4 import BeautifulSoup
import requests
import time

class BBCParser():
    """
    Class to read from BBC RSS feed
    """
    
    def __init__(self):
        self.bbc_url = "http://feeds.bbci.co.uk/news/rss.xml"
        self.response = None
        self.status = 404
        self.parsedItems=[]
        self.curr_top_news = None
    
    def getResponse(self):
        """
        Function to read from BBC RSS Feed

        Returns
        -------
        TYPE: Integer
            Status code, 200 if success else 404
        TYPE: ResulSet
            Response from BBC RSS feed

        """
        
        self.response = requests.get(self.bbc_url)
        self.response = BeautifulSoup(self.response.content, features= 'xml')
        
        if (self.response !=None):
            self.status = 200
            self.items = self.response.find_all('item')
        return self.status, self.items
        
    
    def responseParser(self, items):
        """
        Function to parse the feed and get elements required from it.

        Parameters
        ----------
        items : List
            List of all items parsed from the XML Feed

        Returns
        -------
        TYPE: List
            List of interested items parsed from the XML Feed
        TYPE: String
            Top item from the parsed XML Feed

        """
        
        for item in items:
            item_dict = {}
            item_dict['title'] = item.title.text
            item_dict['link'] = item.link.text
            item_dict['createdOn'] = item.pubDate.text
            self.parsedItems.append(item_dict)
        self.curr_top_news = self.parsedItems[0]['title']
        return self.parsedItems,self.curr_top_news


if __name__=='__main__':
    bbc = BBCParser()
    prev_top_news = None
    while(True):
        status_code, items = bbc.getResponse()
        if(status_code == 200):
            parser_output, top_news = bbc.responseParser(items)
            print(top_news)
        if(top_news == prev_top_news):
            print("Do not publish to Kafka")
        else:
            print("Publish to Kafka")
            prev_top_news = top_news
        time.sleep(3600)
        
