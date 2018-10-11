import argparse
import sys
import json
import csv
import os
import requests
import collections
from chefcli.ChefRequest import makeRequest
from chefcli.ChefParser import CodeChefHTMLParser
from datetime import datetime
from termcolor import colored


def decode(response):
    return json.loads(json.dumps(response.json()['result']))


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contests', required=False, action='store_true',
                        help='Get All Contests')
    parser.add_argument('--contestdetails', required=False, metavar='<ContestDetails>',
                        help='Get details of Contest.Eg- JAN17,APR18')
    parser.add_argument('--country', required=False, metavar='<Search country string>',
                        help='Search country from available countries')
    parser.add_argument('--institution', required=False, metavar='<Institution>',
                        help='Institution Filter. Eg: "Motilal Nehru National Institute of Technology"')
    parser.add_argument('--languages', required=False, action='store_true',
                        help='Get list of languages on codechef')
    parser.add_argument('--tags', required=False, metavar='<ProblemBasedOnTags>',
                        help='Problem for given tags/authors. eg: jan13,kingofnumber')
    parser.add_argument('--user', required=False, metavar='<Username>',
                        help='Get user information.')
    parser.add_argument('--compare', required=False, nargs=2, metavar=('<Username1>', '<Username2>'),
                        help='Compare two user profiles eg: vijju123 kingofnumber')
    parser.add_argument('--submit', required=False, nargs=3, metavar=('<CodeFilePath>', '<Language>', '<InputString>'),
                        help='Submit and get output of code for a input.\nRequires three argument: codeFilePath, language and input string.\n E.g ./a.cpp C++ 4.3.2 Mohit \n If no input leave use -> ""\n.Check languages available using --languages')
    parser.add_argument('--rankings', required=False, action='store_true',
                        help='Get Institute wise ranking list a.k.a Chef-cli ratings')
    parser.add_argument('--recommend', required=False, metavar='<Username>',
                        help='Get problem recommendation for a particular user.')
    parser.add_argument('--graph', required=False, metavar='<Username',
                        help='Get submission graph for a particluar user.')
    parser.add_argument('--problem', required=False, nargs=2, metavar=(
        '<ContestCode>', '<ProblemCode>'), help='Get details of a particular Problem')
    parser.add_argument('--sampleSubmit', required=False, nargs=4, metavar=('<ContestCode>', '<ProblemCode>',
                                                                            '<CodeFilePath>', '<Language>'), help='Submit a problem to check if it passes sample test cases.')
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
        contestDetails = args.contestdetails
        country = args.country
        institution = args.institution
        languages = args.languages
        tags = args.tags
        user = args.user
        compare = args.compare
        submit = args.submit
        graph_user = args.graph
        rankings = args.rankings
        recommend_user = args.recommend
        problem = args.problem
        sampleSubmit = args.sampleSubmit

        # Parser check
        if compare:
            # Compare two user profiles
            compareProfiles(compare)

        elif contests:
            # Make request to fetch list of all contests
            print(colored("\n-----------Active Contests-----------\n\n", "yellow"))
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/contests?status=present"))
            contestList = response.get('data', "").get(
                'content', "").get('contestList', "")
            for contest in contestList:
                print(colored("-------------------------------------", "yellow"))
                print(colored("\tCode : ", "blue") + contest.get("code"))
                print(colored("\tName : ", "blue") + contest.get("name"))
                print(colored("\tStart Date : ", "blue") + contest.get("startDate"))
                print(colored("\tEnd Date : ", "blue") + contest.get("endDate"))

            print(colored("\n-----------Future Contests-----------\n", "yellow"))
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/contests?status=future"))
            contestList = response.get('data', "").get(
                'content', "").get('contestList', "")
            for contest in contestList:
                print(colored("-------------------------------------", "yellow"))
                print(colored("\tCode : ", "blue") + contest.get("code"))
                print(colored("\tName : ", "blue") + contest.get("name"))
                print(colored("\tStart Date : ", "blue") + contest.get("startDate"))
                print(colored("\tEnd Date : ", "blue") + contest.get("endDate"))
            print(colored("-------------------------------------\n", "yellow"))

        elif contestDetails:
            # Make request to fetch details of particular contest
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/contests/" + contestDetails))
            contestDetails = response.get('data', "").get('content', "")
            print(colored("-------------------------------------\n", "yellow"))
            print(colored("\tContest : ", "blue") + contestDetails.get("name", ""))
            print(colored("\nProblem Code : Successful Submissions", "yellow"))
            print(colored("-------------------------------------\n", "yellow"))
            problemList = contestDetails.get("problemsList", "")
            for problem in problemList:
                print(colored("\t" + str(problem.get("problemCode", "")), "blue") + " : " +
                      str(problem.get("successfulSubmissions", "")))
            print(colored("-------------------------------------\n", "yellow"))

        elif country:
            # Make request to fetch list of countries
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/country?search=" + country))
            countriesList = response.get('data', "No results found").get(
                'content', "No results found")
            print(colored("\n-------------------------------------", "yellow"))
            print(colored("\nList of matching countries\n", "yellow"))
            for country in countriesList:
                print(colored("\t" + country.get("countryName", ""), "blue"))
            print(colored("\n-------------------------------------\n", "yellow"))

        elif graph_user:
            # Display submission graph of the user
            submissionGraph(graph_user)

        elif institution:
            # Make request to search institution
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/institution?search=" + institution))
            # print(response)
            instituteList = response.get('data', "No resuls found").get(
                'content', "No results found")
            print(colored("\n-------------------------------------", "yellow"))
            print(colored("\nList of matching intitutes\n", "yellow"))
            for institute in instituteList:
                print("\t" + colored(institute.get("institutionName", ""), "blue"))
            print(colored("\n-------------------------------------\n", "yellow"))

        elif languages:
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/language"))
            languagesList = response.get(
                "data", "Not Found").get("content", "Not Found")
            print(colored("\n---------------------List of Languages---------------------\n", "yellow"))
            for lang in languagesList:
                print("\t" + colored(lang.get("shortName", ""), "blue"))
            print(colored("\n-------------------------------------\n", "yellow"))

        elif problem:
            # Display details of a problem
            renderProblem(problem)

        elif rankings:
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/contests?status=past&limit=20&sortOrder=desc"))
            contestList = response.get('data',"").get('content',"").get('contestList',"")
            contests = []
            months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEPT','OCT','NOV','DEC']
            for contest in contestList:
                name = contest['name']
                code = contest['code']
                if code.find("COOK") != -1 or code.find("LTIME") != -1:
                    contests.append(code+"A")
                    contests.append(code+"B")
                for month in months:
                    if code.find(month) != -1 and name.find("Challenge") != -1:
                        contests.append(code+"A")
                        contests.append(code+"B")
            contests.sort()
            check = {}
            for contest in contests:
                check[contest] = -1
            for contest in contests:
                code = contest
                if check[code] == -1:
                    for con in contests:
                        if con == code:
                            continue
                        if(con.find(code) != -1):
                            check[con] = 0
            res = []
            for key in check:
                if check[key] == -1:
                    res.append(key)
            res.sort()
            instituteRanks = {}
            instituteCount = {}
            print(colored("\n-------------------------------------\n", "yellow"))
            print(colored("\nFollowing contests are considered for ranking the institutes\n", "yellow"))
            for contest in res:
                print(colored(contest, "blue"))
                currentInstitute = {}
                response = decode(makeRequest(
                    "GET", "https://api.codechef.com/rankings/" + contest + "?institutionType=College"))
                # print(response)
                ranklist = response.get('data',"").get('content',"")
                for rankDetail in ranklist:
                    rank = int(rankDetail.get("rank"))
                    institute = rankDetail.get("institution")
                    if institute in instituteRanks:
                        if institute in currentInstitute:
                            currentInstitute[institute] = currentInstitute[institute] + 1
                        else:
                            currentInstitute[institute] = 1
                        if currentInstitute[institute] > 25:
                            continue
                        instituteRanks[institute] = instituteRanks[institute] + rank
                        instituteCount[institute] = instituteCount[institute] + 1
                    else:
                        currentInstitute[institute] = 1
                        instituteRanks[institute] = rank
                        instituteCount[institute] = 1
                for institute in currentInstitute:
                    if(currentInstitute[institute] < 25):
                        instituteRanks[institute] = instituteRanks[institute] + (25-currentInstitute[institute])*300
            result = {}
            result1 = {}
            for key in instituteRanks:
                result[key] = int(instituteRanks[key]/instituteCount[key])
            result1 = sorted(result.items(), key=lambda x: x[1])
            print(colored("\n-----------Institute wise ranklist based on events listed above------------\n", "yellow"))
            print(colored("\n\tCollege Name : College Rating\n", "yellow"))
            for key in result1:
                print(colored(key[0] + " : ", "blue") + str(key[1]))
            print(colored("\n----------------------------------------------------------------\n", "yellow"))

        elif recommend_user:
            # Recommend problems to a user based on the previous problems that he solved
            response = requests.get(
                "http://149.129.139.203:5000/api/recommend/user/" + recommend_user).json()
            problem_list = response.get("recommendedProblems", [])

            print(colored("\n-------------------------------------", "yellow"))
            print(colored("\nList of recommended problems\n", "yellow"))

            for problem in problem_list[:10]:
                print("\t" + colored(problem, "blue"))

            print(colored("\n-------------------------------------\n", "yellow"))

        elif submit:
            # Submit and run code for output
            submitCode(submit)

        elif sampleSubmit:
            # Submit problem and check it's correctness on sample testcases
            sampleSubmitCode(sampleSubmit)

        elif tags:
            # Make request to fetch details of particular all_tags
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/tags/problems?filter=" + tags))
            problem_tags = response.get(
                "data", "Not Found").get("content", "Not Found")
            print(colored("\n-------------------------------------\n", "yellow"))
            print(colored("Problem code : Solved count\n", "yellow"))
            for key in problem_tags.keys():
                val = problem_tags[key]
                for keys in problem_tags[key]:
                    if keys == "solved":
                        solved = str(val[keys])
                print("\t" + colored(key, "blue") + " : " + solved)
            print(colored("\n-------------------------------------\n", "yellow"))

        elif user:
            # Make request to fetch user details
            response = decode(makeRequest(
                "GET", "https://api.codechef.com/users/" + user))

            user = response.get("data", "Not Found").get(
                "content", "Not Found")

            print(colored("\n--------------User Details-----------------------\n", "yellow"))
            print("\t" + colored("Name          : ", "blue") + str(user.get("fullname", "")))
            print("\t" + colored("City          : ", "blue") + str(user.get("city", "").get("name", "")))
            print("\t" + colored("State         : ", "blue") + str(user.get("state", "").get("name", "")))
            print("\t" + colored("Country       : ", "blue") + str(user.get("country", "").get("name", "")))
            print("\t" + colored("Band          : ", "blue") + str(user.get("band", "")))
            print(colored("\n--------------Problem Stats-----------------------\n", "yellow"))
            print("\t" + colored("Partially Solved     : ", "blue") + str(user.get("submissionStats",
                                                           "").get("partiallySolvedProblems", "")))
            print("\t" + colored("Completely Solved    : ", "blue") +
                  str(user.get("submissionStats", "").get("solvedProblems", "")))
            print("\t" + colored("Solutions Submitted  : ", "blue") +
                  str(user.get("submissionStats", "").get("submittedSolutions", "")))
            print("\t" + colored("AC Submissions       : ", "blue") +
                  str(user.get("submissionStats", "").get("acceptedSubmissions", "")))
            print("\t" + colored("Wrong Submissions    : ", "blue") +
                  str(user.get("submissionStats", "").get("wrongSubmissions", "")))
            print(colored("\n--------------Rating Stats-----------------------\n", "yellow"))
            print("\t" + colored("Overall  : ", "blue") + str(user.get("ratings", "").get("allContest", "")))
            print("\t" + colored("Long     : ", "blue") + str(user.get("ratings", "").get("long", "")))
            print("\t" + colored("Short    : ", "blue") + str(user.get("ratings", "").get("short", "")))
            print("\t" + colored("LTime    : ", "blue") + str(user.get("ratings", "").get("lTime", "")))
            print(colored("\n-------------------------------------------------\n", "yellow"))

    except KeyboardInterrupt:
        print('\nGood Bye.')
    return 0


