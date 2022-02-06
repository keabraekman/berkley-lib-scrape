import requests
from bs4 import BeautifulSoup
import pickle
from pathlib import Path
import sys
sys.setrecursionlimit(10000)

# page1 = requests.get("https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000")
# soup1 = BeautifulSoup(page1.content, 'html.parser')

search_words = ["Jair", "Der", "Ching", "Chin", "Tsing", "Hong", "Fong", "Tan", "Dea"]
pages = [1,3,20,56,1,34,55,13,5]


# http://vm154.lib.berkeley.edu:3001/searchcase/display?commit=Search&page=1&q=jair&utf8=%E2%9C%93
# page1 = requests.get(url)
# soup1 = BeautifulSoup(page1.content, 'html.parser')
# print(soup1)


# Create a function that creates the URLs necessary to collect the soups
# Save the soups as pickle objects. One object per word. Save them as arrays
# One page per item in the array
def collectSoups(words, pages):
    for i in range(len(words)):
        pickle_array = []
        for j in range(pages[i]):
            url = 'http://vm154.lib.berkeley.edu:3001/searchcase/display?commit=Search&page='+str(j+1)+'&q='+words[i]+'&utf8=%E2%9C%93'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            print('saving ' + 'soups/'+words[i]+'/'+str(j+1)+'.pkl')
            Path("soups/"+words[i]).mkdir(parents=True, exist_ok=True)
            pickle.dump(soup, open('soups/'+words[i]+'/'+str(j+1)+'.pkl', 'wb'))


collectSoups(search_words, pages)


# jair = pickle.load(open('soups/Der.pkl', 'rb'))

# print(jair)
