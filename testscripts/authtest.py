import requests, sys
from base64 import b64decode, b64encode

url = "http://127.0.0.1:5000/"

users = [('testuser', 'testpasswd')]



match sys.argv[1]:
    case 'register':
        url += 'auth/register'
        post = {'username':users[0][0], 'passwd':users[0][1]}
        request = requests.post(url, json = post)
        print("register POST request sent...")
        print("response: ", request.text)
    case 'create_task':
        url += 'todolist/create_task'
        post = {'brief':'brief description', 'detail': 'detailed description',
                'taskStatus':'completed'}
        b64cred = b64encode((users[0][0]+":"+users[0][1]).encode("ascii")).decode("ascii")
        authHeader = {'Authorization': f'Basic {b64cred}'}
        request = requests.post(url, json = post, headers = authHeader)
        print("response: ", request.text)
    case 'fetch_all':
        url += 'todolist/fetch'
        response = request = requests.get(url, params={"detailed":"ship"})
        print(response.text)
    case 'update':
        url += 'todolist/update'
        post = {'id':'2', 'brief':'skibidi'}
        b64cred = b64encode((users[0][0]+":"+users[0][1]).encode("ascii")).decode("ascii")
        authHeader = {'Authorization': f'Basic {b64cred}'}
        response = requests.post(url, json = post, headers = authHeader)
        print(response.text)
    case 'delete':
        url += 'todolist/delete'
        post = {'id':'3'}
        b64cred = b64encode((users[0][0]+":"+users[0][1]).encode("ascii")).decode("ascii")
        authHeader = {'Authorization': f'Basic {b64cred}'}
        response = requests.post(url, json = post, headers = authHeader)
        print(response.text)
    case _:
        print('unknown parameter')