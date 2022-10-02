from array import array
import requests
import argparse
import json

URL = "https://codeforces.com/api/"

def connect_login(args):
    # Verify user and add it to info.json file
    # Check if arguments are none
    if args.atcoder == None and args.codeforces == None and args.codechef == None:
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
        if data['login']['codechef'] != None:
            loggedIn.append('codechef')
        if data['login']['atcoder'] != None:
            loggedIn.append('atcoder')
    except:
        pass
    if len(loggedIn) == 0:
        print("\033[1;33mWarning: No Account has been Synced")
        print("Type \"codehut login --help\" for help\033[0m")
        return None
    

def main():
    parser = argparse.ArgumentParser(description="Competitve Programming Tool")
    # Create sub parsers for multiple possible arguments
    subparser = parser.add_subparsers(dest='command')

    # Login sub parser to login to Codeforces, CodeChef and AtCoder
    login = subparser.add_parser('login', help="Sync with Codeforces/CodeChef/AtCoder Accounts")
    # Optional arguments to login to any of them
    login.add_argument('-cf', '--codeforces', type=str, help="Codeforces Username", metavar='')
    login.add_argument('-cc', '--codechef', type=str, help="CodeChef Username", metavar='')
    login.add_argument('-ac', '--atcoder', type=str, help="AtCoder Username", metavar='')

    # Problem sub parser to fetch questions to practice
    problem = subparser.add_parser('problem', help="Fetch Practice Questions")
    # Optional arguments to get questions based on Rating Range or Tags
    problem.add_argument('-r', '--rating', type=array, help="Rating Range to Practice -> (eg [1000, 2000])", metavar='')
    problem.add_argument('-t', '--tags', type=array, help="Tage to Practice -> (eg [dp, greedy])", metavar='')

    args = parser.parse_args()

    if args.command == 'login':
        connect_login(args)
    if args.command == 'problem':
        get_problem(args)

if __name__ == "__main__":
    main()