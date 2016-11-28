from pokercards.cards import *
import deuces

evaluator = deuces.Evaluator()

def evaluate(board, hand):
    board = [deuces.Card.new(card) for card in board]
    hand = [deuces.Card.new(card) for card in hand]
    return evaluator.evaluate(board, hand)

# Takes Card Object, converts to string for evaluator
def card_to_string(card):
    return card.rank + card.suit.lower()

class Player(object):
    """
    hand: List of Cards
    """
    def __init__(self, name, bluff, risk, money, game):
        self.hand = PokerHand([], False)
        self.name = name
        self.bluff = bluff
        self.risk = risk
        self.money = money
        self.game = game

    def add_card(self, card):
        self.hand.cards.append(card)

    def empty_hand(self):
        self.hand = PokerHand([], False)

    # Return array of 2 strings
    def hand_to_str(self):
        return [card_to_string(card) for card in self.hand.cards]

    def __str__(self):
        return str([self.name, self.hand, self.money])


class Game(object):

    def __init__(self, number_players, anti=10):
        # Initialize Deck
        self.deck = Deck()
        self.deck.shuffle()

        self.board = []

        self.players = self.create_players(number_players)
        self.active_players = self.players

        self.pot = 0
        self.anti = anti
        self.bet = anti    # Current bet at the table
        self.turn = 0   # Index of player's turn
        self.highest_bidder = self.players[0] # Player with highest bid
        self.round_started = False
        self.game_over = False

    def create_players(self, number):
        player_list = [] # List of Players
        for i in range(number):
            player = Player(str(i), .5, .5, 100, self)
            player_list.append(player)
        return player_list

    def deal(self):
        for player in self.players:
            player.add_card(self.deck.pop())
            player.add_card(self.deck.pop())

    def add_to_board(self, initial=False):
        if initial:
            for i in range(3):
                self.board.append(self.deck.pop())
        else:
            self.board.append(self.deck.pop())

    def print_players(self):
        for player in self.players:
            print(player)


    def player_turn(self):
        if (self.active_players[self.turn] == self.highest_bidder) and self.round_started:
            self.bet = 0
            self.turn = 0
            self.round_started = False
            return False

        else:
            if len(self.active_players) <= 2:
                return False
            print self.active_players
            player = self.active_players[self.turn]
            bet = self.player_bet(player)
            self.round_started = True

            # Fold, Match, or Raise
            if bet == -1: # Fold
                del self.active_players[self.turn]
                self.turn = self.turn % len(self.active_players)

            elif bet == self.bet:
                self.turn = (self.turn + 1) % len(self.active_players)
                self.pot += bet

            else:
                self.pot += bet
                self.bet = bet
                self.highest_bidder = player
                self.turn = (self.turn + 1) % len(self.active_players)

            return True

    def player_bet(self, player):
        def value_bet():
            if (self.board == []):
                return 0
            value = 7462 - evaluate(self.board_to_str(), player.hand_to_str()) + (1000 * player.bluff)
            pot = self.pot
            money = player.money
            bet = value / 7462
            if (pot > (money / 4)):
                bet = (bet + (bet * player.risk)) * 50
            else:
                bet = (bet + (bet * player.risk)) * 25
            return bet
        bet = value_bet()
        if (bet > player.money):
            bet = player.money
        if (bet < 5):
            bet = 0
        if (bet < self.bet):
            return -1
        player.money -= bet
        return bet

    def run_round(self):

        while self.player_turn():
            pass

        if len(self.board) == 0:
            self.add_to_board(initial=True)
            self.run_round()

        elif len(self.board) < 5:
            self.add_to_board()
            self.run_round()

        else:
            self.print_game()
            self.finish()

    def find_best_player(self):
        best_player, best_score = None, -1
        board = self.board_to_str()

        for player in self.active_players:
            score = evaluate(board, player.hand_to_str())
            if score > best_score:
                best_score, best_player = score, player
        return best_player

    def finish(self):
        best_player = self.find_best_player()
        best_player.money += self.pot
        self.reset()


    def reset(self):

        self.deck = Deck()
        self.deck.shuffle()
        self.board = []
        self.pot = 0
        self.bet = self.anti  # Current bet at the table
        self.round_started = False


        new_players = []
        for player in self.players:
            player.empty_hand()
            if player.money > 0:
                new_players.append(player)

        self.players = new_players

        if len(self.players) == 1:
            self.game_over = True

        def rotate_players():
            first_player = self.players.pop(0)
            self.players.append(first_player)

        rotate_players()
        self.highest_bidder = self.players[0]  # Player with highest bid

        self.active_players = self.players


    def board_to_str(self):
        return [card_to_string(card) for card in self.board]


    def print_game(self):
        for player in self.players:
            print(player)


def main():
    game = Game(4)

    while not game.game_over:
        game.deal()
        game.run_round()
        game.print_game()
        print ('')

if __name__ == '__main__':
    main()
