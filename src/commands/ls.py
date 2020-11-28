import argparse
from database.database import DB

__TARGET_ADMIN = 0
__TARGET_FOLLOW = 1


def register(subparsers: argparse._SubParsersAction):
    ls = subparsers.add_parser(
        'ls',
        description='Lists all of [option].',
        help='list all of [option]'
    )
    ls.set_defaults(func=__ls)
    ls_group = ls.add_mutually_exclusive_group(required=True)
    ls_group.add_argument(
        '-a', '--admin',
        action='store_const', dest='target', const=__TARGET_ADMIN,
        help='list the admin users of this server'
    )

    ls_group.add_argument(
        '-f', '--follow',
        action='store_const', dest='target', const=__TARGET_FOLLOW,
        help='list the followed Twitter accounts'
    )
    ls_group.add_argument(
        '-m', '--master',
        action='store_const', dest='target', const=__TARGET_ADMIN,
        help='alias for --admin'
    )


def __ls(args):
    result = {
        __TARGET_ADMIN: __list_admins,
        __TARGET_FOLLOW: __list_follows
    }[args.target]()

    return result


def __list_admins():
    admins = DB['admins'].find()
    if admins.count() == 0:
        return 'None'
    admins = '\n'.join([
        '<@{}>'.format(a['discord_id'])
        for a in admins
    ])
    return admins


def __list_follows():
    follows = DB['follows'].find()
    if follows.count() == 0:
        return 'None'
    follows = '\n'.join([
        '@{} - synced: {}'
        .format(f['account'], f['synced_at'] if 'synced_at' in f else 'never')
        for f in follows
    ])
    return follows
