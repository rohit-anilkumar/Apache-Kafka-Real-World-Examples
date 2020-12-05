#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 20:26:46 2020

@author: rohit
"""


from bbc_xml_feed_parser import BBCParser
import time

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