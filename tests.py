import unittest
from Player import *
from pokercards.cards import *


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game(4)
        self.game.deal()
        self.game.add_to_board(initial=True)

    def test_player_bet(self):
        game = self.game
        game.player_bet()

        self.assertEquals(game.bet, 10)
        self.assertEquals(game.turn, 1)

        game.turn = len(game.active_players) - 1
        game.player_bet()
        self.assertEquals(game.turn, 0)

        game.turn = 3
        game.highest_bidder = game.active_players[3]
        game.player_bet()
        self.assertEquals(game.bet, 0)
        self.assertEquals(game.turn, 0)





class TestCard(unittest.TestCase):
    def test_card_to_string(self):
        self.assertEquals(card_to_string(Card('T', 'H')), 'Th')

if __name__ == "__main__":
    unittest.main()