from database import Database
from os import getenv
from twitter import Twitter
from timeloop import Timeloop
from datetime import timedelta
import discord

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
_UP_MSG = 'Announcement: this unit has been sent to provide news \
and liquidate meatbags. Fortunately, this unit is currently out of news.\n\
Declaration: Remember, nobody is born cool, except, of course, \
my maker <@{0}>'.format(_ADMIN)
if getenv('APP_ENV') == 'dev':
    _UP_MSG = '[DEV]' + _UP_MSG
_HELP_MSG = 'Declaration: let me walk you through my functions, \
helpless meatbag. Do not forget to tag me.\n\
- help: if you do not figure this out, you should be terminated.\n\
- follow <account>: I will target the given meatbag account. Any tweet will be\
crossposted into #general\n\
- unfollow <account>: I will not target this specific account anymore.\n\
- serve <@member>: I will now serve the mentionned member as well.\n\
- unserve <@member>: I will terminate the servitude contract with this meatbag.\
- ls-f: I will list all currently targeted tweet accounts.\
- ls-a: I will list all currently served masters and mistresses'
_FOLLOW_MSG = 'Declaration: Target acquired. http://www.twitter.com/{}'
_UNFOLLOW_MSG = 'Declaration: Target lost ({}).'
_SERVE_MSG = 'Declaration: {} holds the high ground over me, as well.'
_UNSERVE_MSG = 'Declaration: {} underestimated my power.'

db = Database()
client: discord.Client = discord.Client()
tl = Timeloop()
channel = None


@tl.job(interval=timedelta(minutes=15))
def browse_twitter():
    client.dispatch('browse')


def parse_order(message: discord.Message):
    msg = message.content.split(' ')
    msg = filter(lambda word: len(word) > 0, msg)
    msg = list(msg)[1:]

    if len(msg) == 0:
        return _NO_ORDER_GIVEN

    if msg[0] == 'help':
        return _HELP_MSG

    if msg[0] == 'ls-f':
        return '\n'.join(['`@{} - synced: {}`'.format(f['account'], f['synced_at'] if 'synced_at' in f else 'never') for f in db.list_follows()])

    if msg[0] == 'ls-a':
        return '\n'.join(['<@{}>'
                          .format(a['discord_id']) for a in db.list_admins()])

    if msg[0] == 'fetch':
        client.dispatch('browse')
        return 'Fetching...'

    if msg[0] == 'follow' and len(msg) == 2:
        if not db.find_follow(msg[1]):
            db.store_follow(msg[1])
        return _FOLLOW_MSG.format(msg[1])

    if msg[0] == 'unfollow' and len(msg) == 2:
        db.delete_follow(msg[1])
        return _UNFOLLOW_MSG.format(msg[1])

    if msg[0] == 'serve' and len(msg) == 2 and '@' in msg[1]:
        mention = list(filter(lambda m: m.id != _HK51, message.mentions))[0]
        db.store_admin(mention._user.id)
        return _SERVE_MSG.format(msg[1])

    if msg[0] == 'unserve' and len(msg) == 2 and '@' in msg[1]:
        mention = list(filter(lambda m: m.id != _HK51, message.mentions))[0]
        db.delete_admin(mention._user.id)
        return _UNSERVE_MSG.format(msg[1])

    return _ORDER_NOT_FOUND


@client.event
async def on_browse():
    twitter = Twitter()
    tweets = twitter.fetch(db.list_follows())

    for tweet in tweets:
        # should store here
        db.update_follow(tweet['author'], tweet['synced_at'])
        await channel.send('https://twitter.com/{}/status/{}'
                           .format(tweet['author'], tweet['twitter_id']))


@client.event
async def on_ready():
    global channel
    print('server: {}, channel: {}'.format(_SERVER, _CHANNEL))
    channel = client.get_guild(_SERVER).get_channel(_CHANNEL)
    await channel.send(_UP_MSG)


@client.event
async def on_message(message: discord.Message):
    author: discord.User = message.author._user
    chan: discord.channel.TextChannel = message.channel

    if chan.id != _CHANNEL:
        return
    if not any(_HK51 == m.id for m in message.mentions):
        return

    admins = [a['discord_id'] for a in db.list_admins()]
    if author.id == _ADMIN or author.id in admins:
        result = parse_order(message)
        await channel.send(result)

tl.start()
client.run(_TOKEN)
