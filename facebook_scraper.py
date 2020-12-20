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

post_links=[]
post_ids=[]
shares=[]
dates=[]
likes=[]
comments=[]

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

soup = BeautifulSoup(page_source, 'lxml')
section=soup.findAll('div',{'class':'_3drp'})
for a in section:

    link=a.find('a',attrs={'class':'_5msj'})
    post_link=link['href']
    part = post_link.split('&')[0]
    post_id=part.split('=')[1]
    print(post_link)
    print(post_id)
        
    
    date=a.find('abbr')
    like=a.find('div', attrs={'class':'_1g06'})
    if(len(like) == 0):
        like ="0 likes"
    comm_shar=a.findAll('span', attrs={'class':'_1j-c'})
    if(len(comm_shar[0])==0):
        comm_shar[0] ="0 comments"
    if(len(comm_shar[1])==0):
        comm_shar[1] ="0 shares"
    spanx=a.find('div',{'class':'_5rgt _5nk5 _5msi'})
    post_text=spanx.find('span')
    if(len(post_text)==0):
        post_text =" "
        
    texts.append(post_text.get_text(strip=True))
    likes.append(like.get_text(strip=True))
    dates.append(date.get_text(strip=True))
    comments.append(comm_shar[0].get_text(strip=True))
    shares.append(comm_shar[1].get_text(strip=True))

df=pd.DataFrame({'Text':texts,'dates':dates, 'like':likes, 'Comment':comments ,'Shares':shares })
df.to_csv('facebookscrapedata.csv', index=False, encoding='utf-8')