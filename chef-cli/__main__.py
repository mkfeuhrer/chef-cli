import argparse
import sys
import json
from ChefRequest import makeRequest

def decode(response):
    parsed = json.loads(response.content.decode("utf-8"))
    return json.dumps(parsed, indent=4, sort_keys=True)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contests', required=False, action='store_true',
                        help='Get All Contests')
    parser.add_argument('--contestdetails', required=False, metavar='<ContestDetails>',
                        help='Get details of Contest.Eg- JAN17,APR18')
    parser.add_argument('--countries', required=False, action='store_true',
                        help='Get list of countries')
    parser.add_argument('--institution', '-i', required=False, metavar='<Institution>',
                        help='Institution Filter. Eg: "Motilal Nehru National Institute of Technology"')
    parser.add_argument('--tags', required=False, metavar='<ProblemBasedOnTags>',
                        help='Problem for given tags/authors. eg: jan13,kingofnumber')
    parser.add_argument('--todo', required=False, action='store_true',
                        help='Gets Problems listed in todo')
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

        response="Incorrect request"

        # Arguments initialization
        contests = args.contests
        contestDetails=args.contestdetails
        countries=args.countries
        institution = args.institution
        tags=args.tags
        todo=args.todo
        user = args.user

        # Parser check
        if contests:
            # Make request to fetch list of all contests
            response = decode(makeRequest("GET", "https://api.codechef.com/contests"))

        elif contestDetails:
            # Make request to fetch details of particular contest
            response = decode(makeRequest("GET", "https://api.codechef.com/contests/"+contestDetails))

        elif countries:
            # Make request to fetch list of countries
            response = decode(makeRequest("GET", "https://api.codechef.com/country"))

        elif institution:
            # Make request to search institution
            response = decode(makeRequest("GET", "https://api.codechef.com/institution?search="+institution))

        elif tags:
            # Make request to fetch details of particular all_tags
            response = decode(makeRequest("GET", "https://api.codechef.com/tags/problems?filter="+tags))

        elif todo:
            # Make request to fetch user todo problems
            response = decode(makeRequest("GET", "https://api.codechef.com/todo/problems/"))

        elif user:
            # Make request to fetch user details
            response = decode(makeRequest("GET", "https://api.codechef.com/users/"+user))

        print(response)

    except KeyboardInterrupt:
        print('\nGood Bye.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
