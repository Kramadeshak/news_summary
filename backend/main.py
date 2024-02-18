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
    return article.title, article.text

def get_url_article_dict(link):
    url_article_dict = {}
    url = redirect_link(link)
    url_article_dict['url'] = url
    url_article_dict['title'], url_article_dict['article'] = get_article(url)
    return url_article_dict

def get_event_article_list(entry):
    article_list = [get_url_article_dict(entry.link)]
    for article_link in entry['sub_articles']:
        article_list.append(get_url_article_dict(article_link['url']))
    return article_list

top = gn.top_news()

event_article_list = get_event_article_list(top['entries'][0])

gpt_token_list = [{'title': d['title'], 'article': d['article']} for d in event_article_list]
gpt_token_json = json.dumps(gpt_token_list)

print(f"Event json:\n{gpt_token_json}\nlength:{len(gpt_token_json)}")
