#!/usr/bin/env python
# encoding: utf-8

"""
log.py - A log module for willie.
Copyright 2013, Timothy Lee <marlboromoo@gmail.com>
Licensed under the MIT License.
"""

import time
import json
import willie
import redis

MODULE = 'log'
db = None
logging = True

def configure(config):
    """

    | [log] | example | purpose |
    | ----- | ------- | ------- |
    | redis_host | localhost | Redis host |
    | redis_port | 6379 | Redis port |
    | redis_db | log | Redis dbid |

    """
    if config.option('Configure log', False):
        config.interactive_add('log', 'redis_host',
                               'Redis host', 'localhost')
        config.interactive_add('log', 'redis_port', 'Redis port', 6379)
        config.interactive_add('log', 'redis_db', 'Redis dbid', 0)


def setup(bot):
    """Setup the database.

    :bot: willie.bot.Willie

    """
    global db
    #. get settings
    host, port, db = None, None, None
    try:
        host=bot.config.log.redis_host
        port=int(bot.config.log.redis_port)
        db=bot.config.log.redis_db
    except Exception, e:
        print "%s: Configure the module first!" % (MODULE)
    #. init the DB
    if all([host, port, db]):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        db = redis.Redis(connection_pool=pool)
        #. check status
        try:
            db.info()
        except Exception, e:
            print "%s: DB init fail - %s" % (MODULE, e)

def _log(channel, time, nick, msg):
    """@todo: Docstring for _log.

    :time: @todo
    :channel: @todo
    :nick: @todo
    :msg: @todo
    :returns: @todo

    """
    try:
        key = "%s:%s:%s" % (channel, time, nick)
        db.rpush(key, json.dumps(
            dict(channel=channel, time=time, nick=nick, msg=msg)))
        #print key
        #print db.lrange(key, 0, -1)
    except Exception, e:
        print "%s: logging fail - %s " % (MODULE, e)

@willie.module.rule('.*')
def log(bot, trigger):
    """Log the message to the database.

    :bot: willie.bot.Willie
    :trigger: willie.bot.Willie.Trigger

    """
    #. only log message in the channel not from other IRC users
    if logging and db and trigger.sender.startswith('#'):
        _log(trigger.sender, int(time.time()), trigger.nick, trigger.bytes)
    print trigger.sender, int(time.time()), trigger.nick, trigger.bytes

@willie.module.commands('startlog')
def startlog(bot, trigger):
    """Toggle the log module on."""
    #. Can only be done in privmsg by an admin
    if trigger.sender.startswith('#'):
        return

    if trigger.admin or trigger.owner:
        global logging
        logging = True
        bot.reply('Okay.')

@willie.module.commands('stoplog')
def stoplog(bot, trigger):
    """Toggle the log module off."""
    #. Can only be done in privmsg by an admin
    if trigger.sender.startswith('#'):
        return

    if trigger.admin or trigger.owner:
        global logging
        logging = False
        bot.reply('As you wish.')
