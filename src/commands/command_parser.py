import argparse
import commands.ls as ls


def __init_parser():
    parser = argparse.ArgumentParser(
        prog='HK51',
        description='Professional Meatbag Hunter'
    )
    subparsers = parser.add_subparsers()
    ls.register(subparsers)
    return parser


def parse(command: str):
    parser = __init_parser()
    args = parser.parse_args(command)
    return args.func(args)
