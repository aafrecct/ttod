class Player():
    '''A model for a player in a truth or dare game.

    Attributes:
    name        -- A string containing the name of the player.
    partner     -- A Player object representing the player's partner if in game. (If None, the player is single)
    used_truths -- A list of the question indexes that have been asked to the player.
    used_dares  -- A list of the dare indexes that have been asked to the player.
    '''
    
    def __init__(self, name, partner=None):
        self.name = name
        self.partner = partner
        self.used_truths = []
        self.used_dares = []
        self.used_questions = []

    def add_used(self, kind, index):
        used_list = self.used_truths if kind == 'truth' else self.used_dares
        used_list.append(index)
        self.used_questions.append(index)

    def is_used(self, index)
        return index in used_questions
