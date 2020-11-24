import argparse
from database.database import Database

__TARGET_ADMIN = 0
__TARGET_FOLLOW = 0


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
        action='store_const', dest='target', const='ADMIN',
        help='list the admin users of this server'
    )

    ls_group.add_argument(
        '-f', '--follow',
        action='store_const', dest='target', const=__TARGET_FOLLOW,
        help='list the followed Twitter accounts'
    )
    ls_group.add_argument(
        '-m', '--master',
        action='store_const', dest='target', const=__TARGET_FOLLOW,
        help='alias for --admin'
    )


def __ls(args):
    result = {
        'ADMIN': __list_admins,
        'FOLLOW': __list_follows
    }[args.target]()

    return result


def __list_admins():
    return 'the list of the admins'


def __list_follows():
    return 'the list of the follows'
