import feedparser as fp
import rethinkdb as r
import time

def GetURL(rssEntry):
  return rssEntry.feedburner_origlink

def CheckForExisiting(rssEntry):
  if r.db("heisenberg").table("articles").get(GetURL(rssEntry)).run():
    return True
  else:
    return False

def SaveArticle(rssEntry):
  r.db("heisenberg").table("articles").insert({
    "url": GetURL(rssEntry),
    "savedate": Time.now.utc,
    "shares":[]
    }).run()

r.connect('localhost', 28015).repl()

for rssEntry in fp.parse('http://feeds.feedburner.com/rappler/').entries:
  if not CheckForExisting(rssEntry):
    SaveArticle(rssEntry)
