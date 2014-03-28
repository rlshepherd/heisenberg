import feedparser as fp
import rethinkdb as r
import time

def GetURL(rssEntry):
  return rssEntry.feedburner_origlink

def CheckForExisting(rssEntry):
  if len(list(r.db("heisenberg").table("articles").filter({
    "url": GetURL(rssEntry)
    }).run())) > 0:
    return True
  else:
    return False

def SaveArticle(rssEntry):
  r.db("heisenberg").table("articles").insert({
    "url": GetURL(rssEntry),
    "savedate": r.now(),
    "shares":[]
    }).run()

r.connect('localhost', 28015).repl()

for rssEntry in fp.parse('http://feeds.feedburner.com/rappler/').entries:
  if not CheckForExisting(rssEntry):
    SaveArticle(rssEntry)
