from random import randint, choice, shuffle
from yaml import safe_load

def read_questions(path):
    '''Returns a dictionary with the grouped questions in the given folder.
    Looks for files "truths.yaml" and "dares.yaml" inside the folder.

    Keyword arguments:
    path -- The path to the file containing the questions.
    '''
    questions = {'truths': {}, 'dares': {}}
    for key in questions:
        with open(path + "/{}.yaml".format(key), 'r') as questionsfile:
            questions[key] = safe_load(questionsfile)
    return questions


class TODGame():
    '''This class handles the number of players and picking random questions.

    Attributes:
    players        -- A list of objects of the Player class.
    questions      -- A dictionary from the lines of the files 'truths.yaml' and 'dares.yaml'.
    round_counter  -- A counter of the number of rounds since the beginning.
    player_counter -- A counter indicating the player's whose turn it is.
    '''
    
    def __init__(self, players, language='en'):
        self.players = players 
        # Initial read of questions.
        self.questions = {'truths':[], 'dares':[]}
        questions = read_questions('translations/{0}'.format(language))
        category_indexes = {'truths':{}, 'dares':{}} # A dictionary containing the start and end indexes of categories.
        for kind, value in questions.items():
            globalindex = 0
            for ctg, questionlist in value.items():
                self.questions[kind].extend(questionlist) # Add all truths to a common list, and dares to a different one.
                category_indexes[kind][ctg] = (globalindex, globalindex + len(questionlist) - 1)
                globalindex += len(questionlist)
        for plyr in self.players:
            plyr.create_orders(category_indexes)
        self.round_counter = 0
        self.player_counter = -1    # Begins at -1 so first player is 0.

    def shuffle_players(self):
        '''Reorder the players in game randomly'''
        shuffle(self.players)
    
    def get_random_player(self, player = None):
        '''Returns a random player in the game that is not the player given.'''
        lst = [p for p in self.players if p.name != player.name] if player is not None else self.players
        return choice(lst)

    def is_truth(self, question):
        '''Returns if the provided question is a 'truth' or not (is a 'dare')'''
        b = False
        for lst in self.questions['truths'].values():
            b = b or question in lst
        return b

    def _random_norep_question(self, kind, player):
        kind = choice(['truth', 'dare']) if kind == 'random' else kind
        question = self.questions[kind + 's'][player.kind_order(kind)[player.used_questions[kind]]] 
        player.add_used(kind)
        return question

    def _question_tuple(self, player, question):
        return (player.name, question, player.partner, self.get_random_player(player).name)
        
    def next_player(self):
        if self.player_counter < (len(self.players) - 1):
            self.player_counter += 1
        else:
            self.player_counter -= (len(self.players) - 1)
        player = self.players[self.player_counter]
        return player

    def ask_question(self, kind):
        player = self.players[self.player_counter]
        question = self._question_tuple(player, self._random_norep_question(kind, player))
        return question
