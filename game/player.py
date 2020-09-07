from random import shuffle

class Player():
    '''A model for a player in a truth or dare game.

    Attributes:
    name        -- A string containing the name of the player.
    partner     -- A Player object representing the player's partner if in game. (If None, the player is single)
    used_truths -- A list of the question indexes that have been asked to the player.
    used_dares  -- A list of the dare indexes that have been asked to the player.
    '''
    
    def __init__(self, name, partner=None, categories=set()):
        self.name = name
        self.partner = partner
        self.categories = {'all'} | categories
        self.truth_order = []
        self.dare_order = []
        self.used_questions = {'truth': 0, 'dare': 0}
    
    def set_categories(self, categories = set()):
        self.categories |= categories

    def create_orders(self, category_indexes):
        ''' Randomizes the order of truths and dares for this player.'''
        ti = category_indexes['truths']
        di = category_indexes['dares']
        for ctg in self.categories:
            self.truth_order.extend(range(ti[ctg][0], ti[ctg][1]))
            self.dare_order.extend(range(di[ctg][0], di[ctg][1]))
        shuffle(self.truth_order)
        shuffle(self.dare_order)

    def kind_order(self, kind):
        return self.truth_order if kind == 'truth' else self.dare_order

    def add_used(self, kind):
        ''' Adds one to the traker of questions that are already asked.'''
        self.used_questions[kind] += 1
