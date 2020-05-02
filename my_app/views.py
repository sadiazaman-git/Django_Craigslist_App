from django.shortcuts import render
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests
import re
import lxml

# Create your views here.

craigslist_url = "https://losangeles.craigslist.org/search/bbb?query={}"
image_url = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):

    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    final_url = craigslist_url.format(quote_plus(search))
    response = requests.get(final_url)
    # print(response)
    soup = BeautifulSoup(response.text, features='lxml')
    # print(soup)
    '''
    post_title = post_list[0].find(class_='result-title').text
    # post_price = post_list[0].find(class_='result-price').text
    post_url = post_list[0].find('a').get('href')
    print(post_title)
    print(post_url)
    image_id = post_list[0].find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]
    image = image_url.format(image_id)
    print(image)
    #cprint(post_price)
    '''
    post_list = soup.find_all('li', {'class': 'result-row'})

    final_post = []

    for post in post_list:
        title = post.find(class_="result-title").text
        url = post.find('a').get('href')

        if post.find(class_='result-image').get('data-ids'):
            image_id = post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]
            image = image_url.format(image_id)
            print(image)

        else:
            image = 'https://craigslist.org/images/peace.jpg'

        if post.find(class_ = 'result-price'):
            price = post.find(class_='result-price').text

        else:
            price = 'N/A'

        final_post.append((title, url, image ))

    return render(request, 'my_app/new_search.html', {'search': search, 'final_post':final_post,})