def submitCode(submit):
    parameters = {}
    file = open(submit[0], "r")
    parameters['sourceCode'] = file.read()
    parameters['language'] = submit[1]
    parameters['input'] = submit[2]
    response = makeRequest(
        "POST", "https://api.codechef.com/ide/run", parameters)
    result = response.json().get('result', "error").get('data', "").get("link", "")
    response = decode(makeRequest(
        "GET", "https://api.codechef.com/ide/status?link=" + result))

    print("\n---------------------Submission Result---------------------\n")
    print("Input :\n" + response.get('data', "").get('input') + "\n")
    print("Compiler :" + response.get('data', "").get('langVersion') + "\n")
    print("Output :\n" + response.get('data', "").get('output') + "\n")
    if(response.get('data', "").get('stderr') != ""):
        print("Std Error :\n" + response.get('data', "").get('stderr'))
    if(response.get('data', "").get('cmpinfo') != ""):
        print("Compilation Result :\n" + response.get('data', "").get('cmpinfo'))
    print("-------------------------------------------------------------\n")

    return 0


def compareProfiles(compare):

    user1 = compare[0]
    user2 = compare[1]
    response1 = decode(makeRequest(
        "GET", "https://api.codechef.com/users/" + compare[0]))
    response2 = decode(makeRequest(
        "GET", "https://api.codechef.com/users/" + compare[1]))

    data = []
    ranks = []
    columnNames = ["Details"]
    columnNames.append("User1")
    columnNames.append("User2")
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

    print(colored("\n---------------------Profile Comparision---------------------\n", "yellow"))
    col_width = max(len(word) for row in data for word in row) + 2
    for row in data:
        print("\t".join(word.ljust(col_width) for word in row))
    print(colored("\n-------------------------------------------------------------\n", "yellow"))

    ranks.pop(0)
    header_columns = ['@ ' + name1, name2]

    # Make data here
    with open("compare_profile.dat", mode="w") as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_columns)
        for rank in ranks:
            file_writer.writerow(rank)
    # Print graph
    os.system('termgraph compare_profile.dat --color {blue,red}')
    os.system('rm compare_profile.dat')
    return


