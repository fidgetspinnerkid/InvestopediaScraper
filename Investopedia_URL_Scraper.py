"""
Andrew Huang

Purpose: Scrape the Investopedia Game 2016 No End Rankings pages for the
URLs of each player's trade history and output the URLs onto a text file.
"""
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# these are the urls that we will be requesting with the requests module requests
url_to_scrape = 'http://www.investopedia.com/simulator/ranking/?page=1'

# start browser
s = requests.session()

# get the HTML code of the url: http://www.investopedia.com/simulator/ranking/?page=1 using a GET request
r = s.get(url_to_scrape)

# parse the HTML with BeatifulSoup
soup = BeautifulSoup(r.content)

# Find the form_build_id in the HTML we got from the GET request
form_build_id = ''
for input1 in soup.find_all(name="form_build_id"):
    form_build_id = input1['value']

# My information for login
values = {'email': 'huangandrew6@gmail.com',
          'password': 'password',
          'form_build_id': form_build_id,
          'form_id': 'account_api_form',
          'op': 'Sign in'}

# send the dictionary of information to the webserver as a post
r = s.post(url_to_scrape, data=values)

# make a blank text file that we will fill with the URLs of the players' trade history
outFile = open('urlList.txt', 'w')

# All the players from page 745 to page 2878 were inactive
# Iterate through the first 744 pages of the rankings, we will skip the inactive people in the middle
for x in range(1, 745):
    # Go to pages 1 to 744 in the rankings
    url = 'http://www.investopedia.com/simulator/ranking/?page=' + str(x)

    # Send a get request for the page of rankings to the webserver
    r = s.get(url)

    # Parse the HTML we get from the server
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all tags that look like this: <a href=".............">(history)</a>
    for link in soup.find_all('a', href=True, text='(history)'):
        # write the links(the href) in the tags into the textfile urlList.txt
        outFile.write(link['href'] + '\n')

# Iterate through pages 2879 to 3232
for x in range(2879, 3233):
    # Go to pages 2879 to 3232 in the rankings
    url = 'http://www.investopedia.com/simulator/ranking/?page=' + str(x)

    # Send a get request for the page of rankings to the webserver
    r = s.get(url)

    # Parse the HTML we get from the server
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all tags that look like this: <a href=".............">(history)</a>
    for link in soup.find_all('a', href=True, text='(history)'):
        # write the links(the href) in the tags into the textfile urlList.txt
        outFile.write(link['href'] + '\n')
