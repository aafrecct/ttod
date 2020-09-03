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
    truths         -- A dictionary from the lines of the file 'truths.yaml'.
    dares          -- A dictionary from the lines of the file 'dares.yaml'.
    round_counter  -- A counter of the number of rounds since the beginning.
    player_counter -- A counter indicating the player's whose turn it is.
    '''
    
    def __init__(self, players, language='en'):
        self.players = players
        self.questions = read_questions('translations/{0}'.format(language))
        self.round_counter = 0
        self.player_counter = -1

    def shuffle_players(self):
        shuffle(self.players)
    
    def get_random_player(self, player):
        return choice([p for p in self.players if p.name != player.name])

    def is_truth(self, question):
        b = False
        for lst in self.questions['truths'].values():
            b = b or question in lst
        return b

    def player_question_pool(self, kind, player):
        if kind == 'truth':
            pool_d = self.questions['truths']
        elif kind == 'dare':
            pool_d = self.questions['dares']
        else:
            pool_d = {}
            for key in self.questions['truths'].keys():
                pool_d[key] = self.truths[key] + self.dares[key]
        pool = pool_d['all']
        pool += pool_d['single'] if player.partner is None else pool_d['couples']
        return pool

    def _random_norep_question(self, kind, player):
        q_pool = self.player_question_pool(kind, player)
        used_of_the_kind = {'truth': player.used_truths,
                            'dare': player.used_dares,
                            'both': player.used_questions}
        max_questions = len(q_pool) - len(used_of_the_kind[kind])
        question = q_pool[randint(0, max_questions - 1)]
        if player.is_used(question[0]):
            question = q_pool[max_questions + used_of_the_kind[kind].index(question[0]) - 1]
        player.add_used(question[0])
        return question

    def _question_tuple(self, player, question):
        return (player.name, question[1], player.partner, self.get_random_player(player).name)
        
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