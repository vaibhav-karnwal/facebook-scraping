# importing pandas package 
import pandas as pd 
from credential import input_date, input_time

# making data frame from csv file  
data = pd.read_csv("facebook_scraped_post.csv") 
print(data) 
# replacing blank spaces with '_'  
data.columns =[column.replace(" ", "_") for column in data.columns] 
  
print(data)