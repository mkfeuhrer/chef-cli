import argparse
import sys
from ChefRequest import makeRequest


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', '-u', required=False, metavar='<Username>',
                        help='Get user information.')
    parser.add_argument('--institution', '-i', required=False, metavar='<Institution>',
                        help='Institution Filter. Eg: "Motilal Nehru National Institute of Technology"')
    parser.add_argument('--contests', required=False, action='store_true',
                        help='Get All Contests')
    parser.add_argument('--contestdetails', required=False, metavar='<ContestDetails>',
                        help='Get details of Contest.Eg- JAN17,APR18')
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

        # Arguments initialization
        user = args.user
        institution = args.institution
        contests = args.contests
        contestDetails=args.contestdetails

        # Parser check
        if user:
            # Make request to fetch user details .....
            print(makeRequest("GET", "https://api.codechef.com/users/"+user).content)

        elif institution:
            # Make request to search institution
            print(makeRequest("GET", "https://api.codechef.com/institution?search="+institution).content)

        elif contests:
            # Make request to fetch list of all contests
            print(makeRequest("GET", "https://api.codechef.com/contests").content)

        elif contestDetails:
            # Make request to fetch details of particular contest
            print(makeRequest("GET", "https://api.codechef.com/contests/"+contestDetails).content)

    except KeyboardInterrupt:
        print('\nBye.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
