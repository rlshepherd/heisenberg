#! /usr/local/bin/pythonw
"""
heisenberg.py
===========
Tracks social shares for articles collected from a feedburner feed.

Usage:
  heisenberg.py <feed>

Options:
  -h --help    Show this screen.
  --version    Show version.

Examples:
=========
1. Track social shares from r-bloggers.net

python heisenberg.py http://www.r-bloggers.net/rss/

"""

import cmd
import datetime
import logging
import rethinkdb as r
from docopt import docopt
import schedule
import threading

running = True

class StopCmd(cmd.Cmd):
  """ Handle STDIN.
  """
  def Stop(self, message):
    print "Stopping heisenberg...\n"
    running = False
    return(1)
  def Status(self, message):
    print "Active Articles: %s \n" % keys.count
    print "Errors so far: %s \n" % keys.errors

class TaskMaster(threading.Thread):
  """ Thread for scheduling tasks.
  """
  def run(self):
    logging.info('Schedule thread started.')
    schedule.every(5).minutes.do(ReadFeed(feed))
    schedule.every(5).minutes.do(Update(0,2))
    schedule.every().hour.do(Update(3,5))
    schedule.every().day.at("00:00").do(Update(6,30))
    while running:
      schedule.run_pending()
      time.sleep(1)
  def stop(self):
    running = False
    logging.info('Stop signal sent.')

if __name__ == '__main__':

  logging.basicConfig(filename='heisenberg.log',
                      level=logging.INFO,
                      format='%(asctime)s %(message)s',
                      datefmt='%d/%m/%Y %I:%M:%S %p')

  logging.info('Started.')

  arguments = docopt(__doc__, version='Heisenberg v0.1')
  feed = arguments['<feed>']

  taskmaster = TaskMasker()
  taskmaster.start()
  print "Heisenberg now running on RSS feed: %s" % feed
  print "Activate your dashboard in another terminal: python app.py"
  print "Type Status to see collection status or Stop to stop collection."
  waiting = StopCmd()
  waiting.prompt = 'heisenberg > '
  waiting.cmdloop()
  taskmaster.stop()
  taskmaster.join()
