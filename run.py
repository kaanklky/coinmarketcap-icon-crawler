import re
import requests
import os
from bs4 import BeautifulSoup as bs
import threading
import timeit

def downloadImage(symbol, id, size):
    print('downloading size ' + size + ' for ' + symbol)
    currentLink      = staticBaseURL + size + '/' + id + '.png'
    currentDirectory = 'icons/' + size
    currentFile      = currentDirectory + '/' + symbol + '.png'

    if not os.path.exists(currentDirectory):
        os.makedirs(currentDirectory)
    
    if os.path.exists(currentFile):
        return
    
    with open(currentFile, 'wb') as currentImage:
        resp = requests.get(currentLink, stream = True)

        for block in resp.iter_content(1024):
            currentImage.write(block)
    
    print('downloaded size ' + size + ' for ' + symbol)



listURL       = 'https://coinmarketcap.com/all/views/all/'
staticBaseURL = 'https://s2.coinmarketcap.com/static/img/coins/'
sizes         = ['16x16', '32x32', '64x64', '128x128', '200x200']

print('getting whole page')
req       = requests.get(listURL)
soup      = bs(req.content, 'html5lib')
listItems = soup.select('table#currencies-all')[0].select('tbody > tr')
start = timeit.default_timer()

for i in range(0, len(listItems)):
    currentSymbol = re.sub('[!@#$]', '', listItems[i].select('td.col-symbol')[0].decode_contents().lower())
    currentID     = listItems[i].select('td.currency-name')[0].select('div')[0].attrs['class'][0][4:]

    for j in range(0, len(sizes)):
        threading.Thread(target = downloadImage, args = (currentSymbol, currentID, sizes[j])).start()

stop = timeit.default_timer()
print('time: ', stop - start)