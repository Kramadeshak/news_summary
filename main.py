from GoogleNews import GoogleNews


googlenews = GoogleNews(lang='en', region='IN', encode='utf-8') # Parsing of string becomes easy
googlenews.enableException(True)
googlenews.search("Modi")
# googlenews.get_page(1)
# sanitize the links
page = googlenews.get_links()
# page = googlenews.get_page(1)
print((type(page)), page)



# fetch GoogleNews(text) -> links


# for link in links
    #processor -> map/template


