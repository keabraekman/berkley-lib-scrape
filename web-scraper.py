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
            pickle_array.append(soup)
        print('saving ' + 'soups/names/'+words[i]+'.pkl')
        # Path("soups/"+words[i]).mkdir(parents=True, exist_ok=True)
        pickle.dump(pickle_array, open('soups/names/'+words[i]+'.pkl', 'wb'))


# collectSoups(search_words, pages)


# pickle > Array > soups > table > link > url > soup 

# I need to find the links and make an array out of it



# http://vm154.lib.berkeley.edu:3001/searchcase/fullDisplay?data=261039


def soup_to_links(soup):
    all_as = soup.find_all('a')
    urls = []
    for i in range(len(all_as)):
        if 'fullDisplay' in all_as[i]['href']:
            number = all_as[i]['href'].replace('/searchcase/fullDisplay?data=','')
            url = 'http://vm154.lib.berkeley.edu:3001/searchcase/fullDisplay?data=' + number
            urls.append(url)
    return urls




    # print(all_words)
    # return len(soup)





# Now we need to go through each pickle file > Each array element > 
# We want to have one pkl per name. The array is made up of the list of links


soup = (pickle.load(open('soups/names/Chin.pkl', 'rb')))[1]
# print(len(soup))

# print(soup_to_links(soup))



def create_individual_pages(words, pages):
    for i in range(len(words)):
        file = pickle.load(open('soups/names/' + words[i] + '.pkl', 'rb'))
        urls = []
        for j in range(pages[i]):
            soup = file[j]
            urls += soup_to_links(soup)
        
        pickle_array = []
        for j in range(len(urls)):
            url = urls[j]
            print('requesting : ', url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            pickle_array.append(soup)
        print('saving ' + 'soups/individual_pages/'+words[i]+'.pkl')
        pickle.dump(pickle_array, open('soups/individual_pages/'+words[i]+'.pkl', 'wb'))


# create_individual_pages(search_words, pages)



# We need to divide Chin and Fong since they're above 100mbs

def divide_pickle_array(pickle_array, fileName):
    pickle.dump(pickle_array[0:int(len(pickle_array)/2)], open(fileName + '1.pkl', 'wb'))
    pickle.dump(pickle_array[int(len(pickle_array)/2):len(pickle_array)], open(fileName + '2.pkl', 'wb'))


chin = pickle.load(open('soups/individual_pages/Chin.pkl', 'rb'))
divide_pickle_array(chin, 'soups/individual_pages/Chin')

fong = pickle.load(open('soups/individual_pages/Fong.pkl', 'rb'))
divide_pickle_array(fong, 'soups/individual_pages/Fong')