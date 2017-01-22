import time
from gamesetups import begin_game
from lobby import GameLobby
from slackclient import SlackClient
from gameaction import handle_action
from game import GameHandler


BOT_ID = 'U3RC29X0A'

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
slack_client = SlackClient("xoxb-127410337010-MOwjbYIDCqhKM9xxIKRq1VL8")
user_list = slack_client.api_call('users.list')

#displays message to channel or user, or later on to a private mafia channel
def message(response, channel = None):
    if channel:
        print(channel)
        slack_client.api_call("chat.postMessage", channel=channel,
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
        players = ', '.join('{}'.format(key) for key in Lobby.get_lobby().keys())
        print(players)
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
def handle_basic(command,user_name):
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
    if command.startswith((EXAMPLE_COMMAND, start_game, join_game, 'sexy')):
        if command.startswith(EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can do that!"
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
            response = Lobby.add_player(user_name,user_id)
            if len(Lobby.game_lobby) >= 1:
                Lobby.set_game_state(2)
        elif command.startswith('sexy'):
            response = "Aristocatt is way more attractive than " + user_name
        message(response)
    else:
        message('You used an incorrect action, type "@mafiabot !help" for a list '
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
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            if Lobby.get_game_state() == 4:
                if Game.check_cycle() == 1:
                    if Game.period == False:
                        message("It is now day time the result of the night actions were: ")
                    elif Game.period == True:
                        response, lynch = Game.resolve_lynch()
                        message(response)
                        message("The town got together and voted. " + lynch +
                                " was lynched.  It is now night")
                        if lynch in Lobby.get_lobby():
                            Lobby.remove_player(lynch)
                    else: message("Houston we have a problem")
                    Game.set_cycle(not Game.period)
                    time.sleep(1)

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
                    if command.startswith(helpme, get_tally):
                        handle_basic(command,user_name)

                    else:
                        response, channel = handle_action(command, channel, Lobby, Game, user_name)
                        message(response, channel)

            time.sleep(READ_WEBSOCKET_DELAY)



    else:
        print("Connection failed. Invalid Slack token or bot ID?")