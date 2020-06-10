import requests
from bs4 import BeautifulSoup

# main scrapper function
def scraper():
  url = "http://m.news24.com/Pages/MostRead"

  url_data = requests.get(url)
  soup = BeautifulSoup(url_data.text,  "html.parser")

  temp = []

  # appends all the links to a list - temp
  for link in soup.select('[href]'):
      temp.append(link['href'])

  # index = 9 is the first article on the most read page
  p = 9
  url = temp[p]

  # handles the edge case of video as an article
  # was not tested - most read has not been a video yet
  # (at the time of writing script)

  # iterate through temp[] until a new url is found
  # that isn't a video (or a live feed)
  for i in range(0, len(temp) - 1):
      if "live" in url or "watch" or"/video" in url:
          p += 1
          url = temp[p]
      break

  # gets a new soup object of the actual most read story
  temp = []
  res  = requests.get(url)
  soup = BeautifulSoup(res.text, "html.parser")

  # doen die res van die werk
  article = art(soup)
  title = tit(soup)
  writer(title, article)

# param: BeautifulSoup opject ('n hele gemors)
# return: String containing the article title
def tit(soup):
  title = ''
  for node in soup.find('h1', class_="article_page_title"):
    if node not in ["<h1>","class", "</h1>"]:
      title += ''.join(node)

  title = title.strip()
  return title


# param: BeautifulSoup opject ('n hele gemors)
# return: String containing the article body
def art(soup):
  article = ''
  for node in soup.find_all('p'):
    temp = node.find_all(text= True)
    article += " "
    article += ''.join(temp)
    article = article.strip()

  return article

# param: a - Title of article, article - scraped article body
# return: txt file with title and article body printed
def writer(a, article):
  f = open("most_read.txt", "w")
  f.write(a)
  f.write("\n\n")
  f.write(article)
  f.close()

def main():
  scraper()

main()
