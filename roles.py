"""Roles extend from Vanilla, Mafia roles would extend from mafia etc.
get_actions just gets all the acceptable actions for that user at that time.
The vote/kill/etc actions take the command entered by the user parse it how they
think it should be parsed and then they do something with it."""

class Vanilla(object):

    def __init__(self, alliance='town'):
        self.alliance = alliance
        self.resolve = alliance
        self.role = 'Vanilla'
        self.day_actions = {'!help':self.help, '!vote': self.vote, '!tally':None}
        self.night_actions = {'!help': self.help}
        self.check_input = {}
        self.resolve = None

    def get_role(self):
        return self.role

    def get_actions(self, **kwargs):
        '''Kwargs is used to get actions because other roles like role cop may be day/night
        cycle irrelevant, this makes it explicit.  If cycle is being passed, it is checking
        to make sure the user has permission to said action at the given day/night cycle'''
        if 'period' in kwargs:

            if kwargs['period']:
                return self.day_actions
            elif not kwargs['period']:
                return self.night_actions


    def vote(self, user_name, target, Game, players):
        try:
            target = target[1]
            if target in players:
                Game.set_vote(user_name, target)
                return user_name + " voted for: " + target, None
            else:
                return "Please select an appropriate player", user_name
        except:
            print('select a correct player')
            return "You need to select a player to vote for", user_name

    def help(self, user_name, *args):
        response = "Hey, you called?  You are " + self.alliance + " aligned \n"
        response += "During the day you have the following actions "
        for x in self.day_actions:
            response += x + " "
        response += "\nDuring the night you have the following actions "
        for x in self.night_actions:
            response += x + " "

        return response, user_name

class Doctor(Vanilla):

    def __init__(self):
        Vanilla.__init__(self)
        self.role = "Doctor"
        self.night_actions['!protect'] = self.protect
        self.check_input['!protect'] = self.check_protect

    def protect(self, target):
        pass

    def check_protect(self):
        pass



class Mafia(Vanilla):

    def __init__(self):
        Vanilla.__init__(self, 'mafia')
        self.role = 'Mafia'
        self.night_actions['!kill'] = self.kill
        self.check_input['!kill'] = self.check_kill

    def check_kill(self,user,command, players):
        try:
            command[1]
        except ValueError:
            return "Please provide a user to kill."
        if command[1] in players:
            return command[1]
        else:
            return "Please return a valid player to kill.  Make sure you spelled their name correctly."


    def kill(self, target, prevented, protected):

        return target
        #if called updates game...needs to be queued









