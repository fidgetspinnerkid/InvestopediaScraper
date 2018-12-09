"""
Andrew Huang

Purpose: Scrape the the trade histories from each of the players
of the game: Investopedia Game 2016 No End. Then output the trades
to an Excel file for further analysis.
"""
import requests
from requests.auth import HTTPBasicAuth
import re
from bs4 import BeautifulSoup
from openpyxl import Workbook
import datetime

# read the URLs in urlList.txt and output it to a list so it's easier to access
urlArray = []
f = open("urlList.txt")
line = f.readline()
while line != "":
    urlArray.append(line.strip())
    line = f.readline()
f.close()

# start browser/session
s = requests.session()

# get the HTML code of the url: http://www.investopedia.com/simulator/ranking/?page=1 using a GET request
url_to_scrape = 'http://www.investopedia.com/simulator/ranking/?page=1'
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

# send the dictionary of information to the webserver as a POST request
r = s.post(url_to_scrape, data=values)

# create a spreadsheet so that we can output it onto an excel later
wb = Workbook()
ws = wb.active

# loop through all the urls we have.
for x in range(1, 54757):
    # The timestamp allows us to estimate rate of scraping.
    print('Beginning to scrape user ' + x + '.')
    print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

    # once it finishes every twentieth person it saves
    if x % 20 == 0:
        wb.save("InvestopediaData.xlsx")
        print('Saved.')

    # get the URL of the person in rank x
    url = urlArray[x - 1]
    nextUrl = 'notblank'

    # check if the user has another page of Trade History
    while nextUrl != '':
        # get the HTML code of the URL of the player's Trade History using a GET request
        r = s.get(url)

        # parse the HTML with BeautifulSoup
        soup = BeautifulSoup(r.content, 'html.parser')

        # find the table with the user's Trade History
        Table = soup.find("table", {"class": "table1 bdr1 zebra"})
        try:
            for row in Table.find_all('tr'):

                # make an empty list that will be filled with a trade on the page of the Trade history
                histTrade = []

                # find all cells in the table's row
                cells = row.find_all('td')

                # check if the row is empty
                if len(cells) > 0:
                    for dp in cells:
                        # take the information from the cells
                        dataPiece = dp.text

                        # deletes the content between the parenthesis in the trades that have the parenthesis
                        dataPiece = re.sub("[\(].*?[\)]", "", dataPiece)
                        histTrade.append(dataPiece)

                # if the person did no trades, then do not output it onto the excel file
                if histTrade == []:
                    continue

                # if its an option then do not output it onto the excel file
                # this is because the options function on the simulator is not extremely accurate
                elif 'Option' in histTrade[1]:
                    continue

                else:
                    # if the trade is a sell or short, then append a "-1" to histTrade
                    # this determines the direction of the vote
                    if 'Sell' in histTrade[1] or 'Short' in histTrade[1]:
                        histTrade.append(-1)

                        # append the rank
                        histTrade.append(x)

                        # if it's not a short or sell, then it's a buy
                    # if the trade is a buy, then the vote is positive
                    else:
                        histTrade.append(1)
                        histTrade.append(x)

                    # Write the trade information, the positive or negative effect, and the rank to the
                    # excel file in a row.
                    ws.append(histTrade)

        # if there is an AttributeError, then skip the user. This likely occurs when the user leaves the game.
        except AttributeError:
            pass

        # check if there is a next page in the person's trade history
        nextUrl = ''
        for link in soup.find_all('a', href=True, text=' &gt; '):
            # write down the URL as the next page
            nextUrl = link['href']
        url = nextUrl

# Save the excel when all the data has been collected.
wb.save("InvestopediaData.xlsx")
