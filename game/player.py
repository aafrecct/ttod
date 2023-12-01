from random import shuffle

class Player():
    '''A model for a player in a truth or dare game.

    Attributes:
    name        -- A string containing the name of the player.
    partner     -- A Player object representing the player's partner if in game. (If None, the player is single)
    used_truths -- A list of the question indexes that have been asked to the player.
    used_dares  -- A list of the dare indexes that have been asked to the player.
    '''
    
    def __init__(self, name: str, partner: list[Player]=[], categories=set()):
        self.name = name
        self.partner = partner
        self.categories = {'all'} | categories
        self.choices = ""
    
    def add_categories(self, categories = set()):
        self.categories |= categories
