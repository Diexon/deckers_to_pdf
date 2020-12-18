
from bs4 import *
import requests as rq
import os
import sys
import re
from urllib.parse import unquote

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

deck = "https://www.underworlds-deckers.com/en/deck-builder/mollogs-mob/?ObjectiveCard=2206,5261,5263,5278,5288,5301,5307,8259,8262,8287,8315,8326,&GambitCard=2213,2218,5323,5324,5341,5366,5377,6017,7017,8363,&UpgradeCard=2223,2224,2226,2228,5393,5396,5398,5413,5438,7039,&DeckTitle=Mollog%20competitivo%202"

deck_title = unquote(re.search('DeckTitle=(.*)', deck).group(1))
#Check if deck is accessible
try :
    rq.get(deck)
except rq.ConnectionError:
    sys.exit(bcolors.FAIL + bcolors.BOLD + "\tERROR: " + deck_title + " -> Not found" + bcolors.ENDC)

print(bcolors.HEADER + '\nExporting deck: ' + deck_title + '\n' + bcolors.ENDC)

card_types = ["ObjectiveCard","GambitCard","UpgradeCard"]

folder_name = deck_title.replace(' ','_')
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

for card_type in card_types: 
    print("Scrapping " + card_type + "...")
    pattern = card_type + "=(.*?),\&"
    card_numbers = re.search(pattern, deck).group(1).split(',')
    # Safe the cards
    for card_number in card_numbers:
        img_data = rq.get('https://www.underworlds-deckers.com/imagesBackground6/1/'+card_number+'.png')
        if img_data.status_code != 404:
            img_data = img_data.content
            print(bcolors.OKGREEN + "\t" + card_number + " -> Downloaded" + bcolors.ENDC)
            with open(folder_name + "/" + card_number + ".png", 'wb+') as f:
                f.write(img_data)
        else:
            print(bcolors.FAIL + bcolors.BOLD + "\tERROR: " + card_number + " -> Not accessible" + bcolors.ENDC)
    f.close