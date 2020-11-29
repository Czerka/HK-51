# HK-51

Our beloved meatbag hunter acts as a Discord bot to help Crimson Wind,
a European SWTOR guild, managing events, and sharing news regarding the game.

## Features

- Users management
- Follows management
- Welcome message
- Tweet sharing
- Event scheduling

### Command parsing

Usually, you issue commands to bots by starting the message with a `.` or a `!`.
I don't think it is a good idea, especially in modern times where several bots usually
run under the same Discord server.

You can issue commands to HK by tagging it. `@HK-51 [...]`.

Regarding the commands themselves, I decided to follow UNIX style commands, options and arguments.

```
usage: HK51 [-h] {user,follow} ...

Professional Meatbag Hunter

positional arguments:
  {user,follow}
    user         manage users
    follow       manage follows

optional arguments:
  -h, --help     show this help message and exit
```

### Users management

HK keeps track of who is allowed to issue commands to it.
```
usage: HK51 user [-h] (-a ADD | -r REMOVE | -l)

Manage users. A user is a Discord user allowed to issue commands

optional arguments:
  -h, --help            show this help message and exit
  -a ADD, --add ADD     set the tagged user as a user of HK
  -r REMOVE, --remove REMOVE
                        remove the tagged user from HK users
  -l, --list            list the current users of HK
```

### Follows management

HK keeps track of given Twitter accounts, and will look for new tweets.
```
usage: HK51 follow [-h] (-a ADD | -r REMOVE | -l)

Manage follows. A follow is represented as a Twitter account, whose tweets
will be shared.

optional arguments:
  -h, --help            show this help message and exit
  -a ADD, --add ADD     add the given twitter account to HK's watch list
  -r REMOVE, --remove REMOVE
                        remove the given twitter account from HK's watch list
  -l, --list            list the current watch list
```

### Welcome message

Currently not configurable, the welcome message is sent to any newcomer to the Discord server.

### Tweet sharing

HK will keep track of a list of twitter accounts of your choosing. Regularily (currently every 15 minutes),
it will share on Discord every new original tweet from those account.

### Scheduling

[Currently WIP - details to be provided later.]

## How does it work ?

HK uses a generic MongoDB container alongside a Python application to run those features.

The official libraries are used to interact with both Discord and Twitter.

The code in itself should be very straight forward.

## How can I get it for my personal use ?

Good question, meatbag. The answer is quite lengthy, and I would prefer to write down a complete and detailed wiki page rather than sum it up here. If the wiki page does not exists yet, you can contact me directly. Opening an issue is fine as the project is small right now.

## Contributing

First, thank you.

Second, before creating any issues, make sure one does not already exists for the matter at hand. You can create issues for any kind of problem you might encounter or feature request you might have.

Third, feel free to fork the repo, start working on an issue, create a pull request, and wait for it to be pulled.

Fourth, I will do my very best to manage the open-source side of things to the top of my abilities, although I am not very experienced in the matter. Any advices, workflow upgrades, will be received with great interest.
