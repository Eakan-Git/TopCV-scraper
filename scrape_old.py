import requests
import time
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import sys

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
timeout = 10

def scrape_job(job_link):
	job_response = requests.get(job_link, headers=headers, timeout=timeout)
	if job_response.status_code != 200:
		print(f"Error: {job_response.status_code}")
	else:
		job_soup = BeautifulSoup(job_response.text, "html.parser")
		#print(job_soup)
		job_title = job_soup.find("h1", {"class": "job-title"}).get_text().replace('\n','')
		company_title = job_soup.find("div", {"class": "company-title"}).find("a").get_text()
		company_logo_link = job_soup.find("div", {"class": "box-company-logo"}).find("img")['src']
		# Get Job Info
		boxes = job_soup.find("div", {"class": "box-main"})
        # print(boxes)
		infos = boxes.find_all("div", {"class": "box-item"})
		info_data = []
		for info in infos:
			tmp = []
			title_info = info.find("strong").text.strip()
			detail_info = info.find("span").text.strip()
			tmp.append(title_info)
			tmp.append(detail_info)
			info_data.append(tmp)
		info_data = {item[0]: item[1] for item in info_data}
		deadline = job_soup.find("div", {"class": "job-deadline"}).text.strip()[-10:]
		list_address = job_soup.find("div", {"class": "box-address"}).find_all("div", {"style": "margin-bottom: 10px"})
		addresses = []
		for address in list_address:
			addresses.append(address.text.strip()[2:])
		skills_soup = job_soup.find("div", {"class": "skill"})
		skills_data = []
		if skills_soup is not None:
			skills = skills_soup.find_all("a")
			for skill in skills:
				skills_data.append(skill.text.strip())
		company_details_soup = job_soup.find("div", {"class": "box-info-company box-white"})
		company_link = company_details_soup.find("a", {"href": True}).get("href")
		box_items = company_details_soup.find("div", {"class": "box-info"}).find_all("div", {"class": "box-item"})
		company_data_titles = []
		company_data_contents = []
		company_data = []
		for item in box_items:
			title = item.find("p", {"class": "title"}).text.strip()
			content = item.find("span", {"class": "content"}).text.strip()
			company_data_titles.append(title)
			company_data_contents.append(content)
		company_data = dict(zip(company_data_titles, company_data_contents))
		job_data_soup = job_soup.find("div", {"class": "job-data"})
		job_data_h3_text = []
		job_data_h3 = job_data_soup.find_all("h3")
		for job_data_h3_item in job_data_h3:
			job_data_h3_text.append(job_data_h3_item.text.strip())
		job_data_h3_text = job_data_h3_text[:-1]
		job_data_content_text = []
		job_data_contents = job_data_soup.find_all("div", {"class": "content-tab"})
		for item in job_data_contents:
			job_data_content_text.append(item.text.strip().replace('\u00a0', '').replace('\u200b', '') + " ")
		# jd = {}
		# for job_data in job_data_soup:
		# 	job_detail_titles = job_detail.find("h2", {"class": "detail-title"}).text.strip()
		# 	job_details_contents = [re.sub('\s+', ' ', p.text.replace('\u00a0', '').replace('\u200b', '')).strip() for p in job_detail.find_all("p")]
		# 	jd[job_detail_titles] = job_details_contents
		# job_details = []
		job_details = dict(zip(job_data_h3_text, job_data_content_text))
		# delimiters = r'[+-•]'
		# for key, value in job_details.item():
		# 	contents = re.split(delimiters, value)
		# 	contents = [contents.strip() for content in contents if contents.strip()]
		# 	job_details[key] = contents
		# job_data = []
		# job_data.append({
		# 	'title': job_title,
		# 	'job_link': job_link,
		# 	'company_link': company_link,
		# 	'company': company_title,
		# 	'deadline': deadline,
		# 	'overview': info_data,
		# 	'addresses': addresses,
		# 	'skills': skills_data,
		# 	'job_details': job_details
		# })
		#print(job_data)
		fieldnames = ["title", "job_link", "company_link", "company", "deadline", "overview", "addresses", "skills", "job_details"]

		with open('jobs_data.csv', mode='a', newline='', encoding='utf-8') as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			if f.tell() == 0:
				writer.writeheader()
			writer.writerow({'title': job_title, 'job_link': job_link, 'company_link': company_link, 'company': company_title, 'deadline': deadline, 'overview': info_data, 'addresses': addresses, 'skills': skills_data, 'job_details': job_details})
		print(job_title)

def scrape(url):
	# Make a request to the website
	response = requests.get(url, headers=headers, timeout=timeout)

	# Check if the request was successful
	if response.status_code == 200:
		soup = BeautifulSoup(response.text, "html.parser")
		lists = soup.find("div", {"class": "job-list-default"})
		if lists is None:
			lists = soup.find("div", {"class": "job-list-2"})
		jobs = lists.find_all("div", {"class": "job-item-default"})
		if jobs is None:
			jobs = lists.find_all("div", {"class": "job-item-2"})
		for job in jobs:
			job_link = job.find("h3", {"class": "title"}).find("a").get("href")
			#print(job_link)
			if job_link.startswith("https://www.topcv.vn/viec-lam/") and job_link != "https://www.topcv.vn/viec-lam/":
				try:
					scrape_job(job_link)
				except:
					print(f"Failed to scrape the job! - {job_link}")

def clean_up():
	df = pd.read_csv('jobs_data.csv')
	df.drop_duplicates().to_csv("jobs_data.csv", index=False)

def main():
	args = sys.argv[1:]
	if len(args) == 2 and int(args[0]) <= int(args[1]):
		url = 'https://www.topcv.vn/tim-viec-lam-moi-nhat'
		page = int(args[0])
		flag = int(args[1])
		print(f"======================Start scraping from page 1 to page {flag}.======================")
		while True:
			if page > flag:
				break
			scrape(url + f'?page={page}')
			print(f'Scraped page: {page}')
			page += 1
			time.sleep(3)
		clean_up()
		print("Done!")
		return
	if len(args) == 0:
		url = 'https://www.topcv.vn/tim-viec-lam-moi-nhat'
		page = 1
		page_response = requests.get(url, headers=headers, timeout=timeout)
		page_soup = BeautifulSoup(page_response.text, "html.parser")
		flag = int(page_soup.find("ul", {"class":"pagination"}).find_all("li")[-2].text)
		print(f"======================Start scraping from page 1 to page {flag}.======================")
		while True:
			if page > flag:
				break
			scrape(url + f'?page={page}')
			print(f'Scraped page: {page}')
			page += 1
			time.sleep(3)
		clean_up()
		print("Done!")
		return
	else:
		print("Wrong arguments")

main()