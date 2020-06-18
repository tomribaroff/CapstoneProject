#libraries Dataframe manipulation, plotting and maths libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import statistics

#libraries to manage time and datetime objects
import dateutil
from datetime import datetime
import time

#library to help change object types (eg list to string)
import ast

#library to help acquire data off the internet 
import requests
from pandas_datareader import data as dr
import pandas_datareader


def get_keys(path):
    with open(path) as f:
        return json.load(f)
    
def guardian_headline_finder(r):
    #takes in r, the API response, and evaluates the text, returning a list of the headlines contained
    cleaner_headlines_list = []
    clean_headlines_list = []
    results = r.text.split("results")
    messy_headlines = results[1].split("webTitle")
    messy_headlines.pop(0)
    messy_headlines
    for x in messy_headlines:
        cleaner_headlines = x.split("webUrl")
        cleaner_headlines_list.append(cleaner_headlines[0])

    for x in cleaner_headlines_list:
        cleaner_headlines2 = x[3:-3] #removes first three and last three charaters from string
        clean_headlines_list.append(cleaner_headlines2)
    
    return clean_headlines_list

def daily_guardian_headlines(date, api_key):
    #uses the guardian api to return a selection of article titles from any given day
    r_business = requests.get('https://content.guardianapis.com/search?from-date=' + date + "&to-date=" + date + "&production-office=uk&section=business&page-size=50&&api-key=" + api_key)
    r_tech     = requests.get('https://content.guardianapis.com/search?from-date=' + date + "&to-date=" + date + "&production-office=uk&section=technology&page-size=50&&api-key=" + api_key)
    r_uknews   = requests.get('https://content.guardianapis.com/search?from-date=' + date + "&to-date=" + date + "&production-office=uk&section=uk-news&page-size=50&&api-key=" + api_key)
    business_headlines = guardian_headline_finder(r_business)
    tech_headlines = guardian_headline_finder(r_tech)
    uknews_headlines = guardian_headline_finder(r_uknews)
    headlines = business_headlines + tech_headlines + uknews_headlines
    return headlines

def nyt_headline_finder(date):
    #takes in date in string form, returning a list of the headlines for that day
    dirty_headlines_list = []
    cleaner_headlines_list = []
    clean_headlines_list = []
    clean_headlines_date = []
    final = []
    
    dates = date.split("-")
    year = int(dates[0])
    month = int(dates[1])
    day = int(dates[2])
    
    my_data_file = open('nyt_news_data/{}-{}.txt'.format(year,month), 'r')
    
    if (year==2018) & (month in [8,9,10,11,12]):
        results = my_data_file.read().split("web_url")
        
        matches = ['print_page":"1"','headline":{"main',"kicker", "pub_date"]

        for y in results:
            if all(x in y for x in matches):
                dirty_headlines_list.append(y)
        
    else:
        results = my_data_file.read().split("abstract")
    
        matches = ['print_section":"A","print_page":"1"','headline":{"main',"kicker", "pub_date"]

        for y in results:
            if all(x in y for x in matches):
                dirty_headlines_list.append(y)


    # extract the headline
    for x in dirty_headlines_list:
        cleaner_headlines2 = x.split('headline":{"main')
        cleaner_headlines3 = cleaner_headlines2[1]
        cleaner_headlines4 = cleaner_headlines3.split('kicker')
        cleaner_headlines5 = cleaner_headlines4[0]
        clean_headlines_list.append(cleaner_headlines5[3:-3])
           
    #extract the date published
    for x in dirty_headlines_list:
        cleaner_dates = x.split('pub_date')[1]
        cleaner_dates2 = cleaner_dates[2:22]
        clean_headlines_date.append(cleaner_dates2)
    
    #extract the headlines on the correct dates
    count = 0
    for x in clean_headlines_date:
        y = x.split('T')
        y = y[0][1:]
        if y == date:
            final.append(clean_headlines_list[count])
        count += 1
            
    return list(set(final))