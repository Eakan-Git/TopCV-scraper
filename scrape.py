import requests
import time
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import sys
import json

# Set headers and timeout
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
timeout = 10

# A function to save unhandled job links to a text file
def append_unhandled_job_link(job_link):
    with open("unhandled_job_links.txt", "a+") as f:
        f.write(job_link + "\n")
# A function to save company links to a text file
def append_company_link(company_link):
    with open("company_links_intern.txt", "a+") as f:
        f.write(company_link + "\n")
# A function to append/write data to a json file
def append_to_json(data):
    with open("jobs_data_intern.json", "a+", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# A recursive function to extract all the content from a job description
def extract_content(element):
    content = []
    children = element.find_all(recursive=False)
    for child in children:
        if child.name == "p":
            strong_tags = child.find_all(["strong", "b", "i", "em", "u"])
            if len(strong_tags) == 1 and not child.find(string=False):
                text = strong_tags[0].get_text().strip()
                if text:
                    content.append(text)
            else:
                text_blocks = list(child.stripped_strings)
                text_blocks = [block.strip() for block in text_blocks if block.strip()]
                content.extend(text_blocks)
        elif child.name == "ul":
            list_items = child.find_all("li")
            for item in list_items:
                text = item.get_text().strip()
                if not text.startswith("•"):
                    text = "• " + text
                if text:
                    content.append(text)
        elif child.name in ["div", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "br"]:
            text = child.get_text().strip()
            if child.name != "style" and text:
                content.append(text)
        else:
            content.extend(extract_content(child))
    return content


def extract_job_details(soup):
    # Data will be stored in a dictionary
    # for saving to a json file later
    job_details = {}
    company_overview = {}
    ###
    ### Variables to scrape
    ###
    job_title = soup.find("h1").get_text().strip()
    print(job_title, "\n")
    job_details['title'] = job_title
    ###
    company_title = soup.find("div", {"class": "company-title"}).get_text().strip()
    company_overview['company_title'] = company_title
    ###
    company_link = soup.find("div", {"class": "company-title"}).find("a")['href']
    company_overview['company_link'] = company_link
    ###
    company_logo = soup.find("div", {"class": "box-header"}).find("img")['src']
    company_overview['company_logo'] = company_logo
    ###
    job_details['company_overview'] = company_overview
    ###
    job_overview = {}
    box_items = soup.find("div", {"class": "box-main"})
    if box_items is not None:
        box_items = box_items.find_all("div", {"class": "box-item"})
        for item in box_items:
            spans = item.find_all("span")
            key = spans[0].get_text().strip()
            value = spans[1].get_text().strip()
            job_overview[key] = value
    job_details['job_overview'] = job_overview
    ###
    address = soup.find("div", {"class": "box-address"})
    if address is not None:
        address = address.find("div", {"style": "margin-bottom: 10px"}).get_text().strip().lstrip("- ")
    job_details['address'] = address
    ###
    job_categories = []
    categories = soup.find("div", {"class": "keyword"})
    if categories is not None:
        categories = categories.find_all("a")
        for category in categories:
            category_text = category.get_text().strip()
            job_categories.append(category_text)
            # print(category_text)
    job_details['job_categories'] = job_categories
    ###
    required_skills = []
    skills = soup.find("div", {"class": "skill"})
    if skills is not None:
        skills = skills.find_all("a")
        for skill in skills:
            skill_text = skill.get_text().strip()
            required_skills.append(skill_text)
            # print(skill_text)
    job_details['required_skills'] = required_skills
    ###
    job_areas = []
    area = soup.find("div", {"class": "area"})
    if area is not None:
        area = area.find_all("a")
        for a in area:
            job_areas.append(a.get_text().strip())
    job_details['job_area'] = job_areas
    ###
    deadline_soup = soup.find("div", {"class": "job-deadline"})
    deadline = ""
    if deadline_soup is not None:
        deadline_soup = deadline_soup.get_text().strip()
        # find index of ":"
        index = deadline_soup.find(":")
        # get the date
        deadline = deadline_soup[index+1:].strip()
        ###
    job_details['deadline'] = deadline
    ###
    job_description = {}
    description_soup = soup.find("div", {"class": "job-data"})
    if description_soup is not None:
        h3s = []
        h3s_soup = description_soup.find_all("h3")
        for h3 in h3s_soup[:3]:
            h3s.append(h3.get_text().strip())

        tabs = description_soup.find_all("div", {"class": "content-tab"})
        content_of_tabs = []

        for tab in tabs:
            content = extract_content(tab)
            content_of_tabs.append(content)

        for i in range(min(len(h3s), len(content_of_tabs))):
            job_description[h3s[i]] = content_of_tabs[i]
    job_details['job_description'] = job_description
    ###
    return job_details, company_link

# A function to scrape a job from a job link
def scrape_job_details(url):
    response = requests.get(url, headers=headers, timeout=timeout)
    # Check if request was successful then proceed to scrape every job
    if response.status_code == 200:
        # Create a BeautifulSoup object from the response
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            # Normal job link
            if url.startswith("https://www.topcv.vn/viec-lam/") and url != "https://www.topcv.vn/viec-lam/":
                job_details, company_link = extract_job_details(soup)
                append_to_json(job_details)
                append_company_link(company_link)
            else:
                append_unhandled_job_link(url)
        except:
            print("Error: Cannot scrape:", url, "\n")
            return
    else:
        # Print error message if request was unsuccessful
        print(f"Error: {response.status_code}")


# A function to count the number of pages
def find_num_of_pages(url):
    # Get the response from the url
    response = requests.get(url, headers=headers, timeout=timeout)
    # Check if request was successful then proceed to scrape every job
    if response.status_code == 200:
        # Create a BeautifulSoup object from the response
        soup = BeautifulSoup(response.text, "html.parser")
        # h3 = soup.find("div", {"class": "title-block"}).find("h3").get_text().strip()
        # print(soup)
        # Find the last number of class pagination
        pagination = soup.find("ul", {"class": "pagination"})
        # print(pagination)
        # checker = soup.find("span", id='job-listing-paginate-text')
        # print(checker)
        # if checker is None:
        last_number = int(pagination.find_all("a")[-2].get_text())
        # else:
        #     checker = checker.get_text().strip()
        #     # find index of "/"
        #     index = checker.find("/")
        #     # get the number of pages
        #     last_number = int(checker[index+1:].strip())
        # Print the number of pages found
        print(f"====================== FOUND {last_number} PAGES ======================")
        # Return the number of pages
        return last_number
    else:
        # Print error message if request was unsuccessful
        print(f"Error: {response.status_code}")

# A function to save job links before scraping job details
def cache_job_link(url):
    with open("job_links_intern.txt", "a+") as file:
        file.write(url + "\n")
# A function to scrape all job links from a page
def scrape_links_from_pages(url):
    # Get the response from the url
    response = requests.get(url, headers=headers, timeout=timeout)
    # Check if request was successful then proceed to scrape every job
    if response.status_code == 200:
        try:
            # Create a BeautifulSoup object from the response
            soup = BeautifulSoup(response.text, "html.parser")
            # Get all box-header elements
            box_headers = soup.find_all("div", {"class": "box-header"})
            print(f"Found {len(box_headers)} job links")
            # For each box-header element, get the job link
            job_links = []
            for box_header in box_headers:
                job_link = box_header.find("a")['href']
                job_links.append(job_link)
        except:
            print("Error: Cannot scrape {url}}")
            return
        if len(job_links) > 0:
            print("Caching job links...")
            for job_link in job_links:
                cache_job_link(job_link)
        else:
            print("No job link found")
            return;
    else:
        # Print error message if request was unsuccessful
        print(f"Error: {response.status_code}")

# A function to get all job links from the cache file
def get_job_links_from_cache():
    with open("job_links_intern.txt", "r") as file:
        job_links = file.readlines()
        job_links = [job_link.strip() for job_link in job_links]
    return job_links
# A function to get all company links from the cache file
def get_company_links_from_cache():
    with open("company_links.txt", "r") as file:
        company_links = file.readlines()
        company_links = [company_link.strip() for company_link in company_links]
    return company_links
def append_company_data(company_data):
    with open("company_data.json", "a+") as file:
        json.dump(company_data, file, indent=4, ensure_ascii=False)
        file.write("\n")
##
# def scrape_company_details(url):
#     soup = BeautifulSoup(requests.get(url, headers=headers, timeout=timeout).text, "html.parser")
#     company_data = {}
#     # Get company name
#     company_name = soup.find("h1", {"class": "company-name"})
#     if company_name is None:
#         company_name = soup.find("h1", {"class": "company-detail-name"})
#     if company_name is not None:
#         company_name = company_name.get_text().strip()
#         company_data["company_name"] = company_name
    


# Main function
def main():
    # Set default url
    # base_url = 'https://www.topcv.vn/viec-lam-it'
    base_url = 'https://www.topcv.vn/tim-viec-lam-thuc-tap-t5'
    # Get the url from the command line argument if there is any
    # if len(sys.argv) > 1:
    #     base_url = sys.argv[1]
    # # Get the max page number from the command line argument if there is any
    # if len(sys.argv) > 2:
    #     number_of_page = int(sys.argv[2])
    # else:
    #      # Count the number of pages
    #     number_of_page = find_num_of_pages(base_url)
    number_of_page = 35;
    # Scrape all job links from all pages
    for page in range(1, number_of_page):
        # Set the url for each page
        url = f'{base_url}?page={page}'
        # print(url)
        scrape_links_from_pages(url)
        # Print number of pages and jobs scraped
        # print(f"====================== SCRAPED {page*50} JOBS IN {number_of_page*50} JOBS ======================")
    # # get all job links from file
    job_links = get_job_links_from_cache()
    # job_links = job_links[1185:]
    # Scrape all job details from all job links
    for job_link in job_links:
        scrape_job_details(job_link)
        # sleep for 1 second
        time.sleep(3)
        # Print number of pages and jobs scraped
        print(f"====================== SCRAPED {job_links.index(job_link)+1} JOBS IN {len(job_links)} JOBS ======================")
    # get all company links from file
    # company_links = get_company_links_from_cache()
    # drop all duplicates using pd
    # company_links = pd.unique(company_links).tolist()
    # Scrape all company details from all company links
    # for company_link in company_links:
    #     try:
    #         scrape_company_details(company_link)
    #     except:
    #         print("Error: Cannot scrape {company_link}")
    #     # sleep for 1 second
    #     time.sleep(3)
    #     # Print number of pages and jobs scraped
    #     print(f"====================== SCRAPED {company_links.index(company_link)+1} COMPANIES IN {len(company_links)} COMPANIES ======================")

# Run the main function
if __name__ == "__main__":
    main()