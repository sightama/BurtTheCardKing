
# coding: utf-8

# In[112]:


import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json
import warnings
warnings.filterwarnings(action='once')

'''
Example format for extraction:
Count | Card Name | (Set# Card#)

2 Trail Stories (Set1 #188)
4 Horus Traver (Set1002 #23)
4 Longbarrel (Set4 #5)
4 On the Hunt (Set2 #5)
4 Oni Dragonsmith (Set1003 #2)
'''


# # First step: Login and extract collection fully from eternal warcry.

# ## Note: Remove user/pass lane later!

# In[113]:


"""
For those paying attention mechanize is python 2.x only, someone made mechanicalsoup
(Love you), which if you read the tutorial we give you a brief intro along with show you how
to login. This is compatible /w python 3.6. The code below takes in two command
line parameterse delimited by a space; username password.

ie: aggregate_card_json.py <username> <password>

For now I have my u+p information manually punched in and works!
"""

# import argparse
# parser = argparse.ArgumentParser(description="Login to EternalWarcry.")
# parser.add_argument("username")
# parser.add_argument("password")
# args = parser.parse_args()
user = '<user>'
passwd = '<pass>'

import mechanicalsoup

browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'})

# request eternalWarcry login page. the result is a requests.Response object
login_page = browser.get("https://eternalwarcry.com/login")

# login_page.soup is a BeautifulSoup object

# we grab the login form
login_form = mechanicalsoup.Form(login_page.soup.select_one('form[action="/login"]'))

# specify username and password
login_form.input({"LoginEmail": user, "LoginPassword": passwd})# REPLACE WITH args.username & args.password
# submit form
page2 = browser.submit(login_form, login_page.url)
# Verify we logged in at Eternal Warcry...
print(page2.soup.title.text)









"""
STEP TWO: ITERATE THROUGH EACH PAGE AND GRAB ALL OF THE INFORMATION FOR EACH CARD,
PUT IT INTO A STRING IN THE PRETTY FORMAT THAT ETERNAL FOLLOWS, AND APPEND INTO A BIG LIST
OUTPUT WHICH IS YOUR COLLECTION FROM ETERNALWARCRY
(All this really does is save you time by not having to go into ->"Deck Builder" and
add ALL your cards to a deck and exporting it.... :))
"""
page_num = 1
check_last_pg = re.compile(r'\b(No cards found in your collection)\b')
final_collection = []

while True:
    # Now that were logged in pull each link for our collection and grab the info
    current_page = 'https://eternalwarcry.com/collection?view=oo&p=' + str(page_num)
    page_num = page_num + 1 # Iterate don't wanna forget ;)
    collection_page = browser.get(current_page) # Response object with .soup object

    # Get out of loop if we reach 'no cards exists' page.
    if bool(check_last_pg.search(collection_page.text)):
        break

    # Current Page. #collection_page.text because its response object
    html_page = collection_page.soup
    # Get all cards on this page.
    divs = html_page.findAll(class_= 'card-search-item col-lg-3 col-sm-4 col-xs-6 add-card-main element-relative')
    for div in divs:
        # This is where it gets fun.
        # Each div is a card from the search_view. a href has the link which contains info.
        card_name = str(div.find_all('a'))
        #print(card_name) # This is to be searched for the name of card; can also acquire set and card#
        card_details = str(div.find(class_ = 'display-count'))

        # STEP TWO: FORMULATE CARD
        # First part of string is count
        count = str(re.search(r'data-count="(\d)"', card_details, re.IGNORECASE).group(1))

        # Now get set - card#
        card_set = str(re.search(r'data-card="(\d+-\d+)"', card_details, re.IGNORECASE).group(1))
        card_set = card_set.split('-')
        details = '(Set' + str(card_set[0]) + ' #' + str(card_set[1]) + ')'

        # Now get card name with grammar
        name = str(re.search(r'<img alt="(.+)" class=', card_name, re.IGNORECASE).group(1))

        # Put it altogether....
        item = count + ' ' + name + ' ' + details
        #print(item)

        # Drop each page into a list for later...
        final_collection.append(item)


# final_collection # Uncomment to see list.


# In[114]:


len(final_collection) # Wow that numbers off! Eternal Statistics say I should have 68% 3,691/5,424 cards total.
# But let's think: IT's because it is only looking at the unique cards! So lets do math.


# In[ ]:


# Grab first character of each string (which we know is the count of each card in our collection up to 4) and add it.
total_cards = 0
for x in final_collection:
    total_cards = total_cards + int(x[0])
total_cards

output_json = {'total_cards': total_cards, 'my_collection': final_collection}


# In[ ]:


# Cool! WE got an accurate record of our cards, minus the Commons and UnCommons. Success for tonight.
# Output to a JSON file because sexy
with open('my_collection.json', 'w') as fp:
    json.dump(output_json, fp)
