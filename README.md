Heisenberg is a tool for tracking social shares of frequently updated websites. URLs to track are gathered from an RSS feed. Tracking frequency degrades with content age.

Is heisenberg right for me? Do you:

1. Want to monitor when your content is shared online?
2. Have an RSS feed?

Then you might find heisenberg useful.

TODO summary of purpose and screenshot

# Installation and Setup

1. [Install RethinkDB](http://rethinkdb.com/docs/install/)

2. Install Heisenberg (Using [pip](https://pypi.python.org/pypi/pip), [virtualenv](http://www.virtualenv.org/en/latest/), and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)).

        git clone https://github.com/rlshepherd/heisenberg.git
        mkvirtualenv heisenberg
        cd heisenberg
        pip install -r requirments.txt

3. Start collecting data:

        python heisenberg.py http://feeds.feedburner.com/mysite/

    You're collecting data now! Not familiar with RethinkDB yet? No problem, read on to install a very simple dashboard to get you started.

3. TODO: build web dashboard.

# FAQ

### What are the collection intervals? Why?

The collection intervals change according to how old the article is. The default settings are:

* New articles (between 0 and 2 days old): 10 minutes
* Recent articles (between 2 and 5 days old): 1 hour
* Old articles (between 5 and 30 days old): Daily at midnight

This reflects my view of a good balance between up-to-date information and managing resources. This might not be the right balance
for you or your website. I suggest running heisenberg for a bit to learn about hte "social halflife" of your content, and then tweaking the collection intervals accordingly.

### Can I change the collection intervals?

**Yes!** The easiet way to do this is by not running heisenberg.py at all and instead scheduling your updates via crontab (see the next question).

If you want to update the defaults in heisenberg.py, change the following lines:

    schedule.every(5).minutes.do(Update(0,2))
    schedule.every().hour.do(Update(3,5))
    schedule.every().day.at("00:00").do(Update(6,30))

You can be as fine or coarse grained as you want. I didn't add support for an open interval, but you could put a big number as the upper bound.

### Can I use crontab instead of python to schedule tasks?

**Yes!** All the logic needed to do the updates is baked into readfeed.py and updatecounts.py. If you want to use crontab, then don't use heisenberg.py. Here is a sample crontab file
which provides the exact same scheduling as heisenberg.py:

    10min python readfeed.py myfeed.rss
    10min python updatecounts.py 0 2
    1hour python updatecounts.py 2 5
    daily python updatecounts.py 5 30

### I have my own RSS feed, can I use something besides Feedburner?

**Yes,** and it is very easy to do so. Just modify the GetURL() function in readfeed.py to return the original URL of the article. For example, the RSS feed over at http://www.r-bloggers.net/rss/ looks like this:

    some json.

So our GetURL() function would look like this:

    some python.
