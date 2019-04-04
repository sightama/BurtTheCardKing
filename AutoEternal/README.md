# AutoEternal - An automated player in the Eternal card game.
## Made for a specific deck and playstyle of my choosing.

### Build progression:

1. Have the ability to store the current cards in OUR hand.
  - Having tried various methods (inject process for metadata, reverse google image search),
  I settled on taking a screenshot every 3 seconds, then cropping the screenshot
  to the region where card names are usually, and then apply pyTesseract logic
  to OCR the text from the image. Varying results and weird characters occasionally,
  so the last step will be doing a string similarity comparison using the
  Normalized Levenshtein method and this guy/gals api. ->
  https://github.com/luozhouyang/python-string-similarity

  Once this works successfully end-to-end on a full hand of cards manually,
  I'll use pyautogui to automate the mouse hovering over each card for a seconds or so.
  (Enough time to get an image of the card_name)

  _____________________

2. Detect MY characters in battlefield + automated pyautogui hovering

3. Detect Enemy characters in battlefield

4. Detect when enemy plays card

5. Detect when enemy plays INSTANT spells (aka catching cards played non-RTS)
  -May face performance annd timing issues heavily here.

6. Create decision tree logic on moves made based on cards IN HAND AT ANY MOMENT.
  - Possible chance to play with utility score neural net calculators? (More research necessary)
