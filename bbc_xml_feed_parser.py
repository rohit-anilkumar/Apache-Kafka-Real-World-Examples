#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:37 2020

@author: rohit
"""
from bs4 import BeautifulSoup
import requests


class BBCParser():
    """
    Class to read from BBC RSS feed
    """
    
    def __init__(self):
        self.bbc_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
        self.response = None
        self.curr_top_news = None
        self.status = 404
        self.parsedItems=[]
        self.items=[]
        
    def getResponse(self):
        """
        Function to read from BBC RSS Feed

        Returns
        -------
        TYPE: Integer
            Status code, 200 if success else 404
        TYPE: ResultSet
            Response from BBC RSS feed

        """
        
        self.response = requests.get(self.bbc_url)
        self.response = BeautifulSoup(self.response.content, features= 'xml')
        
        if (self.response !=None):
            if(self.response.find_all('link')[0].text == 'https://www.bbc.co.uk/news/'):  
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

