import feedburner
import rethinkdb

def GetLink(rssEntry):
  return rssEntry.feedburner_origlink

def GetSavedArticles():
  pass()

for rssEntry in feedparser.parse('http://feeds.feedburner.com/rappler/'):
  # Check if it exists in rethinkdb:
  if not GetLink(rssEntry) in GetSavedArticles():
    