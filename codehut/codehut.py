import requests
import argparse
import json
import webbrowser

from helper_scripts import get_codeforces_by_rating, get_submission_codeforces

URL = "https://codeforces.com/api/"

def connect_login(args):
    # Verify user and add it to info.json file
    # Check if arguments are none
    if args.codeforces == None:
        print("No Arguments Passed. Try Again")
    if args.codeforces is not None:
        cfUser = requests.get(URL + "user.info?handles=" + args.codeforces).json()
        if cfUser['status'] != 'OK':
            # Handle errors while receiving data from Codeforces
            print('\033[1;31mAuthentication with Codeforces Failed\033[0m')
            print('Check your Handle')
        else:
            # User Handle from codeforces
            handle = cfUser['result'][0]['handle']
            print(f"Found a Codeforces Handle Corresponding to \033[1;35m{args.codeforces}\033[0m")
            print(f"https://codeforces.com/profile/{handle}")
            print("Confirm to PROCEED ? Yes(Y)/No(N)", end=" ")
            inp = input()
            if inp.lower() == 'yes' or inp.lower() == 'y':
                print("\033[1;32mCodeforces Account Synced!\033[0m")
            
            # Storing information in info.json
            # Open info.json
            file = open('info.json')
            data = json.load(file)
            # Set Codeforces Info
            data['login']['codeforces'] = {
                "handle": handle,
                "rating": cfUser['result'][0]['rating'],
                "rank": cfUser['result'][0]['rank']
            }
            file.close()
            # Dump the changed info back into info.json
            data = json.dumps(data, indent=4)
            with open('info.json', 'w') as outfile:
                outfile.write(data)

def get_problem(args):
    # Check the accounts has been logged in
    loggedIn = []
    file = open('info.json')
    data = json.load(file)
    try:
        if data['login']['codeforces'] != None:
            loggedIn.append('codeforces')
    except:
        pass
    if len(loggedIn) == 0:
        print("\033[1;33mWarning: No Account has been Synced")
        print("Type \"codehut login --help\" for help\033[0m")
        return None
    
    if data['current'] != None:
        print("There is already a Problem in Progress, do you want to get a new one?")
        print("Yes/No", end="\t")
        inp = input()
        if inp.lower() == 'n' or inp.lower() == 'no':
            return
    problem = get_codeforces_by_rating(args.rating.split(','), args.tags.split(','))
    # Add the problem as current problem
    file = open('info.json')
    data = json.load(file)
    data['current'] = problem.split('/')[5] + problem.split('/')[6];
    file.close()
    data = json.dumps(data, indent=4)
    with open('info.json', 'w') as outfile:
        outfile.write(data)

    # open web browser with the url of the problem
    webbrowser.open(problem)

def get_submission(args):
    # get info from info.json
    file = open('info.json')
    data = json.load(file)
    # get all submissions
    handle = data['login']['codeforces']['handle']
    submissions = requests.get(URL + f"user.status?handle={handle}&from=1&count=20").json()
    
    # Check for the solution uploaded
    verdict = get_submission_codeforces(submissions['result'], data['current'])
    if verdict == 'OK':
        print("\033[1;32mACCEPTED\033[0m")
    elif verdict == 'WRONG_ANSWER':
        print("\033[1;33mWRONG ANSWER\033[0m")
    elif verdict == 'COMPILATION ERROR':
        print("\033[1;34mCOMPILATION ERROR\033[0m")
    else:
        print("\033[1;34mRUN TIME ERROR")
    file.close()
    data['current'] = None
    data = json.dumps(data, indent=4)
    with open('info.json', 'w') as outfile:
        outfile.write(data)

def main():
    parser = argparse.ArgumentParser(description="Competitve Programming Tool")
    # Create sub parsers for multiple possible arguments
    subparser = parser.add_subparsers(dest='command')

    # Login sub parser to login to Codeforces, CodeChef and AtCoder
    login = subparser.add_parser('login', help="Sync with Codeforces Account")
    # Optional arguments to login to any of them
    login.add_argument('-cf', '--codeforces', type=str, help="Codeforces Username", metavar='')

    # Problem sub parser to fetch questions to practice
    problem = subparser.add_parser('problem', help="Fetch Practice Questions")
    # Optional arguments to get questions based on Rating Range or Tags
    problem.add_argument('-r', '--rating', type=str, help="Rating Range to Practice with comma -> (eg '1000,2000')", metavar='')
    problem.add_argument('-t', '--tags', type=str, help="Tage to Practice with comma -> (eg 'dp,greedy')", metavar='')

    # Submit sub parser to Submit codes
    submit = subparser.add_parser('submit', help="Submit the Code")

    args = parser.parse_args()

    if args.command == 'login':
        connect_login(args)
    if args.command == 'problem':
        get_problem(args)
    if args.command == 'submit':
        get_submission(args)

if __name__ == "__main__":
    main()