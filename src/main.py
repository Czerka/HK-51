from database.database import DB
from os import getenv
import discord
import shlex
from timeloop import Timeloop
from datetime import timedelta

from twitter.twitter import Twitter
from commands.command_parser import parse


_TOKEN = getenv('DISCORD_TOKEN')
_SERVER = int(getenv('DISCORD_SERVER'))
_CHANNEL = int(getenv('DISCORD_CHANNEL'))
_ADMIN = int(getenv('DISCORD_ADMIN'))
_HK51 = int(getenv('DISCORD_HK51'))

_NO_ORDER_GIVEN = 'Threat: next time you bother me, I will reduce your meatbag \
life to ashes.\nDeclaration: added to order 66 list.'
_ORDER_NOT_FOUND = 'Sad: Data corrupted.\n\
Declaration: Cannot parse order.\n\
Demand: please learn to write.'
_FOLLOW_MSG = 'Declaration: Target acquired. http://www.twitter.com/{}'
_UNFOLLOW_MSG = 'Declaration: Target lost ({}).'
_SERVE_MSG = 'Declaration: {} holds the high ground over me, as well.'
_UNSERVE_MSG = 'Declaration: {} underestimated my power.'

client: discord.Client = discord.Client()
tl = Timeloop()
channel = None


def wrap(text: str, wrapper: str = '```'):
    return wrapper + text + wrapper


@tl.job(interval=timedelta(minutes=15))
def browse_twitter():
    client.dispatch('browse')


@client.event
async def on_browse():
    twitter = Twitter()
    tweets = twitter.fetch(DB['follows'].find())

    for tweet in tweets:
        DB['follows'].update_one({
            'account': tweet['author']
        }, {
            '$set': {'synced_at': tweet['synced_at']}
        })
        await channel.send('https://twitter.com/{}/status/{}'
                           .format(tweet['author'], tweet['twitter_id']))


@client.event
async def on_ready():
    global channel
    channel = client.get_guild(_SERVER).get_channel(_CHANNEL)
    msg = parse('-h')
    await channel.send(wrap(msg))


@client.event
async def on_message(message: discord.Message):
    author: discord.User = message.author._user
    chan: discord.channel.TextChannel = message.channel

    if not any(_HK51 == m.id for m in message.mentions):
        return

    admins = [a['discord_id'] for a in DB['admins'].find()]
    if author.id != _ADMIN and author.id not in admins:
        return

    msg = ' '.join(message.content.split(' ')[1:])
    result = parse(msg)
    await chan.send(wrap(result))

tl.start()
client.run(_TOKEN)
