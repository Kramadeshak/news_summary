import requests
import json
from pygooglenews import GoogleNews
from newspaper import Article
from gpt import generate_script



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

gn = GoogleNews(lang='en', country='IN')
top_news = gn.top_news() # World news, etc

for entry in top_news['entries']:
    event_article_list = get_event_article_list(entry)

    gpt_token_list = [{'title': d['title'], 'article': d['article']} for d in event_article_list]
    gpt_token_json = json.dumps(gpt_token_list)

    print(f"Token length:{len(gpt_token_json)}")

    response = generate_script(gpt_token_json, 'g4f')
    print(response)

 # multiple prompt for summary generation | combine multiple outputs, generate script(video fetching sources ko combine kaise krna h): videos generated on the basis of template created
 # references - sources for claiming genuinity
 # DB design
 # embeddings - gpt->number(embedding{data correlation}: can be loaded, for initial context & classification) | Eg - search via embeddings corellation
 # graphQL - expose as a service