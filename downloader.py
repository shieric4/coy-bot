import pandas as pd
import requests
from titlecase import titlecase

from bs4 import BeautifulSoup

import files as fln
from shared.drive import drive as drv
from shared.drive import pickles as pkl

surl = 'http://scripts.jakeandamir.com/index.php?search=:&from-date=&to-date=&do-search=1'

def getSoup(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def init():
    if drv.exist(fln.fDataframe) == False:
        link = "https://www.youtube.com/results?search_query=jake+and+amir+%s"
        titles = []
        links = []
        scripts = []
        soup = getSoup(surl)
        for script in soup.findAll("div", {"class": "episode-script-inner"}):
            scripts.append(str(script.text).replace('...', '⋯').replace('..', '⋯'))
        for title in soup.findAll("td", { "class" : "header-inner-title"}):
            titles.append(titlecase(title.text))
            links.append(link % str(title.text).replace(' ', '+'))
        archive = pd.DataFrame({'Title': titles, 'Link': links, 'Script': scripts})
        archive = archive.replace('[\t]+', '', regex=True)
        archive = archive.replace('[\r]+', '', regex=True)
        pkl.save(fln.fDataframe, archive)
    df = pkl.load(fln.fDataframe)
    return df