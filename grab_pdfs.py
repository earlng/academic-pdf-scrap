import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import os

#Grab all the links in this directory
URL="https://proceedings.neurips.cc/paper/2020"

http = httplib2.Http()
status, response = http.request(URL)

papers=[]

#will go through the URL, and output list "papers" of the PDF links
for link in BeautifulSoup(response,"html.parser", parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        #print(link['href'])
        identifier=link['href']
        identifier=identifier.replace("Abstract.html", "Paper.pdf")
        identifier=identifier.replace("hash", "file")
        full_url="https://proceedings.neurips.cc"+identifier
        papers.append(full_url)

#delete first 3 entries in the papers, and last one because they are not good.
del papers[:3]
del papers[-1]

subdirectory="pdfs"

for link in papers:
    name = link.rsplit('/',1)[1]
    full_path = os.path.join(subdirectory, name)
    r = requests.get(link, allow_redirects=True)
    open(full_path, 'wb').write(r.content)