import json
import time
import calendar
import random
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sqlite3
conn = sqlite3.connect('pokebot_users.db')
import pbotPost
from pokemon import pokemon_list
from pokemon import pokemon_active

bearer_token = 'xqnwj1aiufg67famh8kthzgqpa'
#Kanto Public id xqnwj1aiufg67famh8kthzgqpa
#Kanto Region Private id uwkrrxm7c7f19gixuc93rcmr8w
#intern channel qrfhyetwutnnucb3uuoe3ka1fh
#for test channel use the token for your dms
#test channel h6phkma4ibnr3fpdayutxpy7wh

LISTEN_URL = 'https://mattermost.hyland.com/api/v4/channels/' + bearer_token + '/posts'
POST_URL = 'https://mattermost.hyland.com/api/v4/posts'
AUTH_TOKEN = '-------------------------'

#Checks for valid commands
def process_commands(message, name):
    #no flag response
    message = message.lower()
    cap_name = name
    name = name.lower()
    if(message== "!pbot"):
        pbotPost.webHook_pbot("Thank you for using PokeBot! For a list of commands please use the help or h flag.")

    #help flag
    if("!pbot h" in message):
        pbotPost.webHook_pbot("PokeBot Says: ")

    #catch poke
    if(message in pokemon_list):
        if pokemon_active[message] == 1:
            pbotPost.webHook_pbot('' + cap_name + ' caught ' + message +'!')
            pokemon_active[message] = 0
            db_post(name,message)

    #check pokemon flag
    if("!pbot p" in message):
        #print(trainers)
        if(name in trainers):
            mypokemon = ''
            for pokemon in trainers[name]:
                #print(pokemon)
                mypokemon = mypokemon + ' :' + pokemon + ': '
            pbotPost.webHook_pbot('PokeBot Says: Displaying ' + cap_name + '\'s Pokemon.')
            pbotPost.webHook_pbot(mypokemon)
        else:
            pbotPost.webHook_pbot('Pokebot Says: You have no pokemon.')

#posts a message in the channel
def post_message(s):
    data = {'channel_id': bearer_token, 'message': s}
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    requests.post(POST_URL, json= data, headers= headers, verify= False)

def post_messages_webHook_pbot(s):
    url = 'https://mattermost.hyland.com/hooks/enank36nm3fzietx6c9o6pzsqy'
    headers = {'Content-Type' : 'application/json'}
    data = {
        'username':'Poke-Bot',
        'icon_url': 'https://images.discordapp.net/avatars/424911754242555904/57bcc9cd16a736279dd8d4f8d875b6fb.png',
        'text': s
    }
    requests.post(url, json= data, headers= headers, verify= False)

def post_messages_webHook_pokemonAppear(s):
    url = 'https://mattermost.hyland.com/hooks/enank36nm3fzietx6c9o6pzsqy'
    headers = {'Content-Type' : 'application/json'}
    data = {
        'username':'A Wild Pokemon Has Appeared!',
        'icon_url': 'https://unixtitan.net/images/pokeball-clipart-open-4.png',
        'text': '# :' + s + ':'
    }
    requests.post(url, json= data, headers= headers, verify= False)

#gets a message/display name of messages sent in the channel
def read_message():
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    resp = requests.get(LISTEN_URL, headers= headers, verify= False)
    if(resp.status_code==200):
        #gets the message text
        info = json.loads(resp.text)
        post = info['order'][0]

        #gets the user's display name
        userid = info['posts'][post]['user_id']
        profile = requests.get('https://mattermost.hyland.com/api/v4/users/' + userid, headers= headers, verify= False)
        user = json.loads(profile.text)
        display_name = user['first_name'] + ' ' + user['last_name']

        #returns message, display name
        return (info['posts'][post]['message'], display_name)

#sends a random pokemon to the channel and flags it as active
def send_pokemon(pokedex):
    index = random.randint(0, len(pokedex) - 1)
    pokemon = pokedex[index].lower()
    pokemon_active[pokemon] = 1
    pbotPost.pokemonAppear(pokemon)

def pokemon_list_to_string(pokemon):
    poke_list = ''
    for poke in pokemon:
        poke_list = poke_list + poke + ','
    return poke_list[0:len(poke_list) - 1]

def db_post(user_name, pokemon):
    crsr = conn.cursor()
    trainers_update()
    if user_name.lower() in trainers:
        trainers[user_name.lower()].append(pokemon)
        del_command = '''DELETE FROM USERS WHERE user_name = "{}"'''.format(user_name)
        crsr.execute(del_command) 
        conn.commit()

        inventory = pokemon_list_to_string(trainers[user_name.lower()])
        sql_command = """INSERT INTO USERS VALUES ("{}", "{}");""".format(user_name,inventory)
        crsr.execute(sql_command) 
        conn.commit()
    else:
        
        trainers[user_name.lower()] = [str(pokemon)]
        sql_command = """INSERT INTO USERS VALUES ("{}", "{}");""".format(user_name,pokemon)
        crsr.execute(sql_command) 
        conn.commit()

def trainers_update():
    crsr = conn.cursor()
    #get list of users
    crsr.execute("SELECT user_name FROM USERS")
    data = crsr.fetchall()
    users = []
    for i in data:
        users.append(i)

    #get list of pokemon
    crsr.execute("SELECT pokemon FROM USERS")
    data = crsr.fetchall()
    inventories = []
    for i in data:
        data = crsr.fetchall()    
        str = i[0]
        pokemon = str.split(',')
        inventories.append(pokemon)

    #update trainers
    for user in users:
        user_name = user[0].lower()
        trainers[user_name] = inventories[users.index(user)]

trainers = {}
send_poke_time  = 200 + calendar.timegm(time.gmtime()) #initialize time to 200 seconds
send_pokemon(pokemon_list)
while True:

    #populate with pokemon
    #print(minute_wait)
    if(calendar.timegm(time.gmtime()) > send_poke_time):#uses seconds from epoch time instead of min
        send_pokemon(pokemon_list)
        send_poke_time = calendar.timegm(time.gmtime()) +  random.randint(240, 600) # between 4 min and 10 min

    #gets messages/display names
    message, name = read_message()

    #processes commands
    process_commands(message, name)

