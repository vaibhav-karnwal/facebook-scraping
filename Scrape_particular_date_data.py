# importing pandas package 
import pandas as pd 
from credential import input_date, input_time

# making data frame from csv file  
df = pd.read_csv("facebook_scraped_post.csv") 

# replacing blank spaces with '_'  
df.columns =[column.replace(" ", "_") for column in df.columns] 
newdf=df.query('dates=="16 December " &Time==" 12:23"')

print(newdf)
