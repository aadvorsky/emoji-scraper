# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import os
import sqlite3


class EmojiScraper(object):
    def __init__(self, url):
        self.url = url 
        self.soup = None

    def get_soup(self): 
        page = requests.get(self.url)
        self.soup = bs(page.text, "html.parser")

    def get_emoji_table(self): 
        return self.soup.find("table").find_all("tr")

    def get_emoji_url(self, cell):
        return cell.find("img")["src"]

    def get_emoji_attr(self, cell):
        return cell.getText()

    def download_images(self, emoji_table):
        conn = sqlite3.connect('database.db')
        print(conn)
        c = conn.cursor()
        for row in emoji_table[1::]:
            cells = row.find_all("td")
            try:
                name = self.get_emoji_attr(cells[16])
                categories = self.get_emoji_attr(cells[18]).split(' | ')
                #print(categories)
                if ':' in name:
                    name = name.replace(':', '')
                url = self.get_emoji_url(cells[5])
                c.execute("INSERT INTO emojis (name, url) VALUES (? , ?)", (name, url))
                for cat in categories:
                    #print(cat)
                    c.execute("INSERT INTO categories (emoji_name, category) VALUES (? , ?)", (name, cat))
                #print(url)
                urllib.request.urlretrieve(url, "emojis/" + name + ".png")
            except Exception as e:
                # I know this is /bad/ but
                # likely an index out of range exception
                # meaning there is no image or it's a row we don't need
                # print error to be certain
                print(e)
                pass
        conn.commit()         


if __name__ == "__main__": 
    Scraper = EmojiScraper("http://unicode.org/emoji/charts/full-emoji-list.html")
    Scraper.get_soup() 
    table = Scraper.get_emoji_table()
    print(os.path.exists('emojis'))
    if not os.path.exists('emojis'):
        os.makedirs('emojis') 
    Scraper.download_images(table)
