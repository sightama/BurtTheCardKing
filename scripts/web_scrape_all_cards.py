"""
This script takes approximately 13.333 - 15 minutes to run, and will create two
 documents represnting all cards in the current meta of Eternal: TCG.
"""
import requests
import re
import pandas as pd
import warnings
import datetime
from bs4 import BeautifulSoup
warnings.filterwarnings(action='once')


# Regular expressions utilized for jumping through HTML/BeautifulSoup objects.
fire = re.compile(r'<span class=\"ew ew-fire ew-highlighted\">\W*<\/span>', flags=re.IGNORECASE | re.MULTILINE)
shadow = re.compile(r'<span class=\"ew ew-shadow ew-highlighted\">\W*<\/span>', flags=re.IGNORECASE | re.MULTILINE)
time = re.compile(r'<span class=\"ew ew-time ew-highlighted\">\W*<\/span>', flags=re.IGNORECASE | re.MULTILINE)
justice = re.compile(r'<span class=\"ew ew-justice ew-highlighted\">\W*<\/span>', flags=re.IGNORECASE | re.MULTILINE)
primal = re.compile(r'<span class=\"ew ew-primal ew-highlighted\">\W*<\/span>', flags=re.IGNORECASE | re.MULTILINE)
remove_crap = re.compile(r'<br/>|<p>|</p>|<h1>|</h1>|<strong>|</strong>', flags=re.IGNORECASE | re.MULTILINE)
re_card_text = re.compile(r'<p class=\"text-center text-xl\">([\s\S]*)<div class=\"align-c\" id=\"card-sounds\">',
                          re.IGNORECASE)


def acquire_all_cards():
    # Initialize stuff.
    sesh = requests.Session()
    page_num = 1  # Page number while iterating through cards on eternal warcry website.
    df_index = 0  # Index of dataframe
    df_all_cards = pd.DataFrame(columns=['type', 'set', 'faction', 'name', 'text'])  # Initialize DF
    try:
        while True:
            current_page = 'https://eternalwarcry.com/cards?p=' + str(page_num)
            resp = sesh.get(url=current_page)
            resp.raise_for_status()
            # Current Page.
            html_page = BeautifulSoup(resp.text, 'html.parser')
            # Get all cards on this page.
            di = html_page.findAll(class_='card-search-item col-lg-3 col-sm-4 col-xs-6 add-card-main element-relative')

            # Break out of loop and save to files if end of cards list (e.g. no divs (cards)).
            if not di:
                break  # END OF CARDS LIST.

            for div in di:  # For each card on this page...
                link_ext = str(div.find('a')['href'])  # Find the cards page.
                card_page = 'https://eternalwarcry.com' + link_ext
                card_resp = sesh.get(url=card_page)
                card_info = BeautifulSoup(card_resp.text, 'html.parser')

                """Card name"""
                name = str(card_info.find('h1'))  # The h1 header is the name.
                name = remove_crap.sub("", name).strip()
                data = []
                """Faction, Type & Set"""
                table = card_info.find('table', attrs={'class': 'table table-condensed'})
                # table_body = table.find('tbody')
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])  # Get rid of empty values
                # The first tr contains the field names.
                card_type = data[0][1]
                card_set = data[1][1]
                faction = data[2][1]

                """Everything below relates to getting card text+flavor. Clean text data."""
                # Below: 1st object = picture info, 2nd object = card info.
                layered_div = card_info.findAll('div', {"class": "col-sm-6"})[1]
                # Use regular expressions to grab text if exists.
                card_text = re_card_text.search(str(layered_div))  # This is prone to breaking, scary...
                if not card_text:  # For cases like 'Fire Sigil', where no text for card.
                    card_text = 'NONE'
                else:
                    card_text = card_text.group(1)
                    card_text = card_text.replace('<', ' <')
                    card_text = card_text.replace('.', '. ')
                    #card_text = card_text.replace('\n', ' ')
                    card_text = card_text.strip()
                # Remove HTML and crap surrounding relevant card text.
                card_text = remove_crap.sub("", card_text).strip()
                if 'span class' in card_text:
                    # Remove spanclass and find if fire|time|shadow|justice|primal
                    card_text = fire.sub('Fire', card_text)
                    card_text = shadow.sub('Shadow', card_text)
                    card_text = time.sub('Time', card_text)
                    card_text = justice.sub('Justice', card_text)
                    card_text = primal.sub('Primal', card_text)
                    # TODO: Make this account for multifactions gained. (forloop) [Does this handle it right?)

                # Post cleanup
                for x in ['   ', '  ', '\n']:
                    card_text = card_text.replace(x, ' ')
                card_text = card_text.replace(' :', ':')

                # Finally export new row to dataframe.
                df_all_cards.loc[df_index] = [str(card_type), str(card_set), str(faction), str(name), str(card_text)]
                df_index = df_index + 1  # Increase dataframe index.
                # TODO: See if the above grabs ENTIRE table, for rarity, shifstone, etc.

            now = datetime.datetime.now()
            print(f'Completed page {page_num} at time\t\t {str(now.hour)+":"+str(now.minute)+":"+str(now.second)}')
            page_num = page_num + 1  # Iterate don't wanna forget ;)

        print(str(page_num), str(df_index))  # Just for verification that we hit 54 pgs, and have 1721 cards.
        df_all_cards.to_excel('scripts/all_cards.xlsx', index=False)
        df_all_cards.to_csv('scripts/all_cards.csv', index=False)
    except Exception as e:
        print(f'Error: Exception thrown: {e}')


if __name__ == "__main__":
    acquire_all_cards()
