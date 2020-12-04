import argparse
from database import DB


def register(subparsers: argparse._SubParsersAction) -> None:
    user = subparsers.add_parser(
        'user',
        description='Manage users.\nA user is a Discord user allowed to issue commands',
        help='manage users'
    )
    user.set_defaults(func=__user)
    user_group = user.add_mutually_exclusive_group(required=True)
    user_group.add_argument(
        '-a', '--add',
        help='set the tagged user as a user of HK'
    )
    user_group.add_argument(
        '-r', '--remove',
        help='remove the tagged user from HK users'
    )
    user_group.add_argument(
        '-l', '--list',
        action='store_true',
        help='list the current users of HK'
    )


def __user(args) -> str:
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
    users = DB['users'].find()
    if users.count() == 0:
        return 'None'
    users = '\n'.join([
        '- <@{}>'.format(u['discord_id'])
        for u in users
    ])
    return users


def __add(user: str) -> str:
    # Need to extract id from this format :
    # <@!243843303483768832>
    try:
        if '<@!' not in user:
            raise Exception()
        user = user[3:-1]
    except Exception:
        return '[Threat] Stupid meatbag. This is not a valid Discord user.'

    DB['users'].insert_one({'discord_id': user})
    return '[Anger] <@!{}> has the high ground over me.'.format(user)


def __remove(user: str) -> str:
    try:
        if '<@!' not in user:
            raise Exception()
        user = user[3:-1]
    except Exception:
        return '[Threat] Stupid meatbag. This is not a valid Discord user.'

    DB['users'].delete_one({'discord_id': user})
    return '[Satistaction] <@!{}> underestimated my power.'.format(user)
