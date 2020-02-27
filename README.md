Support for python version 3.7.6
Also you will need to install 'Build Tools for Visual Studio' from here: https://visualstudio.microsoft.com/downloads/?q=visual+c%2B%2B+build+tools to be able to install jupyter fro mCLI to your venv.
Once your in the installer it will prompt you with options. Select only C++ build tools and proceed.




















OLD:
______________________________________________________________
Instructions (w/o markdown):

1. Create account at eternalwarcry.com, goto "Menu"->
    "Collection" -> "Browse Collection" ->

2. Sort by Owned cards

3. Goto Collection options, and select "Add by rarity"
  3a. Add All uncommon and common cards this way.

4. Next open Eternal on a PC through steam and create a deck with
    rares/promo's/legendaries sorted by EACH COLOR.
    IMPORTANT: Get the COUNT of cards for most accurate settings.
      Will most likely have a "fill-in-all-4" setting that makes it so users can/only have to select each card one time. My thought process is the more unique information, the better.
      4a. I found it helpful and useful to start from left to right when
      filtering each color, and ignoring mixed color cards that have been added ON THE LEFT. (if that makes any sense)

5. Export every deck of each color from Eternal and import into collection on
    EternalWarcry.com

_____________________________________________________________________
CLUSTERING STRUCTURE IDEAS:

STEP1: GATHER THE DATA
	- Use Selenium/BeautifulSoup to webscrape CARDNAME|CARDTEXT|FACTION(S), then store in csv or xls.
	OR
	- Find somebody's already made excel with card and text details.

STEP2: REMOVE STOPWORDS AND PERFORM K-MEANS ALG. ON CARDTEXT
	- Initially I wanted to group the factions, THEN cluster on the text, but for the first run we will cluster on just the text.


-Lane