import requests
import json
from pygooglenews import GoogleNews
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

def get_event_article_list(entry):
    article_list = [get_url_article_dict(entry.link)]
    for article_link in entry['sub_articles']:
        article_list.append(get_url_article_dict(article_link['url']))
    return article_list

top = gn.top_news()

event_article_list = get_event_article_list(top['entries'][0])

event_json = json.dumps(event_article_list)

print(f"Event json:\n{event_json}")
