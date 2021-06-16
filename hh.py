#import required libraries
import requests
from bs4 import BeautifulSoup

'''
items - numbers of vacancies per page
URL - site of vacancies
headers - browser-mimicking parameters
'''
items = 100
URL = f'https://kazan.hh.ru/search/vacancy?&text=python&st=searchVacancy&items_on_page={items}'
headers = {
        'Host': 'hh.ru',
        'User-Agent': 'Safari',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

#get max page number
def extract_max_page():
    hh_req = requests.get(URL,
                        headers=headers)
    hh_soup = BeautifulSoup(hh_req.text, 'html.parser')
    pages = []
    paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
    for page in paginator:
        pages.append(int(page.find('a').text))
        
    return pages[-1]

#parsing the data on each page
def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class':"vacancy-serp-item__meta-info-company"}).find('a').text
    company = company.strip()
    location = html.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.split(',')[0]

    return {'title': title, 'company': company, 'location': location, 'link': link}

#filling an array with parsing data
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'HeadHunter: парсинг страницы {page}')
        result = requests.get(f'{URL}&page={page}', headers=headers)
        hh_soup = BeautifulSoup(result.text, 'html.parser')
        results = hh_soup.find_all('div', 
            {'class': 'vacancy-serp-item'}
            )
        for result in results:
            job = extract_job(result)
            jobs.append(job)
            
    return jobs

#collecting data from parsing
def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)

    return jobs