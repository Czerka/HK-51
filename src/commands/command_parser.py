import argparse
import commands.user as user
import commands.follow as follow
import shlex
import io


class CustomParser(argparse.ArgumentParser):
    def exit(self):
        # this is an override
        raise SyntaxError(self.get_help_string())

    def get_help_string(self):
        stream = io.StringIO('')
        self.print_help(stream)
        return stream.getvalue()

    def error(self, message):
        # this is an override
        response = '{}: error: {}\n'.format(self.prog, message)
        raise SyntaxError(response + self.get_help_string())


def __init_parser():
    parser = CustomParser(
        prog='HK51',
        description='Professional Meatbag Hunter',
        exit_on_error=False
    )
    subparsers = parser.add_subparsers()
    # register commands
    user.register(subparsers)
    follow.register(subparsers)

    return parser


def parse(command: str):
    command = shlex.split(command)
    parser = __init_parser()
    try:
        args = parser.parse_args(command)
        if 'func' in args:
            return args.func(args)
        return wrap(parser.get_help_string())
    except argparse.ArgumentError as error:
        return wrap(parser.get_help_string())
    except SyntaxError as error:
        return wrap(error.msg)
    except Exception as error:
        return wrap(repr(error))


def wrap(text: str, wrapper: str = '```'):
    return wrapper + text + wrapper
