import requests

bearer_token = 'xqnwj1aiufg67famh8kthzgqpa'
#Kanto Public id xqnwj1aiufg67famh8kthzgqpa
#Kanto Region Private id uwkrrxm7c7f19gixuc93rcmr8w
#intern channel qrfhyetwutnnucb3uuoe3ka1fh
#for test channel use the token for your dms
#test channel h6phkma4ibnr3fpdayutxpy7wh

LISTEN_URL = 'https://mattermost.hyland.com/api/v4/channels/' + bearer_token + '/posts'
POST_URL = 'https://mattermost.hyland.com/api/v4/posts'
AUTH_TOKEN = 'h6s5cmnp5pr77kx6s7ao3huwzh'

POST_URL = 'https://mattermost.hyland.com/api/v4/posts'
WEBHOOK_URL = 'https://mattermost.hyland.com/hooks/enank36nm3fzietx6c9o6pzsqy'
def post(s):
    data = {'channel_id': bearer_token, 'message': s}
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    requests.post(POST_URL, json= data, headers= headers, verify= False)

def webHook_pbot(s):
    
    headers = {'Content-Type' : 'application/json'}
    data = {
        'username':'Poke-Bot',
        'icon_url': 'https://images.discordapp.net/avatars/424911754242555904/57bcc9cd16a736279dd8d4f8d875b6fb.png',
        'text': s
    }
    requests.post(WEBHOOK_URL, json= data, headers= headers, verify= False)

def pokemonAppear(s):
    
    headers = {'Content-Type' : 'application/json'}
    data = {
        'username':'A Wild Pokemon Has Appeared!',
        'icon_url': 'https://unixtitan.net/images/pokeball-clipart-open-4.png',
        'text': '# :' + s + ':'
    }
    requests.post(WEBHOOK_URL, json= data, headers= headers, verify= False)
