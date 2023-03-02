import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import re
import csv

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
timeout = 10


def extract_companies_data():
	try:
		df = pd.read_csv('jobs_data.csv')
		column_name=['company_link']
		pd.DataFrame(df.company_link.unique()).to_csv("company_link.csv", index=False, header = column_name)
	except:
		print("Error while trying to create file.")

def scrape_companies_data():
	dfc = pd.read_csv('company_link.csv')
	for link in dfc.company_link:
		response = requests.get(link, headers=headers, timeout=timeout)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, "html.parser")
			try:
				name = soup.find("h1", {"class": "company-detail-name"}).text
			except:
				continue
			try:
				website = soup.find("p", {"class": "website"}).find("a").get("href")
			except:
				website = ""
			try:
				size = soup.find("p", {"class": "company-size"}).text.strip()[:-10]
			except:
				size = -1
			try:
				description_soup = soup.find("div", {"class": "company-info box-white"}).find("div", {"class": "box-body"})
				#p_tags = description_soup.find_all("p")
				description = [re.sub('\s+', ' ', p.text.replace('\u00a0', '').replace('\u200b', '')).strip() for p in description_soup.find_all("p")]
				#print(description_soup)
			except:
				description = "x"
			try:
				address_soup = soup.find("div", {"class": "box-address box-white"}).find_all("p", {"class": "text-dark-gray"})
				addresses = [p.text.strip() for p in address_soup]
			except:
				addresses = []
			# data = {'name': name,
			# 		'website': website,
			# 		'size': size,
			# 		'description': description,
			# 		'addresses': addresses
			# }
			# dfd = pd.DataFrame(data)
			fieldnames = ['name', 'website', 'size', 'description', 'addresses']
			# dfd.to_csv('companies_data.csv', index=False)
			with open('companies_data.csv', mode='a', newline='', encoding='utf-8') as f:
				writer = csv.DictWriter(f, fieldnames=fieldnames)
				if f.tell() == 0:
					writer.writeheader()
				writer.writerow({'name': name, 'website': website, 'size': size, 'description': description, 'addresses': addresses})
			print(name)
			
def clean_up():
	df = pd.read_csv('companies_data.csv')
	df.drop_duplicates().to_csv("companies_data.csv", index=False)

extract_companies_data()
scrape_companies_data()
clean_up()