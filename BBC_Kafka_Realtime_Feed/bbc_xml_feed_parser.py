#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:40:37 2020

@author: rohit
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

class BBCParser():
    """
    Class to read from BBC RSS feed
    """
    
    def __init__(self):
        self.bbc_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
        self.response = None
        self.status = 404  
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
        parsedItems=[]
        for item in items:
            item_dict = {}
            item_dict['title'] = item.title.text
            item_dict['link'] = item.link.text
            item_dict['createdOn'] = item.pubDate.text
            parsedItems.append(item_dict)    
        return parsedItems
    
    def newsOrganiser(self, parser_output):
        """
        Function to reorder dataframe based on timestamp

        Parameters
        ----------
        parser_output : Dataframe
            Pandas df output from responseParser method.

        Returns
        -------
        final_news_dict : List of dicts
            Dictionary of reordered records.
        top_news : string
            Top element from title field.

        """
        news_df = pd.DataFrame(parser_output)
        news_df['TS'] = news_df['createdOn'].apply(lambda x:pd.Timestamp(x))
        news_df['PublishDateTime'] = pd.to_datetime(news_df['TS'], format='%Y-%m-%d %H:%M:%S-%Z',errors='coerce').astype(str)
        news_df = news_df.sort_values('PublishDateTime', ascending=False, ignore_index=True)
        final_news_df = news_df.drop(['createdOn','TS'], axis=1)
        top_news = final_news_df['title'].iloc[0]
        final_news_dict = final_news_df.to_dict(orient='records')
        return final_news_dict, top_news

