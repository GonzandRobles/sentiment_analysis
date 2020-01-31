from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import requests
import re
import csv
import time
import random


response = requests.get('https://www.yelp.com/biz/bluebeard-coffee-roasters-tacoma?osq=Coffee+%26+Tea')
text = BeautifulSoup(response.text, 'html.parser')


# set the type of tag and class with attributes
num_reviews = text.find('div', attrs={'class':'lemon--div__373c0__1mboc arrange-unit__373c0__1piwO border-color--default__373c0__2oFDT nowrap__373c0__1_N1j'}).string
# regex the extract just the number of reviews, \d+ extracts just the numbers from a string
num_reviews = int(re.findall('\d+', num_reviews)[0])
#print(num_reviews)

url_list = []

for i in range(0, num_reviews, 20):
    url_list.append('https://www.yelp.com/biz/bluebeard-coffee-roasters-tacoma?osq=Coffee%20%26%20Tea&start='+str(i))
print(url_list)

# html tag that contains each customer review, username, location, rating, etc..
reviews = text.find_all('div', attrs={'class':'lemon--div__373c0__1mboc sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__UHqhV gutter-12__373c0__3kguh grid__373c0__29zUk layout-stack-small__373c0__3cHex border-color--default__373c0__2oFDT'})
# set review to the firt index
review = reviews[0]

with open('reviews.csv','w', encoding='utf-8') as csvfile:
    review_writer = csv.writer(csvfile)
    for review in reviews:
        # We use a dictionary to save one review because each review should have the same number of keys
        dic = {}
        username = review.find('span', attrs={'class','lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa'}).string
        location = review.find('span', attrs={'class','lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text-size--small__373c0__3SGMi'}).get_text()
        date = review.find('span', attrs={'span','lemon--span__373c0__3997G text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_'}).get_text()
        rating = review.find('span', attrs={'class', 'lemon--span__373c0__3997G display--inline__373c0__2q4au border-color--default__373c0__YEvMS'}).div.get('aria-label')
        rating = float(re.findall('\d+', rating)[0])
        content = review.find('p', attrs={'class','lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_'}).get_text()
        # assign values to the dictionary
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating
        dic['content'] = content
        # write the dictionaries to a local csv file
        review_writer.writerow(dic.values())
        
        
        
def scrape_single_page(reviews, csvwriter):
    for review in reviews:
        dic = {}
        username = review.find('span', attrs={'class','lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa'}).string
        location = review.find('span', attrs={'class','lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text-size--small__373c0__3SGMi'}).get_text()
        date = review.find('span', attrs={'span','lemon--span__373c0__3997G text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_'}).get_text()
        rating = review.find('span', attrs={'class', 'lemon--span__373c0__3997G display--inline__373c0__2q4au border-color--default__373c0__YEvMS'}).div.get('aria-label')
        rating = float(re.findall('\d+', rating)[0])
        content = review.find('p', attrs={'class','lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_'}).get_text()
        # assign values to the dictionary
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating
        dic['content'] = content
        # write the dictionaries to a local csv file
        csvwriter.writerow(dic.values())
        
with open('reviews.csv','w', encoding='utf-8') as csvfile:
    review_writer = csv.writer(csvfile)
    for index, url in enumerate(url_list):
        response = requests.get(url).text
        soup = BeautifulSoup(response,'html.parser')
        reviews = text.find_all('div', attrs={'class':'lemon--div__373c0__1mboc sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__UHqhV gutter-12__373c0__3kguh grid__373c0__29zUk layout-stack-small__373c0__3cHex border-color--default__373c0__2oFDT'})
        scrape_single_page(reviews, review_writer)
        # Random sleep to avoid getting banned from the server
        time.sleep(random.randint(1,3))
        # log the progress
        print('Finish Page ' + str(index + 1))
