from bs4 import BeautifulSoup
import requests

def submit():
    csrf_token = get_csrf()
    headers = {
        'X-Csrf-Token': csrf_token
    }

    payload = {
        'csrf_token': csrf_token,
        'ftaa': '7gpl6sg25dsyuvfchc',
        'bfaa': 'b509623e99b1a10c37a0526ea4b65621',
        'action': 'submitSolutionFormSubmitted',
        'contestId': '1739',
        'submittedProblemIndex': 'E',
        'ProgramTypeId': '73',
        'source': '#iclude',
        'tabSize': '4',
        'sourceFile': '',
        '_tta': '223'
    }

    res = requests.post(url=f"https://codeforces.com/problemset/submit?csrf_token={csrf_token}", data=payload).json()
    # print(type(res))


def get_csrf():
    res = requests.get("https://codeforces.com/problemset/submit").content
    soup = BeautifulSoup(res, 'lxml')
    li = soup.find_all('meta')
    # return li[1].get("content")
    print(li)

def login():
    base = "https://codeforces.com"
    service_url = "{base}/{login}".format(base=base, login="enter")

    s = requests.session()
    dt = s.get(service_url)
    dt = dt.text
    ss = BeautifulSoup(dt, 'html.parser')
    csrf_token = ss.find_all("span", {"class": "csrf-token"})[0]["data-csrf"]
    print(csrf_token)

    usr_name = 'rajaryan18'
    psd = 'minecraftdr'

    headers = {
        'X-Csrf-Token': csrf_token
    }
    payload = {
    'csrf_token': csrf_token,
    'action': 'enter',
    'handleOrEmail': usr_name,
    'password': psd,
    }
    try:
        data = s.post(service_url, data=payload, headers=headers)
        print(data.json()['result'])
    except:
        print("Error")


login()