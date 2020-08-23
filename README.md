# HK-51

A bot that will fetch recent tweets from SWTOR related accounts and post them
on the guild's Discord server.

- [HK-51](#hk-51)
  - [Fetching the tweets](#fetching-the-tweets)
  - [Posting the tweets on discord](#posting-the-tweets-on-discord)

## Fetching the tweets

Python script that will fetch the tweets and extract { id, created_at },
writing both to a text file.

## Posting the tweets on discord

HK-51 will read the textfile, and post links to the tweets on Discord.
