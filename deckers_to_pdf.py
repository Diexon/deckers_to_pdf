
from bs4 import *
import requests as rq
import os
import re

deck = "https://www.underworlds-deckers.com/en/deck-builder/mollogs-mob/?ObjectiveCard=2206,5261,5263,5278,5288,5301,5307,8259,8262,8287,8315,8326,&GambitCard=2213,2218,5323,5324,5341,5366,5377,6017,7017,8363,&UpgradeCard=2223,2224,2226,2228,5393,5396,5398,5413,5438,7039,&DeckTitle=Mollog%20competitivo%202"

card_types = ["ObjectiveCard","GambitCard","UpgradeCard"]

if not os.path.exists('cards'):
    os.mkdir('cards')

for card_type in card_types: 
    pattern = card_type + "=(.*?),\&"
    card_numbers = re.search(pattern, deck).group(1).split(',')
    # Safe the cards
    for card_number in card_numbers:
        img_data = rq.get('https://www.underworlds-deckers.com/imagesBackground6/1/'+card_number+'.png').content
        with open("cards/" + card_number + ".png", 'wb+') as f:
            f.write(img_data)
    f.close