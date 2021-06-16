#import required libraries
import requests
from bs4 import BeautifulSoup

#URL - site of vacancies
URL = 'https://stackoverflow.com/jobs?q=python'


#get max page number
def extract_max_page():
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_pages = int(pages[-2].get_text(strip=True))
    
    return last_pages

#parsing the data on each page
def extract_job(html):
    title = html.find('h2').find('a').text 
    job_id = html['data-jobid']
    link = f'https://stackoverflow.com/jobs/{job_id}/'
    company = html.find('h3').find('span').get_text(strip=True)
    location = html.find('span', {'class': 'fc-black-500'}).text

    return {'title': title, 'company': company, 'location': location, 'link': link}


#filling an array with parsing data
def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page + 1):
        print(f'StackOverFlow: парсинг страницы {page}')
        result = requests.get(f'{URL}&pg={page}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


#collecting data from parsing
def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)

    return jobs

    