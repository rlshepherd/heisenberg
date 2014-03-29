#! /usr/local/bin/pythonw
"""
updatecounts.py
===========
Update social share counts for articles saved in a rethinkdb table.

Usage:
  updatecounts.py <lowerBound> <upperBound>

Options:
  -h --help    Show this screen.
  --version    Show version.

Examples:
=========
1. Update counts for articles less than 2 days old:

python updatecounts.py 0 2

2. Update counts for articles older than 2 day and younger than 5:

python updatecounts.py 2 5

3. Update counts for articles older than 3 days and younger than 30:

python updatecounts.py 5 30

"""

import rethinkdb as r
import json
import urllib2
import datetime
from docopt import docopt


def Twitter(url):
    '''Return total shares on Twitter for a url.'''
    response = urllib2.urlopen(
        'http://cdn.api.twitter.com/1/urls/count.json?url=%s' % url)
    data = json.loads(response.read())
    if 'count' in data.keys():
        return data['count']
    else:
        return 0


def Facebook(url):
    '''Return total shares on Facebook for a url.'''
    response = urllib2.urlopen(
        'http://graph.facebook.com/?id=%s' % url)
    data = json.loads(response.read())
    if 'shares' in data.keys():
        return data['shares']
    else:
        return 0

def PrevShareCount(url, platform):
    '''Return previous shares for a given url and platform from rethinkdb.'''
    selection = r.db('heisenberg').table('articles').filter({
      'url' : url})['shares'].run()
    shareHistory = list(selection)[0]
    if (len(shareHistory) > 0):
      platformHistory = [ ob['count'] for ob in shareHistory
                          if ob['platform'] == platform ]
      if len(platformHistory) == 0:
        return(0)
      else:
        return(platformHistory[len(platformHistory) - 1])
    else:
      return(0)


def NewShares(url, platform):
    '''Get shares since last count for a url and platform'''
    if platform == "Twitter":
        return Twitter(url) - PrevShareCount(url, platform)
    elif platform == "Facebook":
        return Facebook(url) - PrevShareCount(url, platform)


def UpdateShares(url, platform):
    '''Save count of new shares to rethinkdb.'''
    r.db('heisenberg').table('articles').filter({'url': url}).update({
        'shares': r.row['shares'].append({
          'count': NewShares(url, platform),
          'timestamp': r.now(),
          'platform': platform
        })
    }).run()


def GetSelectionURLs(lowerBound, upperBound):
    now = datetime.datetime.utcnow()
    y = now - datetime.timedelta(lowerBound)
    x = now - datetime.timedelta(upperBound)
    selection = r.db('heisenberg').table('articles').filter(
        r.row['savedate'].during(
            r.time(x.year, x.month, x.day, x.hour, x.minute, x.second, "Z"),
            r.time(y.year, y.month, y.day, y.hour, y.minute, y.second, "Z"))
    ).run()
    #TODO: get most recent shares per platform.
    urls = [article['url'] for article in list(selection)]
    return(urls)


def UpdateRange(lowerBound, upperBound):
    '''Update all articles older than lowerBound days old, and younger than
       upperBound days.
    '''
    articlesToUpdate = GetSelectionURLs(lowerBound, upperBound)
    for url in articlesToUpdate:
        UpdateShares(url, 'Twitter')
        UpdateShares(url, 'Facebook')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Heisenberg v0.1')

    if arguments['lowerBound'] < arguments['upperBound']:
        lowerBound = arguments['lowerBound']
        upperBound = arguments['upperBound']
    else:
        raise exception('lowerBound must be smaller than upperBound!')
    r.connect('localhost', 28015).repl()
    UpdateRange(lowerBound, upperBound)