def submissionGraph(user):
    # Experimental feature currently prints the submission graph for only last 600 submissions.
    # Limitation is due to 30 API call restirction on Submission API in 5 minutes.

    offset = 0
    submissions = collections.OrderedDict()
    now = datetime.now()
    end = datetime(now.year - 1, now.month, now.day, now.hour,
                   now.minute, now.second, now.microsecond)
    end = str(end)

    for i in range(1, 30):

        response = makeRequest(
            "GET", "https://api.codechef.com/submissions/?username=" + user + "&limit=20&offset=" + str(offset)).json()
        submission = response.get("result", {}).get(
            "data", {}).get("content", [])

        date = "1970-01-01 00:00:00"

        for sub in submission:

            date = sub.get("date", "1970-01-01 00:00:00").split(" ")[0]
            if submissions.get(date, ""):
                submissions[date] += 1
            else:
                submissions[date] = 1

        if end.split(" ")[0] > date.split(" ")[0]:
            break

        offset += 20

    startDate = end.split(" ")[0]

    sorted_submissions = collections.OrderedDict(sorted(submissions.items()))

    with open("submission_graph.dat", mode="w") as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        for key, value in sorted_submissions.items():
            file_writer.writerow([key, value])

    print(colored("\n-------------------------------------\n", "yellow"))
    print(colored("\tSubmission graph", "yellow"))

    os.system("termgraph --calendar --start-dt " +
              startDate + " submission_graph.dat")
    os.system('rm submission_graph.dat')
    print(colored("\n-------------------------------------\n", "yellow"))

