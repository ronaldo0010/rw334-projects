import requests
from bs4 import BeautifulSoup
from operator import itemgetter

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import copy
from nltk.corpus import movie_reviews
import random
from nltk.tokenize import word_tokenize

try:
    nltk.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def scraper():
    work = "https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=rPRXhYeMN9E6OCRWs7704hENbvHAGmyK"
    res = requests.get(work)
    all = res.json()
    movie_data = all["results"]
    myLs = []

    # adds the first 20 reviews to a list of dict's
    for i in range(0, 19):
        link = movie_data[i]["link"]
        url = str(link["url"])
        review = requests.get(url)

        article = form(review)
        author = movie_data[i]["byline"]
        author = author[0] + author[author.index(' '): ]
        odate = movie_data[i]["opening_date"]
        # gets movie reviews with none value as opening_date
        # and changes it to the begining of time
        if odate == None:
            odate = '0000-00-00'

        # List of dics
        myLs.append({
            "name": "{}".format(movie_data[i]["display_title"]),
            "mod_date": "{}".format(movie_data[i]["date_updated"]),
            "author": "{}".format(author),
            "open_date":"{}".format(odate),
            "review": "{}".format(article)
        }

        )

    myLs = sorted(myLs, key=lambda k: (k['open_date'], k['mod_date']), reverse = True)

    # review_ls is a list that contains 15 reviews (sorted according
    # to openinge_date)
    review_ls = []

    # this displays the dic

    for i in range(15):
        review_ls.append(myLs[i]["review"])

    print_dict(myLs)

    #senti = (vader_senti_anal(review_ls))

    # myLs[] - contains movies
    # belangrike var's:
    # senti - contains analysis

    #for i in range(0, 15):
    #    myLs[i].update({
    #    "senti" : senti[i]
    #    })

    #print(senti)



def form(review):
        article = ''

        website = BeautifulSoup(review.text, "html.parser")
        for node in website.find_all('p', class_ = "css-1smgwul e1wiw3jv0"):
            article += ''.join(node.find_all(text = True))

        return article

def main():
    scraper()

def print_dict(ls):
    for i in range(0, 15):
        print("Movie Review " + str(i+1) )
        print("_________________________________________")
        print()
        print("Movie Title: " + ls[i]["name"])
        print("Name: " + ls[i]["author"])
        print("Opening Date: " + ls[i]["open_date"])
        print("Last modified date: " + ls[i]["mod_date"])
        print()
        print("Movie Review: ")
        print(ls[i]["review"])
    #    print("Review Sentiment: " + str(ls[i]["senti"]) )
    #    print()
        print("_________________________________________")
        print()


def vader_senti_anal(review):
  # res contains senti anal for each coresponding review
    res = []
    reviews = copy.deepcopy(review)

    sia = SentimentIntensityAnalyzer()

    for sentence in reviews:

      sk = sia.polarity_scores(sentence)
      e = sk["compound"]
      if e >= 0.05:
          comp = "Positive"
      elif e > -0.05 and e < 0.05:
          comp = "Neutral"
      elif e < -0.05:
          comp = "Negative"
      d = (e, comp)
      res.append(d)

    return res


main()
