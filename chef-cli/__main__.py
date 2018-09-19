import argparse
import sys
import json
import csv
import os
from ChefRequest import makeRequest

def decode(response):
    return json.loads(json.dumps(response.json()['result']))

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contests', required=False, action='store_true',
                        help='Get All Contests')
    parser.add_argument('--contestdetails', required=False, metavar='<ContestDetails>',
                        help='Get details of Contest.Eg- JAN17,APR18')
    parser.add_argument('--countries', required=False, action='store_true',
                        help='Get list of countries')
    parser.add_argument('--institution', required=False, metavar='<Institution>',
                        help='Institution Filter. Eg: "Motilal Nehru National Institute of Technology"')
    parser.add_argument('--languages', required=False, action='store_true',
                        help='Get list of languages on codechef')
    parser.add_argument('--tags', required=False, metavar='<ProblemBasedOnTags>',
                        help='Problem for given tags/authors. eg: jan13,kingofnumber')
    parser.add_argument('--todo', required=False, action='store_true',
                        help='Gets Problems listed in todo')
    parser.add_argument('--user', required=False, metavar='<Username>',
                        help='Get user information.')
    parser.add_argument('--compare', required=False, nargs=2, metavar=('<Username1>','<Username2>'),
                        help='Compare two user profiles eg: vijju123 kingofnumber')
    parser.add_argument('--submit', required=False,  nargs=3, metavar=('<CodeFilePath>', '<Language>' , '<InputString>'),
                        help='Submit and get output of code for a input.\nRequires three argument: codeFilePath, language and input string.\n E.g ./a.cpp C++ 4.3.2 Mohit \n If no input leave use -> ""\n.Check languages available using --languages')
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
        contests = args.contests
        contestDetails=args.contestdetails
        countries=args.countries
        institution = args.institution
        languages=args.languages
        tags=args.tags
        todo=args.todo
        user=args.user
        compare=args.compare
        submit=args.submit

        # Parser check
        if compare:
            #Compare two user profiles
            compareProfiles(compare)

        elif contests:
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

        elif languages:
            response = decode(makeRequest("GET", "https://api.codechef.com/language"))
            languagesList = response.get("data","Not Found").get("content","Not Found")
            print("\n---------------------List of Languages---------------------\n")
            for lang in languagesList:
                print(lang.get("shortName",""))

        elif submit:
            # Submit and run code for output
            submitCode(submit)

        elif tags:
            # Make request to fetch details of particular all_tags
            response = decode(makeRequest("GET", "https://api.codechef.com/tags/problems?filter="+tags))

        elif todo:
            # Make request to fetch user todo problems
            response = decode(makeRequest("GET", "https://api.codechef.com/todo/problems/"))

        elif user:
            # Make request to fetch user details
            response = decode(makeRequest("GET", "https://api.codechef.com/users/"+user))

        # print(json.dumps(response, indent=4, sort_keys=True))

    except KeyboardInterrupt:
        print('\nGood Bye.')
    return 0

def submitCode(submit):
    parameters = {}
    file = open(submit[0], "r")
    parameters['sourceCode'] = file.read();
    parameters['language'] = submit[1];
    parameters['input'] = submit[2];
    response = makeRequest("POST", "https://api.codechef.com/ide/run", parameters)
    result = response.json().get('result',"error").get('data',"").get("link","")
    response = decode(makeRequest("GET", "https://api.codechef.com/ide/status?link="+result))

    print("\n---------------------Submission Result---------------------\n")
    print("Input :\n"+response.get('data',"").get('input')+"\n")
    print("Compiler :"+response.get('data',"").get('langVersion')+"\n")
    print("Output :\n"+response.get('data',"").get('output')+"\n")
    if(response.get('data',"").get('stderr') != ""):
        print("Std Error :\n"+response.get('data',"").get('stderr'))
    if(response.get('data',"").get('cmpinfo') != ""):
        print("Compilation Result :\n"+response.get('data',"").get('cmpinfo'))
    print("-------------------------------------------------------------\n")

    return 0

def compareProfiles(compare):

    user1 = compare[0]
    user2 = compare[1]
    response1 = decode(makeRequest("GET", "https://api.codechef.com/users/"+compare[0]))
    response2 = decode(makeRequest("GET", "https://api.codechef.com/users/"+compare[1]))

    data = []
    ranks = []
    columnNames = ["Details"]
    columnNames.append("User1");
    columnNames.append("User2");
    ranks.append(columnNames)
    data.append(columnNames)

    username1 = response1['data']['content']['username']
    username2 = response2['data']['content']['username']
    usernames = ["Username"]
    usernames.append(username1)
    usernames.append(username2)
    data.append(usernames)

    name1 = response1['data']['content']['fullname']
    name2 = response2['data']['content']['fullname']
    names = ["Names"]
    names.append(name1)
    names.append(name2)
    data.append(names)

    ranking1 = response1['data']['content']['rankings']['allContestRanking']['global']
    ranking2 = response2['data']['content']['rankings']['allContestRanking']['global']
    rankings = ["Rankings"]
    rankings.append(str(ranking1))
    rankings.append(str(ranking2))
    data.append(rankings)
    ranks.append(rankings)

    Lranking1 = response1['data']['content']['rankings']['longRanking']['global']
    Lranking2 = response2['data']['content']['rankings']['longRanking']['global']
    Lrankings = ["Long Rankings"]
    Lrankings.append(str(Lranking1))
    Lrankings.append(str(Lranking2))
    ranks.append(Lrankings)
    data.append(Lrankings)

    Sranking1 = response1['data']['content']['rankings']['shortRanking']['global']
    Sranking2 = response2['data']['content']['rankings']['shortRanking']['global']
    Srankings = ["Short Rankings"]
    Srankings.append(str(Sranking1))
    Srankings.append(str(Sranking2))
    ranks.append(Srankings)
    data.append(Srankings)

    print("\n---------------------Profile Comparision---------------------\n")
    col_width = max(len(word) for row in data for word in row) + 2
    for row in data:
        print("\t".join(word.ljust(col_width) for word in row))
    print("\n-------------------------------------------------------------\n")

    # Make data here
    # with open("compare_profile.csv",mode="w") as file:
    #     file_writer = csv.writer(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     for rank in ranks:
    #         file_writer.writerow(rank)
    # Print graph
    # os.system('termgraph compare_profile.csv --color {blue,red}')
    return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
