import csv
import requests
import concurrent.futures
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
links = []
first_names = ['FirstName']
last_names = ['LastName']
media_outlets = ['MediaOutlets']
current = 0

def scrape(site):
    data  = requests.get(site)
    soup = BeautifulSoup(data.text,'lxml')
    link = 'https://muckrack.com'
    link_data = soup.find_all('div',{"class":"mr-directory-item"})
    for i in link_data:#scraping links to profiles
        href = i.a.get('href')
        site = link + href
        links.append(site)

def scrape_details(site):
    media_outlet = []
    data = requests.get(site)
    soup = BeautifulSoup(data.text,'lxml')
    #finding name
    name = soup.find('h1',{'class':'profile-name mr-font-family-2 top-none'}).text.strip()
    first_names.append(name.split()[0])
    last_names.append(name.split()[1])
    #finding media Outlet
    media_outlet_raw = soup.find_all('li',{"class":"mr-person-job-item"})
    for i in media_outlet_raw:
        media_outlet.append(i.text.strip())
    media_outlets.append(media_outlet)

    # details = zip(first_names,last_names,media_outlets)
    print(len(first_names)) #ToShowProgress
    # return details


def print_result(d):
    longest = len(max(d,key = len))
    for key,value in d.items():
        print(f"{key}{(longest - len(key))*' '}: {value}")

def return_csv(*args):
    rows = zip(*args)
    with open('datafile.csv','w+') as f:
        f_writer = csv.writer(f)
        for row in rows:
            f_writer.writerow(row)

def write_csv(links):
    with open('links.csv','w+') as f:
        f_writer  = csv.writer(f)
        for link in links:
            f_writer.writerow([link])

def import_urls(file_name):
    with open(f'{file_name}.csv','r+') as f:
        f_reader = csv.reader(f)
        for row in f_reader:
            links.append(row[0])

if __name__ == '__main__':
    try:
        import_urls(file_name='links')
    except:
        page_urls = [f'https://muckrack.com/beat/food?page={x}' for x in range(1,101)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(scrape,page_urls)
        write_csv(links)  
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(scrape_details,links)
    except:
        return_csv(first_names,last_names,media_outlets)
    else:
        return_csv(first_names,last_names,media_outlets)