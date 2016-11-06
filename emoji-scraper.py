# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import urllib 

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

    def get_emoji_name(self, cell): 
        return cell.getText() 

    def download_images(self, emoji_table): 
        for row in emoji_table[1::]: 
            cells = row.find_all("td")
            try: 
                name = self.get_emoji_name(cells[16])
                if ':' in name: 
                    name = name.replace(':', '')
                url = self.get_emoji_url(cells[4])
                urllib.urlretrieve(url, "emojis/"+name+".png")   
            except Exception, e: 
                # I know this is /bad/ but
                # likely an index out of range exception
                # meaning there is no image or it's a row we don't need
                pass             

if __name__ == "__main__": 
    Scraper = EmojiScraper("http://unicode.org/emoji/charts/full-emoji-list.html")
    Scraper.get_soup() 
    table = Scraper.get_emoji_table()
    Scraper.download_images(table)