from pygooglenews import GoogleNews
import requests
from newspaper import Article

gn = GoogleNews(lang='en', country='IN')

def redirect_link(link):
    r = requests.get(link)
    return r.url
    

def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def get_url_article_dict(link):
    url_article_dict = {}
    url = redirect_link(link)
    url_article_dict['url'] = url
    url_article_dict['article'] = get_article(url)
    return url_article_dict



top = gn.top_news()
