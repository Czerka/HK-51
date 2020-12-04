import argparse
from database import DB


def register(subparsers: argparse._SubParsersAction) -> None:
    welcome = subparsers.add_parser(
        'welcome',
        description='Manage the welcome message.\nThe welcome message is sent\
            to every new member upon joining the server.',
        help='manage welcome message'
    )
    welcome.set_defaults(func=__welcome)
    welcome_group = welcome.add_mutually_exclusive_group(required=True)
    welcome_group.add_argument(
        '-u', '--update',
        help='set the welcome message for this server'
    )
    welcome_group.add_argument(
        '-s', '--show',
        action='store_true',
        help="show the welcome message"
    )


def __welcome(args) -> str:
    if args.show:
        return __show()
    if args.update is not None:
        return __update(args.update)
    raise Exception(
        'No behavioural function found for : {}'.format(repr(args))
    )


def __show():
    msg = DB['settings'].find_one({'key': 'welcome_message'})
    if msg is None:
        return '`None`'
    return '```' + msg['value'] + '```'


def __update(msg: str) -> str:
    DB['settings'].update_one({
        'key': 'welcome_message'
    }, {
        '$set': {'value': msg}
    }, True)
    return '[Affirmation] Welcome message updated.'
