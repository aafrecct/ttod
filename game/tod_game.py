from random import randint, shuffle
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
    players -- A list of objects of the Player class.
    truths  -- A dictionary from the lines of the file 'truths'.
    dares   -- A dictionary from the lines of the file 'dares'.
    '''
    
    def __init__(self, players, language='en'):
        self.players = players
        self.truths = read_questions('translations/{0}/truths'.format(language)
        self.dares = read_questions('translations/{0}/dares'.format(language)

    def change_player_order(self):
        self.players = shuffle(self.players)

    def is_truth(self, question):
        return question in self.truths['all'] + self.truths['single'] + self.truths['couples']  

    def player_question_pool(self, kind, player):
        if kind == 'truth':
            pool_d = self.truths
        elif kind == 'dare':
            pool_d = self.dares
        else:
            pool_d = {'all':self.truths['all'] + self.dares['all'],
                    'single':self.truths['single'] + self.dares['single'],
                    'couples':self.truths['couples'] + self.dares['couples']}
        pool = pool_d['all']
        pool += kind_d['single'] if player.partner == None else pool_d['couples']
        return pool

    def random_norepeat_question(self, pool, player):
        used_questions = player.used_truths if kind
        question_index = randint(0, len(question_list) - len(player.))
        question = question_list[]
        return (question, question_list.index(question))
        


a = TODGame([])
