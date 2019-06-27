import requests

POST_URL = 'https://mattermost.hyland.com/api/v4/posts'
WEBHOOK_URL = 'https://mattermost.hyland.com/hooks/enank36nm3fzietx6c9o6pzsqy'
def post(s):
    data = {'channel_id': bearer_token, 'message': s}
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    requests.post(POST_URL, json= data, headers= headers, verify= False)

def webHook_pbot(s):
    
    headders = {'Content-Type' : 'application/json'}
    data = {
        'username':'Poke-Bot',
        'icon_url': 'https://images.discordapp.net/avatars/424911754242555904/57bcc9cd16a736279dd8d4f8d875b6fb.png',
        'text': s
    }
    requests.post(WEBHOOK_URL, json= data, headers= headers, verify= False)

def pokemonAppear():
    
    headders = {'Content-Type' : 'application/json'}
    data = {
        'username':'A Wild Pokemon Has Appeared!',
        'icon_url': 'https://unixtitan.net/images/pokeball-clipart-open-4.png',
        'text': '# :' + s + ':'
    }
    requests.post(WEBHOOK_URL, json= data, headers= headers, verify= False)