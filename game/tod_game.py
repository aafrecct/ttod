from random import randint, choice, shuffle
:%s/^/\=printf('%-4d', line('.'))

def read_questions(path):
    '''Returns a dictionary with the grouped questions in the given file.

    Keyword arguments:
    path -- The path to the file containing the questions.
    '''
    
    with open(path, 'r') as questionsfile:
        questions = {}
        last_header = ""
        for line in questionsfile.readlines():
            l = line[:-1]
            if l[0] == '[':
                last_header = l
                questions[l] = []
            else:
                questions[last_header].append((int(l[:5]), l[5:))

    return questions


class TODGame():
    '''This class handles the number of players and picking random questions.

    Attributes:
    players        -- A list of objects of the Player class.
    truths         -- A dictionary from the lines of the file 'truths'.
    dares          -- A dictionary from the lines of the file 'dares'.
    round_counter  -- A counter of the number of rounds since the beginning.
    player_counter -- A counter indicating the player's whose turn it is.
    '''
    
    def __init__(self, players, language='en'):
        self.players = players
        self.truths = read_questions('translations/{0}/truths'.format(language)
        self.dares = read_questions('translations/{0}/dares'.format(language)
        self.round_counter = 0
        self.player_counter = -1

    def change_player_order(self):
        self.players = shuffle(self.players)
    
    def get_random_player(self, player):
        return choice([p for p in self.players if p.name != player.name])

    def is_truth(self, question):
        return question in self.truths['all'] + self.truths['single'] + self.truths['couples']  

    def _player_question_pool(self, kind, player):
        if kind == 'truth':
            pool_d = self.truths
        elif kind == 'dare':
            pool_d = self.dares
        else:
            pool_d = {}
            for key in self.truths.keys():
                pool_d[key] = self.truths[key] + self.dares[key]
        pool = pool_d['all']
        pool += pool_d['single'] if player.partner == None else pool_d['couples']
        return pool

    def _random_norepeat_question(self, kind, player):
        q_pool = _player_question_pool(kind, player)
        used_of_the_kind = {'truth':player.used_truths,
                            'dare':player.used_dares,
                            'both':player.used_questions}
        max_questions = len(qpool) - len(used_of_the_kind[kind])
        question = q_pool[randint(0, max_questions - 1)]
        if player.is_used(question[0]):
            question = q_pool[max_questions + used_of_the_kind[kind].index(question[0]) - 1]
        player.add_used(question[0]))
        return question

    def _question_tuple(self, player, question_str):
        return (player.name, question_str, player.partner, get_random_player(player))
        
    def next_person(self, kind):
        self.player_counter += 1 if self.player_counter < len(self.players) - 1 else (-len(self.players)+1)
        player = self.players[self.player_counter]
        question = _question_tuple(self, player, _random_norepeat_question(kind, player))

    def different_question(self, kind):
        player = self.players[self.player_counter]
        question = _question_tuple(self, player, _random_norepeat_question(kind, player))

