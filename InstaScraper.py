"""
Created by Joshua Tanke.
"""

import urllib
import urllib.request
from bs4 import BeautifulSoup
import sys
import os
from PIL import Image, ImageTk
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
root = tk.Tk()

def swap(text, ch1, ch2):
    text = text.replace(ch2, '!',)
    text = text.replace(ch1, ch2)
    text = text.replace('!', ch1)
    return text

def chopName(text):
    return text[text.find("@")+1:].split()[0]

def make_soup(url):
    page = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(page, "html.parser")
    return soupdata

def tagScrape(tag):
    count = 0
    path = os.mkdir("#" + tag)
    soup = make_soup("http://photagram.org/tag/" + tag)
    links = soup.findAll(attrs={"class":"thumbnail"})

    for link in links:
        if count == 20:
            break
        
        if link.a is None:
            continue
        count += 1
        currentLink = "http://photagram.org" + link.a.get("href")
        newSoup = make_soup(currentLink)
        
        nameSource = newSoup.find(attrs={"class":"img-rounded"})
        name = str(nameSource.get('alt')).translate(non_bmp_map)
        
        imgSource = newSoup.find(attrs={"class":"expand"})
        if imgSource is None:
            vidSource = newSoup.find(attrs={"class":"panel-body"})
            vid = vidSource.source.get('src')
            vidFile = open(os.path.join("#" + tag, chopName(name) + ".mp4"), 'wb')
            vidFile.write(urllib.request.urlopen(vid).read())
            vidFile.close()
        else:
            img = imgSource.get('href')
            imageFile = open(os.path.join("#" + tag, chopName(name) + ".jpeg"), 'wb')
            imageFile.write(urllib.request.urlopen(img).read())
            imageFile.close()

    print("Program complete.")


if __name__ == "__main__":
    tag = input("Please enter a tag...")
    tagScrape(tag)






    



    
