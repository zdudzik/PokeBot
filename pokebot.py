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
AUTH_TOKEN = ''

#Checks for valid commands
def process_commands(message, name):
    #no flag response
    messagel = message.lower()
    cap_name = name
    name = name.lower()
    if(messagel == "!pbot"):
        pbotPost.webHook_pbot("Thank you for using PokeBot! For a list of commands please use the help or h flag.")

    #help flag
    if("!pbot h" in messagel):
        pbotPost.webHook_pbot("PokeBot Says: Type the name of a wild pokemon to catch it!\nType !pbot to interact with PokeBot. The following flags are supported: \n `p`: displays your pokemon \n `p {Trainer Name}` : displays another trainer's pokemon\n `c`: displays your current number of pokemon\n `c {Trainer Name}` : displays another trainer's number of pokemon\n `l`: displays the leaderboard\n `give {Trainer Name},{pokemon}` : gives a pokemon you have to another trainer \n `v`: check the current PokeBot version.\n `h`: opens the help menu \n Coming soon: trade, battle, and more!")
    
    #version flag
    if("!pbot v" in messagel):
        pbotPost.webHook_pbot("PokeBot Says: You are currently using PokeBot verion: 0.3.22.")

    #catch pokemon
    if(messagel in pokemon_list):
        if pokemon_active[messagel] > 0:
            pbotPost.webHook_pbot('' + cap_name + ' caught ' + messagel +'!')
            pokemon_active[messagel] = pokemon_active[messagel] - 1
            db_post(name,messagel)

    #check pokemon flag
    if("!pbot p" in messagel):
        if (messagel == "!pbot p"):
            if(name in trainers):
                mypokemon = ''
                for pokemon in trainers[name]:
                    mypokemon = mypokemon + ' :' + pokemon + ': '
                pbotPost.webHook_pbot('PokeBot Says: Displaying ' + cap_name + '\'s Pokemon.')
                pbotPost.webHook_pbot(mypokemon)
            else:
                pbotPost.webHook_pbot('Pokebot Says: You have no pokemon.')
        else:
            capname = message[8:]
            keyname = messagel[8:]
            if(keyname in trainers):
                mypokemon = ''
                for pokemon in trainers[keyname]:
                    mypokemon = mypokemon + ' :' + pokemon + ': '
                pbotPost.webHook_pbot('PokeBot Says: Displaying ' + capname + '\'s Pokemon.')
                pbotPost.webHook_pbot(mypokemon)
            else:
                pbotPost.webHook_pbot('Pokebot Says: ' + capname + ' has no pokemon.')

    if("!pbot c" in messagel):
        if (messagel == "!pbot c"):
            if(name in trainers):
                count = 0
                for i in trainers[name]:
                    count = count + 1
                pbotPost.webHook_pbot('PokeBot Says: ' + cap_name + ' has ' + str(count) + ' Pokemon.')
            else:
                pbotPost.webHook_pbot('Pokebot Says: '+ cap_name +' has no pokemon.')
        else:
            capname = message[8:]
            name = messagel[8:]
            if(name in trainers):
                count = 0
                for i in trainers[name]:
                    count = count + 1
                pbotPost.webHook_pbot('PokeBot Says: ' + capname + ' has ' + str(count) + ' Pokemon.')
            else:
                pbotPost.webHook_pbot('Pokebot Says: '+ capname +' has no pokemon.')

    if("!pbot l" in messagel):
        
        leaderboard_str = ''
        pbotPost.webHook_pbot('PokeBot Says: Displaying Leaderboard.')
        leaders = []
        places = [':1st_place_medal:',':2nd_place_medal:',':3rd_place_medal:',':youtried:']
        place = 1
        while place < 5:
            leader = 0
            leader_name = ''
            for i in trainers:
                count = 0
                for k in trainers[i]:
                    count = count + 1
                if count > leader:
                    if i not in leaders:
                        leader = count
                        leader_name = i
            leaders.append(leader_name)
            leaderboard_str = leaderboard_str + places[place-1] + ' : ' + leader_name + ' has ' + str(leader) + ' Pokemon.\n'
            place = place + 1
        pbotPost.webHook_pbot(leaderboard_str)

    if("!pbot grant: " in messagel):
        if(name == 'zach dudzik'):
            targets = message[12:]
            params = targets.split(',')
            db_post(params[0].lower(),params[1].lower())
            pbotPost.webHook_pbot('PokeBot Says: ' + str(params[0]) + ' recieved ' + str(params[1]).lower())

    if("!pbot give" in messagel):
        targets = message[11:]
        targets = targets.strip()
        params = targets.split(',')
        target_name = params[0]
        target_namel = target_name.lower()
        target_gift = params[1].lower()
        if target_namel in trainers:
            if target_gift in pokemon_list:
                trainers_update()
                sender_inventory = trainers[name]
                if target_gift in sender_inventory:
                    trainers[name].remove(target_gift)
                    db_blank_post(name)
                    db_post(target_namel,target_gift)
                    pbotPost.webHook_pbot('PokeBot Says: ' + str(target_name) + ' recieved ' + str(target_gift))
                else:
                    pbotPost.webHook_pbot('PokeBot Says: You do not have a ' + str(target_gift) + ' to give.')
            else:
                pbotPost.webHook_pbot('PokeBot Says: No pokemon with name: ' + target_gift)
        else:
            pbotPost.webHook_pbot('PokeBot Says: No trainer with name: ' + target_name)





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
        return (info['posts'][post]['message'], display_name, userid)

#sends a random pokemon to the channel and flags it as active
def send_pokemon(pokedex):
    index = random.randint(0, len(pokedex) - 1)
    pokemon = pokedex[index].lower()
    pokemon_active[pokemon] = pokemon_active[pokemon] + 1
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

def db_blank_post(user_name):
    crsr = conn.cursor()
    if user_name.lower() in trainers:
        del_command = '''DELETE FROM USERS WHERE user_name = "{}"'''.format(user_name)
        crsr.execute(del_command) 
        conn.commit()

        inventory = pokemon_list_to_string(trainers[user_name.lower()])
        sql_command = """INSERT INTO USERS VALUES ("{}", "{}");""".format(user_name,inventory)
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

    #gets messages/display names/userid
    message, name, userid = read_message()

    #processes commands
    process_commands(message, name)

