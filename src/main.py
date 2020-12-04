from database import DB
from os import getenv
import discord
from discord.ext.commands import Bot
from timeloop import Timeloop
from datetime import timedelta

from twitter import Twitter
from commands.command_parser import parse


_TOKEN = getenv('DISCORD_TOKEN')
_SERVER = int(getenv('DISCORD_SERVER'))
_CHANNEL = int(getenv('DISCORD_CHANNEL'))
_ADMIN = int(getenv('DISCORD_ADMIN'))
_HK51 = int(getenv('DISCORD_HK51'))

intents = discord.Intents.all()
client: discord.Client = discord.Client(intents=intents)
tl = Timeloop()
channel = None


@ tl.job(interval=timedelta(minutes=15))
def browse_twitter():
    client.dispatch('browse')


@ client.event
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


@ client.event
async def on_ready():
    global channel
    channel = client.get_guild(_SERVER).get_channel(_CHANNEL)
    msg = parse('-h')
    await channel.send(msg)


@ client.event
async def on_member_join(member: discord.Member):
    msg = DB['settings'].find_one({'key': 'welcome_message'})
    if msg is None:
        return

    await channel.send('{} {}'.format(member.mention(), msg['value']))


@ client.event
async def on_message(message: discord.Message):
    author: discord.User = message.author._user
    chan: discord.channel.TextChannel = message.channel

    if not any(_HK51 == m.id for m in message.mentions):
        return

    users = [u['discord_id'] for u in DB['users'].find()]
    if author.id != _ADMIN and author.id not in users:
        return
    if author.is_bot:
        return

    msg = ' '.join(message.content.split(' ')[1:])
    result = parse(msg)
    await chan.send(result)

tl.start()
client.run(_TOKEN)
