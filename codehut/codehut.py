import requests
import argparse
import json
import webbrowser
from subprocess import call

from helper_scripts import get_codeforces_by_rating, get_submission_codeforces, check_init, write_file

URL = "https://codeforces.com/api/"

def initialize(args):
    # Initialise Codehut
    print("If you have initialized before, all data will be lost. Press Ctrl + C if you want to discontinue")
    name = input("Name: ")
    print("Complete path to be entered")
    print(r"eg: C:\User\Docs\Folder\File.extension")
    path = input("Path where source code is to be saved (default: codehut repository): ")
    template = input("Path to code template (if any): ")
    language = input("Extension of your programming Language (default: cpp): ")

    while name == '':
        print("\033[1;31mName is a required field. Press Ctrl + C if you wish to quit initializing...\033[0m")
        name = input("Name: ")

    write_file(language, name, template, path)
    print("\033[1;32mInitialization Complete")
    print("Type \"codehut --help\" for help\033[0m")
    print("Use \033[1;35mVisual Studio Code\033[0m for best experience!")


def connect_login(args):
    # Check if user has innitialized
    if not check_init():
        print("\033[1;31mInitialize Codehut before continuing")
        print("Type: codehut init\033[0m")
        return

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
            data["login"] = {}
            data["login"]['codeforces'] = {
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
    # Check if user has innitialized
    if not check_init():
        print("\033[1;31mInitialize Codehut before continuing")
        print("Type: codehut init\033[0m")
        return

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
    data['current'] = problem.split('/')[5] + problem.split('/')[6]
    path = data['init']['path']
    file.close()
    data = json.dumps(data, indent=4)
    with open('info.json', 'w') as outfile:
        outfile.write(data)

    try:
        call(["code", path])
    except:
        print("\033[1;31mVisual Studio Code not installed. Please open the following folder in your code editor to write code\033[0m")
        print("\033[1;33m" + path + "\033[0m")

    print("Opening Web Browser with the problem")
    # open web browser with the url of the problem
    webbrowser.open(problem)


def submit_codeforces(args):
    # Check if user has innitialized
    if not check_init():
        print("\033[1;31mInitialize Codehut before continuing")
        print("Type: codehut init\033[0m")
        return

        

def get_submission(args):
    # Check if user has innitialized
    if not check_init():
        print("\033[1;31mInitialize Codehut before continuing")
        print("Type: codehut init\033[0m")
        return

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

def update_info(args):
    # check if already initialized
    if not check_init():
        print("\033[1;31mInitialize Codehut before continuing")
        print("Type: codehut init\033[0m")
        return

    # get name from info.json
    file = open('info.json')
    data = json.load(file)
    file.close()
    # assign variables
    language = args.language
    path = args.path
    template = args.template

    if args.langauge == None:
        language = data['init']['language']
    if args.path == None:
        path = data['init']['path']
    if args.template == None:
        template = data['init']['template']
    write_file(language, data['init']['name'], template, path)
    print("\033[1;32mUpdated!\033[0m")

def main():
    parser = argparse.ArgumentParser(description="Competitve Programming Tool")
    # Create sub parsers for multiple possible arguments
    subparser = parser.add_subparsers(dest='command')

    # Initializer
    init = subparser.add_parser('init', help="Initialize")

    # Update Path / Template / Language
    update = subparser.add_parser('update', help="Update Path/Template/Language")
    # optional arguments to change
    update.add_argument('-up', '--path', type=str, help="Update Source File Path", metavar='')
    update.add_argument('-ut', '--template', type=str, help="Update Template of Source Code", metavar='')
    update.add_argument('-ul', '--language', type=str, help="Update Extension of Source Code", metavar='')

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
    submit = subparser.add_parser('submit', help="Code Submitted!")

    # handle invalid argument SystemExit
    try:
        args = parser.parse_args()
    except SystemExit:
        print("\033[1;31mInvalid Arguments\033[0m")

    if args.command == 'init':
        initialize(args)
    elif args.command == 'login':
        connect_login(args)
    elif args.command == 'problem':
        get_problem(args)
    elif args.command == 'submit':
        get_submission(args)
        # Not complete
    elif args.command == 'update':
        update_info(args)

if __name__ == "__main__":
    main()