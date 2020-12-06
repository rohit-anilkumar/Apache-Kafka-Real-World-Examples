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
    """
    

    Parameters
    ----------
    payload : Dict
        Dictionary of data values that needs to be serialized before sending to Kafka topics.

    Returns
    -------
    return_payload : json
        json data encoded to utf-8
        
    """
    return_payload = json.dumps(payload).encode('utf-8')
    return return_payload


if __name__=='__main__':
    bbc = BBCParser()
    prev_top_news = None
    top_news = None
    
    bootstrap_servers = '127.0.0.1:9092'
    client_id = 'bbc_feed_publisher'
    topic = 'bbcfeed'
    retries = 5
    
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers, client_id = client_id, retries = retries)
    
    while(True):
        status_code, items = bbc.getResponse()
        if(status_code == 200):
            parser_output = bbc.responseParser(items)
            final_news, top_news = bbc.newsOrganiser(parser_output)
            
        #Condition to check if its necessary to publish message to Kafka or not
        if(top_news == prev_top_news):
            print("Do not publish to Kafka")
        else:
            for news in final_news:
                if(news!= prev_top_news):        
                    print("Publishing to Kafka")
                    producer.send(topic, value=json_serializer(news))
                    time.sleep(0.5)
                else:
                    break
            prev_top_news = top_news
        print('Producer Disabled for 1 hr')
        time.sleep(3600)