def renderProblem(problem):

    response = makeRequest(
        "GET", "https://api.codechef.com/contests/{0}/problems/{1}".format(problem[0], problem[1])).json()

    data = response.get("result", {}).get(
        "data", {}).get("content", {}).get("body", "")

    parser = CodeChefHTMLParser()
    parser.feed(data)

    data = parser.getProblemStatement()

    file = open("data.md", "w")
    file.write(data)
    file.close()

    os.system("mdv data.md")
    os.remove("data.md")


def sampleSubmitCode(sampleSubmit):

    response = makeRequest(
        "GET", "https://api.codechef.com/contests/{0}/problems/{1}".format(sampleSubmit[0], sampleSubmit[1])).json()

    data = response.get("result", {}).get(
        "data", {}).get("content", {}).get("body", "")

    parser = CodeChefHTMLParser()
    parser.feed(data)

    data = parser.getSampleInput()

    parameters = {}
    file = open(sampleSubmit[2], "r")
    parameters['sourceCode'] = file.read()
    parameters['language'] = sampleSubmit[3]
    parameters['input'] = data

    response = makeRequest(
        "POST", "https://api.codechef.com/ide/run", parameters)
    result = response.json().get('result', "error").get('data', "").get("link", "")
    response = decode(makeRequest(
        "GET", "https://api.codechef.com/ide/status?link=" + result))

    if response.get('data', "").get('output') == parser.getSampleOutput():
        print(colored('\nSample Test Cases Passed Successfully', 'green'))
    else:
        print(colored('\nSample Test Cases Failed', 'red'))

    print("\n---------------------Submission Result---------------------\n")
    print("Sample Input :\n" + response.get('data', "").get('input') + "\n")
    print("Compiler :" + response.get('data', "").get('langVersion') + "\n")
    print("Your Output :\n" + response.get('data', "").get('output') + "\n")
    print("Sample Output : \n" + parser.getSampleOutput() + "\n")
    if(response.get('data', "").get('stderr') != ""):
        print("Std Error :\n" + response.get('data', "").get('stderr'))
    if(response.get('data', "").get('cmpinfo') != ""):
        print("Compilation Result :\n" + response.get('data', "").get('cmpinfo'))
    print("-------------------------------------------------------------\n")


if __name__ == '__main__':
    sys.exit(main(sys.argv))
