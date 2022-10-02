import requests
from bs4 import BeautifulSoup
import random

def get_codeforces_by_rating(rating, tags):
    url = "https://codeforces.com/problemset?tags="
    if len(rating) > 0:
        if len(rating) == 1:
            # if one rating is provided, by default everything over that rating is considered
            url = url + f"{rating[0]}-3500"
        else:
            url = url + f"{rating[0]}-{rating[1]}"

    # append all the tags to the url
    for tag in tags:
        url = url + f",{tag}"

    # get problems from codeforces
    ret = requests.get(url).content
    soup = BeautifulSoup(ret, 'lxml')
    problems = soup.find('table', class_ = "problems")
    problems = soup.find_all('td', class_="id")
    with open('soup.txt', 'a') as file:
        ele = random.randint(0, len(problems)-1)
        p = problems[ele].find('a')['href']
        return "https://codeforces.com" + str(p)

def get_submission_codeforces(submissions, problemID):
    # Loop over all submissions and find the one for this current problem
    for submission in submissions:
        if submission['problem']['contestId'] + submission['problem']['index'] == problemID:
            return submission['verdict']
    return None