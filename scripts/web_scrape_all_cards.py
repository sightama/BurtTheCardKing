import re
import pandas as pd
import mechanicalsoup
from time import sleep
# from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings(action='once')

# Regular expressions utilized for jumping through HTML/BeautifulSoup objects.
fire = re.compile(r'<span class="ew ew-fire ew-highlighted"><\/span>', flags=re.IGNORECASE | re.MULTILINE)
shadow = re.compile(r'<span class="ew ew-shadow ew-highlighted"><\/span>', flags=re.IGNORECASE | re.MULTILINE)
time = re.compile(r'<span class="ew ew-time ew-highlighted"><\/span>', flags=re.IGNORECASE | re.MULTILINE)
justice = re.compile(r'<span class="ew ew-justice ew-highlighted"><\/span>', flags=re.IGNORECASE | re.MULTILINE)
primal = re.compile(r'<span class="ew ew-primal ew-highlighted"><\/span>', flags=re.IGNORECASE | re.MULTILINE)
remove_crap = re.compile(r'<br/>|<p>|</p>|<h1>|</h1>|<strong>|</strong>', flags=re.IGNORECASE | re.MULTILINE)
re_card_text = re.compile(r'<p class=\"text-center text-xl\">([\s\S]*)<div class=\"align-c\" id=\"card-sounds\">',
                          re.IGNORECASE)


def acquire_all_cards():
    # Initialize stuff.
    page_num = 1  # Page number while iterating through cards on eternal warcry website.
    df_index = 0  # Index of dataframe
    df_all_cards = pd.DataFrame(columns=['name', 'faction', 'type', 'text'])  # Initialize DF
    browser = mechanicalsoup.Browser(soup_config={'features': 'lxml'})  # TODO: Use BeautifulSoup browser.
    try:
        while True:
            # Now that were logged in pull each link for our collection and grab the info
            current_page = 'https://eternalwarcry.com/cards?p=' + str(page_num)
            collection_page = browser.get(current_page)  # Response object with .soup object

            # Get out of loop if we reach 'no cards exists' page.
            # if bool(check_last_pg.search(collection_page.text)):
            #     break

            # Current Page. #collection_page.text because its response object
            html_page = collection_page.soup
            # Get all cards on this page.
            divs = html_page.findAll(
                class_='card-search-item col-lg-3 col-sm-4 col-xs-6 add-card-main element-relative')
            # Break out of loop if on last page (AKA no cards, therefore no divs).
            if not divs:
                break  # END OF CARDS LIST.

            for div in divs:  # For each card on this page...
                link_ext = str(div.find('a')['href'])  # Find the cards page.
                card_page = 'https://eternalwarcry.com' + link_ext
                sleep(2)  # Don't make too many requests too quickly, or the site throttles you.
                request_page = browser.get(card_page)
                card_info = request_page.soup

                """Card name"""
                name = str(card_info.find('h1'))  # The h1 header is the name.
                name = remove_crap.sub("", name).strip()

                """Faction & Type"""
                card_table = pd.read_html(request_page.content, index_col=0)[
                    1]  # Investigate if better way. This line takes forever.
                faction = card_table.at['Faction', 1]
                type = card_table.at['Type', 1]

                """Everything below relates to getting card text+flavor."""
                # Below: 1st object = picture info, 2nd object = card info.
                layered_div = card_info.findAll('div', {"class": "col-sm-6"})[1]
                # Use regular expressions to grab text if exists.
                card_text = re_card_text.search(str(layered_div))  # This is prone to breaking, scary...
                if not card_text:  # For cases like 'Fire Sigil', where no text for card.
                    card_text = 'NONE'
                else:
                    card_text = card_text.group(1).strip()
                # Remove HTML and crap surrounding relevant card text.
                card_text = remove_crap.sub("", card_text).strip()
                if 'span class' in card_text:
                    # Remove spanclass and find if fire|time|shadow|justice|primal
                    card_text = fire.sub('Fire', card_text)
                    card_text = shadow.sub('Shadow', card_text)
                    card_text = time.sub('Time', card_text)
                    card_text = justice.sub('Justice', card_text)
                    card_text = primal.sub('Primal', card_text)
                    # TODO: Make this account for multifactions gained. (forloop)

                # Finally export new row to dataframe.
                df_all_cards.loc[df_index] = [str(name), str(faction), str(type), str(card_text)]
                df_index = df_index + 1  # Increase dataframe index.

                # TODO: Create soup object using BeautifulSoup NOT mechanicalsoup,
                # TODO: See if the above grabs ENTIRE table, for rarity, shifstone, etc.

            page_num = page_num + 1  # Iterate don't wanna forget ;)

        print(str(page_num), str(df_index))  # Just for verification that we hit 54 pgs, and have 1721 cards.
        df_all_cards.to_excel('scripts/all_cards.xlsx', index=False)
        df_all_cards.to_csv('scripts/all_cards.csv', index=False)
    except Exception as e:
        print(f'Error: Exception thrown: {e}')


if __name__ == "__main__":
    acquire_all_cards()
