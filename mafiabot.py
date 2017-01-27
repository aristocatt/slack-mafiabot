import time
from gamesetups import begin_game
from lobby import GameLobby
from slackclient import SlackClient
from gameaction import handle_action
from game import GameHandler


BOT_ID = 'bot id goes here'

#Constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = 'do'
start_game = '!start'
join_game = '!join'
vote = '!vote'
begin = '!begin'
helpme = '!help'
get_tally = '!tally'


#gamelobby
Lobby = GameLobby()
id_name_hash = {}

#instantiate slack and twilio
slack_client = SlackClient("token goes here")
user_list = slack_client.api_call('users.list')

#displays message to channel or user, or later on to a private mafia channel
def message(response, channel = None):
    if channel:
        slack_client.api_call("chat.postMessage", channel='@'+channel,
                              text=response, as_user=False)
    else:
        slack_client.api_call("chat.postMessage", channel='C3RE8JRT6',
                              text=response, as_user=False)



#check to see if the game can be started, if so start the game
def game_exists(Lobby):
    message("Checking users and initializing game:", )

    if Lobby.get_game_state() == 2:
        Lobby.set_game_state(3)
        time.sleep(2)
        state = Lobby.get_game_state()
        Game = begin_game(Lobby)
        lobby = Lobby.get_lobby()
        players = ', '.join('{}'.format(key) for key in Lobby.get_lobby().keys())
        print(players)
        for x in lobby:
            print(x)
            role = lobby[x].role
            print(role)

            message("Welcome you are" + role +'you know what to do', x)
        Lobby.set_game_state(4)
        message("Game is beginning Players: " + players)
        return Game
    elif Lobby.get_game_state() == 1:
        Lobby.set_game_state(0)
        Lobby.clear_lobby()
        message("Not enough players to begin game")
        return None
    else:
        print("Game state makes no sense, it is currently at: ", Lobby.get_game_state())
        return None


#just a place holder for in game commands that do not actually affect the Game or Lobby classes
def handle_basic(command ,user_name):
    if command.startswith(helpme):
        message("I am working on this.",user_name)
    elif command.startswith(get_tally):
        Game.tally_vote()


#Handles commands entered prior to the game beginning.
def handle_command(command, channel, Lobby, user_name, user_id):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith((helpme, start_game, join_game, '!sexy', '!wizzy')):
        if command.startswith(helpme):
            response = "Need help?  Here's a list of commands \n" \
                       "Begin a game by typing: !start \n" \
                       "Join a game that has begun by typing: !join \n" \
                       "Once enough people have joined start the game by typing: !begin"
        elif command.startswith(start_game):
            if Lobby.get_game_state() == 0:
                response = user_name + " has begun a game.  Type '!join' to join!"
                Lobby.set_game_state(1)
                timer = time.time() + 2
                message(response)
                return timer
            elif Lobby.get_game_state() == 1:
                response = "Game already in queue, type '!join' to join."
            else:
                response = "Game already in progress"

        elif command.startswith(join_game):
            if Lobby.get_game_state() >= 1:
                response = Lobby.add_player(user_name,user_id)
                if len(Lobby.game_lobby) >= 1:
                    Lobby.set_game_state(2)
            elif Lobby.get_game_state() == 0:
                response = "Please type !start to begin a game before joining."
        elif command.startswith('!sexy'):
            response = "Aristocatt is way more attractive than " + user_name
        elif command.startswith('!wizzy'):
            response = "Wizzy: \n" \
                       "1: A pussy/vagina--typically only refers to a desirable one. \n" \
                       "2: Some girls feel awkward when you say 'pussy' in front of them, thus this term has been created to give 'pussy' a funner, more relaxed, and chiller connotation. Fun girls tend to get horny upon hearing the word. \n" \
                       "3: Not just any pussy, a pussy that you really want to be in (Thus, the term can even be used to describe the girl as a whole)."
        message(response)


    else:
        message('You used an incorrect action, type "!help" for a list '
                       'of actions')





def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output and '!' in output['text'][0]:
                # return text after the @ mention, whitespace removed
                return output['text'].lower(), \
                       output['channel'], output['user']

    return None, None, None

def check_game(Lobby):
    players = Lobby.get_lobby()
    town = 0
    mafia = 0
    for x in players:
        if players[x].alliance == "town":
            town += 1
        elif players[x].alliance == "mafia":
            mafia += 1

    if mafia >= town:
        return "Mafia"
    elif mafia == 0:
        return "Town"
    else:
        return None



if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            if Lobby.get_game_state() == 4:
                if Game.check_cycle() == 1:
                    if Game.period == False:
                        kill = Game.resolve_action()
                        message("It is now day time the result of the night actions were: \n")
                        try:
                            message(kill + 'is dead')
                        except TypeError:
                            message("No one was killed")
                        if kill in Lobby.get_lobby():
                            Lobby.remove_player(kill)
                    elif Game.period == True:
                        response, lynch = Game.resolve_lynch()
                        message(response)
                        message("The town got together and voted. " + lynch +
                                " was lynched.")
                        if lynch in Lobby.get_lobby():
                            Lobby.remove_player(lynch)
                    else: message("Houston we have a problem")
                    winner = check_game(Lobby)
                    if winner in ('Town','Mafia'):
                        message("Congratulations: " + winner + " you have won.  Resetting Game and Lobby")
                        Lobby.clear_lobby()


                    Game.set_cycle(not Game.period)
                    time.sleep(1)
                    if Lobby.get_lobby() == None:
                        del Game


            command, channel, user_id = parse_slack_output(slack_client.rtm_read())
            if command and channel and user_id and Lobby.get_game_state() in (0, 1, 2):
                user_name = None
                for x in user_list['members']:
                    if x['id'] == user_id:
                        user_name = x['name']
                if Lobby.get_game_state() == 0:
                    timer = handle_command(command, channel, Lobby, user_name, user_id)
                elif command == begin and Lobby.get_game_state() in (1, 2):
                    if time.time() >= timer:
                        Game = game_exists(Lobby)
                    else: message("Patience is a virtue!")
                else:
                    handle_command(command, channel, Lobby, user_name, user_id)
            elif command and channel and user_id and Lobby.get_game_state() == 4:
                id_hash = Lobby.get_hash()
                if user_id in id_hash:
                    user_name = id_hash[user_id]
                    response, channel = handle_action(command, channel, Lobby, Game, user_name)
                    message(response, channel)

            time.sleep(READ_WEBSOCKET_DELAY)



    else:
        print("Connection failed. Invalid Slack token or bot ID?")