import feedparser as fp
import rethinkdb as r
import time

def GetURL(rssEntry):
  return rssEntry.feedburner_origlink

def GetSavedArticles():
  pass

def SaveArticle(rssEntry):
  r.db("heisenberg").table("articles").insert({
    "url": GetURL(rssEntry),
    "savedate": time.strftime("%x %X"),
    "shares":[]
    }).run()

r.connect('localhost', 28015).repl()

savedArticles = GetSavedArticles()

for rssEntry in fp.parse('http://feeds.feedburner.com/rappler/').entries:
    SaveArticle(rssEntry)
