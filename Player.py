from pokercards.cards import *
import deuces
import copy

evaluator = deuces.Evaluator()

def evaluate(board, hand):
    board = [deuces.Card.new(card) for card in board]
    hand = [deuces.Card.new(card) for card in hand]
    return evaluator.evaluate(board, hand)

# Takes Card Object, converts to string for evaluator
def card_to_string(card):
    return card.rank + card.suit.lower()

class bet_status(object):
    FOLD = "FOLD"


class Player(object):
    """
    hand: List of Cards
    """
    def __init__(self, name, bluff, risk, money):
        self.hand = PokerHand([], False)
        self.name = name
        self.bluff = bluff
        self.risk = risk
        self.money = money
        self.owes = 0

    def add_card(self, card):
        self.hand.cards.append(card)

    def empty_hand(self):
        self.hand = PokerHand([], False)

    # Return array of 2 strings
    def hand_to_str(self):
        return [card_to_string(card) for card in self.hand.cards]

    def __str__(self):
        return str([self.name, self.hand, self.money])

    def __repr__(self):
        return "Player(" + str([self.name, self.hand, self.money])[1:-1] + ")"



class Game(object):

    def __init__(self, number_players, anti=0):
        # Initialize Deck
        self.deck = Deck()
        self.deck.shuffle()

        self.board = []

        self.players = self.create_players(number_players)
        self.active_players = copy.copy(self.players)

        self.pot = 0
        self.anti = anti
        self.bet = anti    # Current bet at the table
        self.turn = 0   # Index of player's turn
        self.highest_bidder = None # Player with highest bid
        self.round_started = True
        self.game_over = False

    def create_players(self, number):
        player_list = [] # List of Players
        for i in range(number):
            player = Player(str(i), .5, .5, 100)
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


    """
    Changs the players turn and removes any players who fold
    """
    def make_player_turn(self, bet, player):

        turn = self.turn
        len_active_players = len(self.active_players)

        if bet < player.owes:
            bet = bet_status.FOLD


        if (bet == bet_status.FOLD) and (player.owes == 0):
            return None

        # Fold, Match, or Raise
        if bet == bet_status.FOLD: # Fold
            self.active_players.remove(self.current_turn())
            self.turn = turn % len_active_players
            return None

        elif bet == player.owes:
            self.turn = (turn + 1) % len_active_players


        else:
            self.highest_bidder = player
            self.turn = (turn + 1) % len_active_players

            for play in self.active_players:
                if play != player:
                    play.owes += (bet - player.owes)

        self.pot += bet
        player.money -= bet
        player.owes = 0




    def player_bet(self, player):
        def value_bet():
            if (self.board == []):
                if (player.hand.cards[0].rank == player.hand.cards[1].rank):
                    return 4
                if (player.hand.cards[1].rank == 'K' or player.hand.cards[1].rank == 'J' or 
                    player.hand.cards[1].rank == 'Q' or player.hand.cards[1].rank == 'A' or
                    player.hand.cards[0].rank == 'K' or player.hand.cards[0].rank == 'J' or 
                    player.hand.cards[0].rank == 'Q' or player.hand.cards[0].rank == 'A'):
                    return 3
                elif (self.bet != 0):
                    if (player.risk > 0):
                        return self.bet
                    else: return bet_status.FOLD
                else: return 0
            value = 7462 - evaluate(self.board_to_str(), player.hand_to_str()) + (1000 * player.bluff)
            pot = self.pot
            money = player.money
            bet = value / 7462
            threshold = value - (1000 * player.risk)
            if (threshold > 6000 and self.bet > 0):
                return bet_status.FOLD
            if (pot > (money / 4)):
                bet = (int)(bet + (bet * player.risk)) * 50
            else:
                bet = (int)(bet + (bet * player.risk)) * 25
            return bet
        bet = value_bet()
        if (bet == bet_status.FOLD):
            return bet
            bet = player.money
        if (bet < 2):
            bet = 0
        return bet

    def enforce_bet(self, bet, player, petty=10):
        """
        Enfore rules for the player bet.
        1. If the bet is more than the players money, remake the bet to their max money.
        2. If the bet is less than the current bet, force the player to fold.
        3. If the bet is negative, force the player to bet 0.
        0. Petty: If the raise is less than this amount, change the bet to 0 to stop infinite betting.

        :param bet: int, the amount the player wants to bet
        :param player: Player, the current player who is betting
        :return: int, the enforced bet
        """
        petty = player.owes + petty

        if (bet == bet_status.FOLD) and (len(self.active_players) == 1):
            bet = self.owes

        if (bet < petty):
            bet = player.owes

        if bet > player.money:
            bet = player.money

        if bet < player.owes:
            bet = bet_status.FOLD

        return bet


    def current_turn(self):
        return self.active_players[self.turn]

    def run_round(self):
        while True:
            #print(self.turn, len(self.active_players) - 1)
            if len(self.active_players) <= 1:
                break

            # Fix for Bad Code
            if self.turn > (len(self.active_players)-1): self.turn = 0

            if (self.current_turn() == self.highest_bidder):
                break


            player = self.current_turn()
            bet = self.player_bet(player)
            bet = self.enforce_bet(bet, player, 2)
            self.make_player_turn(bet, player)

            if not self.highest_bidder:
                self.highest_bidder = player

        if len(self.board) == 0:
            self.add_to_board(initial=True)
            self.run_round()

        elif len(self.board) < 5:
            self.add_to_board()
            self.run_round()

        else:
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
        self.print_game()
        self.reset()


    def reset(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.board = []
        self.pot = 0
        self.round_started = True
        self.turn = 0


        def remove_players():
            active_players = []
            for player in self.players:
                if player.money > 0:
                    active_players.append(player)
            return active_players

        self.active_players = remove_players()


        for player in self.players:
            player.empty_hand()
            player.owes = self.anti


        if len(self.active_players) == 1:
            self.game_over = True


        # Rotate Players
        first_player = self.active_players.pop(0)
        self.active_players.append(first_player)

        self.highest_bidder = None  # Player with highest bid


    def board_to_str(self):
        return [card_to_string(card) for card in self.board]


    def print_game(self):

        print("\n")
        print("TABLE CARDS:")
        print(self.board)
        print("PLAYERS:")
        for player in self.players:
            print(player)
        print("BOARD:")
        print(self.board)

def main():
    game = Game(4)

    while not game.game_over:
        game.deal()
        game.run_round()
        #game.print_game()
        print ('')

if __name__ == '__main__':
    main()
