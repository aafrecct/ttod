from random import randint, choice, shuffle
from loader import load_questions
from copy import copy

class Question:

    def __init__(self, question: str, kind: str, category: str, spice: int, movement: int):
        self.question = question
        self.kind = kind
        self.category = category
        self.spice = spice
        self.movement = movement





class TODGame:
    """This class handles the number of players and picking random questions.

    Attributes:
    players        -- A list of objects of the Player class.
    questions      -- A dictionary from the lines of the files 'truths.yaml' and 'dares.yaml'.
    round_counter  -- A counter of the number of rounds since the beginning.
    player_counter -- A counter indicating the player's whose turn it is.
    """

    def __init__(self, 
                 players: list[Player], 
                 min_spice: int, 
                 max_spice: int, 
                 max_movement: int, 
                 reorder_each_round: bool,
                 shared_question_list: bool
                 ):
        self.min_spice = min_spice
        self.max_spice = max_spice
        self.max_movement = max_movement
        self.players = players
        self.single_players = list(filter(lambda p: not p.partner, players))
        self.raw_questions = load_questions()
        self.shared_question_list = shared_question_list
        if shared_question_list:
            self.questions = self.__process_questions(self.raw_questions)
        else:
            ques
            self.questions = {player: self.__process_questions(self.raw_questions, player) 
                              for player in players}
        self.reorder_each_round
        self.round_counter = 0
        self.player_counter = 0
    
    def __process_questions(self, raw_questions):
        questions = {}
        for kind, kind_questions in raw_questions:
            questions[kind] = {}
            for question in kind_questions:
                question = Question(**question, kind=kind)
                
                if question.category not in questions[kind]:
                    questions[kind][question.category] = {}
                    
                

    def shuffle_players(self):
        """Reorder the players in game randomly"""
        shuffle(self.players)

    def get_random_player(self, player=None):
        """Returns a random player in the game that is not the player given."""
        possible_players = [p for p in self.players if p.name != player.name]
        return choice(possible_players)

    def get_partner_player(self, player):
        """Returns the partner player if player has one or a single player"""
        if player.partner:
            possible_players = player.partner
        else:
            possible_players = [p for p in self.single_players if p.name != player.name]
        return choice(possible_players)

    def get_random_number(self, bound=5):
        return randint(0, 5)

    def get_questions(self, player):
        if self.

    def random_non_repeating_question(self, kind, player):
        """ Returns a random question that the player has not answered before"""
        

    def _random_norep_question(self, kind, player):
        kind = choice(['truth', 'dare']) if kind == 'random' else kind
        question = self.questions[kind + 's'][player.kind_order(kind)[
            player.used_questions[kind]]]
        player.add_used(kind)
        return question

    def _question_tuple(self, player, question):
        return (player.name, question, player.partner,
                self.get_random_player(player).name)

    def next_player(self):
        if self.player_counter < (len(self.players) - 1):
            self.player_counter += 1
        else:
            self.player_counter -= (len(self.players) - 1)
        player = self.players[self.player_counter]
        return player

    def ask_question(self, kind):
        player = self.players[self.player_counter]
        question = self._question_tuple(
            player, self._random_norep_question(kind, player))
        return question
