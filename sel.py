from six.moves.urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import re


def scrape(query):
    query=query.strip().split()
    query="+".join(query)
    html = "https://www.google.co.in/search?site=&source=hp&q="+query+"&gws_rd=ssl"
    req = urllib.request.Request(html, headers={'User-Agent': 'Mozilla/5.0'})
    
    soup = BeautifulSoup(urlopen(req).read(),"html.parser")
    
    #Regex
    reg=re.compile(".*&sa=")
    
    links = []
    #Parsing web urls
    for item in soup.find_all('h3', attrs={'class' : 'r'}):
        #print(item)
        if item.a:
            line = (reg.match(item.a['href'][7:]).group())
            links.append(line[:-4])
    return links



query=input("Query>>")
links = scrape(query)
print(links)

options = webdriver.ChromeOptions()
options.add_argument('headless')
# start chrome browser
browser = webdriver.Chrome(executable_path = './Chrome/chromedriver', options=options)

article_text = []
final_links = []

for l in links:
    try:
        browser.get(l)
        soup = BeautifulSoup(browser.page_source, "lxml")
        paragraphs = soup.find_all('p')
        #print(paragraphs)
        content = ""
        for p in paragraphs:
            content += p.text
        #print(content)
        article_text.append(content)
        final_links.append(l)
        print(l)
    except:
        print("Blocked :(")
#print(final_links)

browser.quit()
