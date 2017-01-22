"""Roles extend from Vanilla, Mafia roles would extend from mafia etc.
get_actions just gets all the acceptable actions for that user at that time.
The vote/kill/etc actions take the command entered by the user parse it how they
think it should be parsed and then they do something with it."""

class Vanilla(object):

    def __init__(self, alliance='town'):
        self.alliance = alliance
        self.resolve = alliance
        self.role = 'Vanilla'
        self.day_actions = {'!vote': self.vote}
        self.night_actions = {}
        self.resolve = None

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
                return "Please select an appropriate player", '@'+user_name
        except:
            print('select a correct player')
            return "You need to select a correct player to vote for.", '@'+user_name


class Mafia(Vanilla):

    def __init__(self):
        Vanilla.__init__(self, 'mafia')
        self.night_actions['!kill'] = self.kill

    def kill(self, target):
        #if called updates game...needs to be queued
        pass








