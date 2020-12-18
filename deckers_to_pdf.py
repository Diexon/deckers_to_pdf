
from bs4 import *
import requests as rq
import os
import sys
import re
from urllib.parse import unquote
from fpdf import FPDF

# Print alias
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
# Check if deck is accessible
try :
    rq.get(deck)
except rq.ConnectionError:
    sys.exit(bcolors.FAIL + bcolors.BOLD + "\tERROR: " + deck_title + " -> Not found" + bcolors.ENDC)

print(bcolors.HEADER + '\nExporting deck: ' + deck_title + '\n' + bcolors.ENDC)


# Download Images
card_types = ["ObjectiveCard","GambitCard","UpgradeCard"]

folder_out = deck_title.replace(' ','_')
if not os.path.exists(folder_out):
    os.mkdir(folder_out)

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
            with open(folder_out + "/" + card_number + ".png", 'wb+') as f:
                f.write(img_data)
        else:
            print(bcolors.FAIL + bcolors.BOLD + "\tERROR: " + card_number + " -> Not accessible" + bcolors.ENDC)
    f.close

# Build pdf
print(bcolors.HEADER + '\nCreating pdf...'+ bcolors.ENDC)

pdf = FPDF()
# imagelist is the list with all image filenames
images_per_row = 3
rows_per_page = 3
margin_x = 5
margin_y = 5
card_width = 63
card_height = 88.25

x = 0
y = 0
pdf.add_page()
for idx, filename in enumerate(os.listdir(folder_out)):
    if filename.endswith(".png"):
        idx_page = idx % (images_per_row * rows_per_page)
        # Fill page
        image = os.path.join(folder_out, filename)
        x = (idx_page % images_per_row) * card_width + margin_x
        y = int(idx_page / images_per_row) * card_height + margin_y
        pdf.image(image,x ,y,card_width,card_height)
        # Prepare new page
        if (int(idx_page / images_per_row) == rows_per_page - 1) and (idx_page % images_per_row == images_per_row - 1):
            pdf.add_page()
            x = 0
            y = 0

pdf.output(os.path.join(folder_out, folder_out + '.pdf'), "F")

print(bcolors.OKBLUE + '\nDONE!'+ bcolors.ENDC)