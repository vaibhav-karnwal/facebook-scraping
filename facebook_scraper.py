import argparse
import time
import json
import csv
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
from requests_html import HTMLSession, HTML
from lxml.etree import ParserError
from credential import username, password, email 

#list of elements to scrape
post_links=[]
post_ids=[]
shares=[]
dates=[]
times=[]
likes=[]
comments=[]
texts=[]

#function to scroll from 0 position to end position
def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        time.sleep(.5)

        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

#calling chrome driver to login
driver = webdriver.Chrome()
driver.get(f"https://m.facebook.com/{username}/")
driver.find_element_by_css_selector("a._4n43").click()
time.sleep(2)
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("pass").send_keys(password)
driver.find_element_by_name("login").click()
       
time.sleep(1)

scroll_to_bottom(driver)

page_source = driver.page_source

#scraping html page data 
soup = BeautifulSoup(page_source, 'lxml')
section=soup.findAll('div',{'class':'_3drp'})
for a in section:

    #for scraping post link and id
    link=a.find('a',attrs={'class':'_5msj'})
    post_link=link['href']
    part = post_link.split('&')[0]
    post_id=part.split('=')[1]
    post_links.append(post_link)
    post_ids.append(post_id)
    
    #for scraping date and time of post
    post_date=a.find('abbr')
    post_data=post_date.get_text(strip=True).split('at')
    date=post_data[0]
    time=post_data[1]
    dates.append(date)
    times.append(time)
    
    #for scraping like of post
    like=a.find('div', attrs={'class':'_1g06'})
    if(len(like) == 0):
        like ="0 likes"
    likes.append(like.get_text(strip=True))
     
    #for scraping text of post
    text=a.find('div',{'class':'_5rgt _5nk5 _5msi'})
    post_text=text.find('span')
    if(len(post_text)==0):
        post_text =" "   
    texts.append(post_text.get_text(strip=True))

    #for scraping comment and share of post
    comm_shar=a.findAll('span', attrs={'class':'_1j-c'})
    comments.append(comm_shar[0].get_text(strip=True))
    shares.append(comm_shar[1].get_text(strip=True))
    
    
#Appending all the list data to a pd dataframe 
df = pd.DataFrame({'dates':dates,'Time':times,'Post Links':post_links,'Post Ids':post_ids,'Text':texts,'like':likes,'Comment':comments ,'Shares':shares})

#converting pd raw data to csv file 
df.to_csv('facebook_scraped_post.csv', index=False, encoding='utf-16')

  
