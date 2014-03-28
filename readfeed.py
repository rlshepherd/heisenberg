#! /usr/local/bin/pythonw
"""
readfeed.py
===========
Read from Feedburner feed to RethinkDB.

Usage:
  readfeed.py <url>
Options: 
  -h --help    Show this screen.
  --version    Show version.

Examples:
=========
1. Get recent articles from www.rappler.com's feedburner feed:

python readfeed.py http://feeds.feedburner.com/rappler/

"""

import feedparser as fp
import rethinkdb as r
import time
from docopt import docopt

def GetURL(rssEntry):
  return rssEntry.feedburner_origlink
4
def CheckForExisting(rssEntry):
  '''Check for existing rethinkdb documents with this url.'''
  if len(list(r.db("heisenberg").table("articles").filter({
    "url": GetURL(rssEntry)
    }).run())) > 0:
    return True
  else:
    return False

def InsertArticle(rssEntry):
  '''Insert new document in rethinkdb for this article.'''
  r.db("heisenberg").table("articles").insert({
    "url": GetURL(rssEntry),
    "savedate": r.now(),
    "shares":[]
    }).run()

r.connect('localhost', 28015).repl()

if __name__ == '__main__':

  arguments = docopt(__doc__, version='Heisenberg v0.1')

  feed = arguments['<url>']

  for rssEntry in fp.parse(feed).entries:
    if not CheckForExisting(rssEntry):
      InsertArticle(rssEntry)