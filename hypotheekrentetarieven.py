#based on source:https://github.com/Jeroenvanbennekom/Hypotheekscraper
from bs4 import BeautifulSoup
import requests
import time 
import pandas as pd
#import numpy as np

#looptijden = ("1", "2", "3", "5", "6", "7", "10", "12", "15", "17", "20", "25", "30")
looptijden = ("5", "7", "10", "15", "17", "20", "30")

#Stel een wachtperiode in
delay = 0.2

def scrape_hypotheekrentetarieven():
	lst = []
	for looptijd in looptijden:
		results = scrape_script_fixed_period(looptijd)
		df = pd.DataFrame(results,columns=['hypotheker','nhg','60%','80%','90%','100%'])
		df['looptijd'] = looptijd
		lst.append(df)
	df_all = pd.concat(lst)
	return(df_all)

def scrape_script_fixed_period(looptijd):
	try:
		data_lst = []
		#Scrape results for all fixed looptijden. 
		url = f"https://www.hypotheekrente.nl/rente/{looptijd}-jaar-rentevast/nhg/#overzicht"
		page_fetch = requests.get(url, timeout = 5)
		page_content = BeautifulSoup(page_fetch.content, "html.parser")
		rows = page_content.find_all('tr')
		for row in rows:
			cols=row.find_all('td')
			cols=[x.text.strip() for x in cols]
			cols=[float(x[:-1]) if x.endswith('%') else x for x in cols ]
			#print(cols)
			#Add only rows with a column for all tariffs and name of the 'verstrekker'. This is to filter empty rows and adverts. 
			if len(cols)==8:
				data_lst.append(cols[1:7])
		#Sleep for 1.x seconds to avoid overstressing server		
		time.sleep(delay)
		return(data_lst) 
	except Exception as e:
		print('Something went wrong with scraping for fixed period. Fix it',e)

#scrape_hypotheekrentetarieven()