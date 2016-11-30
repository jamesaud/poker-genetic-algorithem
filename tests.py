import unittest
from Player import *
from pokercards.cards import *


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game(4)
        self.game.deal()
        self.game.add_to_board(initial=True)


    def test_create_players(self):
        game = Game(5)
        self.assertEquals(5, len(game.active_players), len(game.players))

    def test_deal(self):
        game = Game(5)
        game.deal()
        for player in game.players:
            self.assertEquals(2, len(player.hand.cards))

    def test_add_to_board(self):
        game = Game(5)
        game.add_to_board(initial=True)
        self.assertEquals(len(game.board), 3)
        game.add_to_board()
        self.assertEquals(len(game.board), 4)

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