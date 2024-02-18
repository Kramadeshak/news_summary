from pygooglenews import GoogleNews
import requests
from newspaper import Article

gn = GoogleNews(lang='en', country='IN')


def get_url(entry):
    r= requests.get(entry['link'])
    url = r.url
    article = Article(url)
    article.download()
    article.parse()
    print(article.text)




top = gn.top_news()

get_url(top['entries'][0])

