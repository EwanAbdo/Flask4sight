import csv
import requests
from bs4 import BeautifulSoup
import PyPDF2
from collections import Counter
import sys

def read_resume(path):
    """this function reads a pdf resume/CV and searches for the most frequently mentioned skill

    Args:
        path (string): path to resume

    Returns:
        top_skills: a list of strings ordered according most repeated skills in the resume
    """
    # Read the PDF file
    pdf_file = open(path, 'rb') #./Website/my_resume.pdf
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract the text from the PDF file
    resume_text = ''
    for page in range(len(pdf_reader.pages)):
        resume_text += pdf_reader.pages[page].extract_text()

    # Get the text from the skills section of the resume
    skills_section = resume_text[resume_text.find('Skills'):]#:resume_text.find('Education')

    # Get the most frequently mentioned skills from the skills section
    words = skills_section.split()
    word_counts = Counter(words)
    top_skills = [skill for skill, count in word_counts.most_common(10) if len(skill) > 3]
    return top_skills

def linkedin_scraper(webpage, page_number,filename=None):
    """this function scraps linkedIn given a webpage consiting of a job keyword and a location

    Args:
        webpage (string): search url
        page_number (integer): the page number in the search results
        filename (string, optional): the output file name where the results are written. Defaults to None.

    Returns:
        filename (string, optional): the output file name where the results are written
    """
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content,'html.parser')
 
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link')['href']
 
        writer.writerow([
        job_title,
        job_company,
        job_location,
        job_link
        ])
 
        print('Data updated')
 
    if page_number < 25:
        page_number = page_number + 25
        linkedin_scraper(webpage, page_number,filename=filename)
    else:
        file.close()
        print('File closed')
    return filename

if  __name__== '__main__':
    resume_path = sys.argv[1]
    top_skills= read_resume(resume_path)
    city = sys.argv[2]
    city1 = city.replace(',','')
    filename = 'linkedInFinal-' + top_skills[0] + '-' + city1.replace(' ','') +'.csv'
    file = open(filename, 'a',encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['Title', 'Company', 'Location', 'Apply'])
    url = 'https://www.linkedin.com/jobs/search?keywords='+ '%20'.join(top_skills[0])+'&location='+'%20'.join(city) + '&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='
    linkedin_scraper(url, 0, filename=filename)