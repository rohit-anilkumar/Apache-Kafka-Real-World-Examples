#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 20:26:46 2020

@author: rohit
"""
from bbc_xml_feed_parser import BBCParser
from kafka import KafkaProducer
import time
import json

def json_serializer(payload):
    return_payload = json.dumps(payload).encode('utf-8')
    return return_payload

 
if __name__=='__main__':
    bbc = BBCParser()
    prev_top_news = None
    
    bootstrap_servers = '127.0.0.1:9092'
    client_id = 'bbc_feed_publisher'
    
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers, client_id = client_id)
    
    while(True):
        status_code, items = bbc.getResponse()
        if(status_code == 200):
            parser_output, top_news = bbc.responseParser(items)
        
        #Condition to check if its necessary to publish message to Kafka or not
        if(top_news == prev_top_news):
            print("Do not publish to Kafka")
        else:
            for news in parser_output:
                if(news!= prev_top_news):        
                    print("Publishing to Kafka")
                    producer.send('bbcfeed', value=json_serializer(news))
            prev_top_news = top_news
        time.sleep(3)