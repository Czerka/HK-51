import argparse
from database import DB


def register(subparsers: argparse._SubParsersAction) -> None:
    follow = subparsers.add_parser(
        'follow',
        description='Manage follows.\nA follow is represented as a Twitter\
            account, whose tweets will be shared.',
        help='manage follows'
    )
    follow.set_defaults(func=__follow)
    follow_group = follow.add_mutually_exclusive_group(required=True)
    follow_group.add_argument(
        '-a', '--add',
        help='add the given twitter account to HK\'s watch list'
    )
    follow_group.add_argument(
        '-r', '--remove',
        help='remove the given twitter account from HK\'s watch list'
    )
    follow_group.add_argument(
        '-l', '--list',
        action='store_true',
        help='display HK\'s current watch list'
    )


def __follow(args) -> str:
    if args.list:
        return __list()
    if args.add is not None:
        return __add(args.add)
    if args.remove is not None:
        return __remove(args.remove)
    raise Exception(
        'No behavioural function found for : {}'.format(repr(args))
    )


def __list() -> str:
    follows = DB['follows'].find()
    if follows.count() == 0:
        return 'None'

    width = max(map(lambda f: len(f['account']), follows))
    follows.rewind()

    follows = '\n'.join([
        '@{:<{}} - synced: {}'
        .format(f['account'], width, f['synced_at'] if 'synced_at' in f else 'never')
        for f in follows
    ])

    return '```' + follows + '```'


def __add(account: str) -> str:
    DB['follows'].insert_one({'account': account})
    return '[Declaration] Target acquired: http://www.twitter.com/{}'.format(account)


def __remove(account: str) -> str:
    DB['follows'].delete_one({'account': account})
    return '[Declaration] Target lost ({})'.format(account)
