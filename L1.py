import requests
import json
#from pprint import pprint
token_file = open("token.txt", "r")
token = token_file.readline()
username = 'nemec-r'

users_repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
j_data = users_repos.json()
repo_name_data = []

for repo in j_data:
    if not repo['private']:
       repo_name_data.append(repo['html_url'])

with open('repo_name_data.json', 'w') as outfile:
    json.dump(repo_name_data, outfile)