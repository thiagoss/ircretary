# -*- coding: utf-8 -*-

from time import time
from random import randint

import twitter

# API keys
from keys import consumer_key, consumer_secret, access_token_key, \
    access_token_secret

def clean(msg):
    """ Removes special characters from the message.

    @param msg: message to be cleansed (muaha)
    @type msg: string
    """
    return msg.replace('&lt;', '<').replace('&gt;', '>')


class Echo(str):
    pass


class Engine(object):
    MaxCmdsPerSec = 10
    DefaultProbability = 10

    def __init__(self):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        self.count = 0
        self.probability = Engine.DefaultProbability
        self.last = time()

    def twit(self, message):
        """ Tweets a message and increases our counter.
        """
        self.count += 1

        try:
            status = self.api.PostUpdate(message)
            message = 'Twitted (' + status.text + ')'

            if self.count > 4:
                message += ' (delicious spam: http://www.twitter.com/_lolwtf)'
                self.count = 0

        except Exception, e:
            message = 'Failed to twit! :-( (%s)' % str(e)

        return clean(message)

    def process(self, cmd):
        """ Processes a command
        """
        if '!twit' in cmd:
            return Echo(self.twit(cmd.split('!twit')[1]))
        elif '!url' in cmd and time() > self.last + Engine.MaxCmdsPerSec:
            self.last = time()
            return Echo('Url: http://twitter.com/_lolwtf')
        elif '!chances' in cmd:
            try:
                self.probability = int(cmd.split('!chances')[1].replace('%', ''))
                ans = Echo('Probability set to %d%%' % self.probability)
                self.probability = int(100.0/float(self.probability))
                print self.probability
                return ans
            except Exception, e:
                print e
                return Echo('Failed to set probability. Example: !chances 50%.')
        elif randint(1, self.probability) == 1:
            return Echo(self.twit(cmd))


