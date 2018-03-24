# Coded by TheSpaceCowboy
# Date: 24/11/17
# Github: https://github.com/thespacecowboy42534

#Imports
import bs4 
from  urllib.request import Request,urlopen
from urllib.parse import quote_plus
import urllib
import random
from bs4 import BeautifulSoup as soup

def searchResults(term, it = "def"): # Searches gfycat for the name of the anime
    term = quote_plus(term)
    url = "https://gfycat.com/gifs/search/"+term# Looks for the gif by a given name

    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # Requests the page using a false header because scraping 403's
    client = urlopen(request) # Opens a connection to the page
    html = client.read() # Reads the html and stores it as html
    client.close() # Closes connection to save memory

    page_soup = soup(html,"html.parser") # Uses soup to parse the html data
    p = page_soup.findAll("div",{"class":"infinite-grid-item"}) # Finds every gif
    if(it == "def"):
       it = random.randint(0,len(p))# Returns random link
    else:
       pass # Uses specified result
    if(len(p) > 0):
        return p[it].img["src"] # Finds the image



