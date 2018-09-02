import argparse
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', '-u', required=False, metavar='<Username>',
                        help='Get user information.')
    return parser


def main(argv=None):
    """
    :desc: Entry point method
    """

    if argv is None:
        argv = sys.argv

    try:
        parser = create_parser()
        args = parser.parse_args(argv[1:])

        user = args.user

        if user:
            # Make request to fetch user details .....
            print(user)

    except KeyboardInterrupt:
        print('\nBye.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
