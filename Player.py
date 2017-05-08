from __future__ import print_function
from pokercards.cards import *
import deuces
import copy

evaluator = deuces.Evaluator()
import random


def evaluate(board, hand):
    board = [deuces.Card.new(card) for card in board]
    hand = [deuces.Card.new(card) for card in hand]
    return evaluator.evaluate(board, hand)

# Takes Card Object, converts to string for evaluator
def card_to_string(card):
    return card.rank + card.suit.lower()

class bet_status(object):
    FOLD = -1


class Player(object):
    """
    hand: List of Cards
    """
    def __init__(self, name, money, c1, c2, c3, bluff, risk, divisor, pot_divisor):
        self.hand = PokerHand([], False)
        self.name = str(name)
        self.risk = risk
        self.bluff = bluff
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.divisor = divisor
        self.money = money
        self.pot_divisor = pot_divisor
        self.owes = 0

    def add_card(self, card):
        self.hand.cards.append(card)

    def empty_hand(self):
        self.hand = PokerHand([], False)

    # Return array of 2 strings
    def hand_to_str(self):
        return [card_to_string(card) for card in self.hand.cards]

    def __str__(self):
        return str([self.name, self.hand, self.money, self.c1, self.c2, self.c3])

    def __repr__(self):
        return "Player(" + str([self.name, self.hand, self.money,  self.c1, self.c2, self.c3])[1:-1] + ")"

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Game(object):

    def __init__(self, list_players, anti=10):
        # Initialize Deck
        self.deck = Deck()
        self.deck.shuffle()

        self.board = []

        #self.players = self.create_players(number_players)
        self.players = list_players
        self.active_players = copy.copy(self.players)

        self.pot = 0
        self.anti = anti
        self.bet = anti    # Current bet at the table
        self.turn = 0   # Index of player's turn
        self.highest_bidder = None # Player with highest bid
        self.round_started = True
        self.game_over = False
        self.rounds = 0


        self.liveprint = False

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
        #print("IM STUCK", self.turn, self.active_players, self.highest_bidder)
        turn = self.turn
        len_active_players = len(self.active_players)

        if self.highest_bidder not in self.active_players:
            self.highest_bidder = None

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
        owes_bet = player.owes > 0
        amount_available = player.money / player.divisor
        will_bluff = random.random() < player.bluff

        def bluff():
            return random.random() < player.bluff

        def judge_initial_cards():
            amount = 0
            big_bet = (amount_available * player.risk)
            if (player.hand.cards[0].rank == player.hand.cards[1].rank):
                if (player.hand.cards[0].rank == 'A' or player.hand.cards[0].rank == 'K' or
                            player.hand.cards[0].rank == 'Q' or player.hand.cards[0].rank == 'J' or
                            player.hand.cards[0].rank == 'T' or player.hand.cards[0].rank == '9' or
                            player.hand.cards[0].rank == '8' or player.hand.cards[0].rank == '7'):
                    if (owes_bet):
                        amount = max(player.owes, player.owes + big_bet)
                    else:
                        amount = amount_available + big_bet
                else:
                    if (owes_bet):
                        if (will_bluff):
                            amount = player.owes + big_bet
                        else:
                            amount = player.owes
                    else:
                        if (will_bluff):
                            amount = (amount_available * player.risk)
                        else:
                            amount = 0
            elif (player.hand.cards[1].rank == 'K' or player.hand.cards[1].rank == 'J' or
                          player.hand.cards[1].rank == 'Q' or player.hand.cards[1].rank == 'A' or
                          player.hand.cards[0].rank == 'K' or player.hand.cards[0].rank == 'J' or
                          player.hand.cards[0].rank == 'Q' or player.hand.cards[0].rank == 'A'):
                check = random.random()
                if (owes_bet):
                    if (check < player.risk):
                        amount =  max(player.owes, player.owes + big_bet)

                    elif (will_bluff):
                        amount =  player.owes
                    else:
                        amount =  bet_status.FOLD
                elif (check < player.risk):
                    amount =  amount_available * player.risk
                else:
                    amount =  0
            else:
                if (owes_bet):
                    if (will_bluff):
                        amount = player.owes + big_bet
                    else:
                        amount =  bet_status.FOLD
                else:
                    if (will_bluff):
                        amount = amount_available * player.risk
                    else:
                        amount =  0
            return amount


        def smart_bet():
            multiplier = 1
            value_mult = value_bet() / 7462

            if self.pot > (player.money * player.pot_divisor):
                multiplier += player.risk

            if (will_bluff and (value_mult > player.risk)):
                multiplier += player.risk

            multiplier += value_mult
            bet = amount_available * multiplier

            lower_bound = (player.owes - self.anti)

            if (bet > lower_bound) and (bet < player.owes):
                bet = player.owes

            return bet



        def value_bet():
            return evaluate(self.board_to_str(), player.hand_to_str())

        def round_one():
            if len(self.board) == 3: return True

        def round_two():
            if len(self.board) == 4: return True

        def round_three():
            if len(self.board) == 5: return True

        def make_bet():
            bet = bet_status.FOLD

            if round_one():
                cutoff = player.c1

            if round_two():
                cutoff = player.c2

            if round_three():
                cutoff = player.c3

            if value_bet() < cutoff:
                bet = smart_bet()
                #print("IM SMART IM GONNA BET", bet)

            return bet



        if (self.board == []):
            bet = judge_initial_cards()
           # print("IM BETTING on round 1:", bet)

        else:
            bet = make_bet()
           # print("IM BETTING on round 234:", bet)


        return bet

    def enforce_bet(self, bet, player):
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
        petty = self.anti

        if (bet == bet_status.FOLD) and (len(self.active_players) == 1):
            bet = player.owes

        if (bet == bet_status.FOLD) and (player.owes == 0):
            bet = player.owes

        if bet == bet_status.FOLD:
            return bet

        if bet > player.money:
            bet = player.money

        if bet < player.owes:
            bet = bet_status.FOLD

        if (bet < (player.owes + petty) ):
            bet = player.owes

        if bet == bet_status.FOLD:
            return bet

        return int(bet)


    def current_turn(self):
        return self.active_players[self.turn]

    def run_round(self):
        self.highest_bidder = None
        while True:
            if len(self.active_players) <= 1:
                break

            # Fix for Bad Code
            if self.turn > (len(self.active_players)-1):
                self.turn = 0

            if (self.current_turn() == self.highest_bidder):
                break

            player = self.current_turn()
            bet = self.player_bet(player)
            bet = self.enforce_bet(bet, player)
            self.make_player_turn(bet, player)

            if self.highest_bidder is None:
                self.highest_bidder = player

        if len(self.board) == 0:
            self.add_to_board(initial=True)
            self.run_round()

        elif len(self.board) < 5:
            self.add_to_board()
            self.run_round()

        else:
            self.finish()

    def run_round(self):
        self.print_live(cards=True)

        self.highest_bidder = None
        while True:
            if len(self.active_players) <= 1:
                break

            # Fix for Bad Code
            if self.turn > (len(self.active_players)-1):
                self.turn = 0

            if (self.current_turn() == self.highest_bidder):
                break

            player = self.current_turn()
            bet = self.player_bet(player)
            bet = self.enforce_bet(bet, player)


            self.print_live(cards=False, name=player.name, bet=bet)
            self.make_player_turn(bet, player)

            if self.highest_bidder is None:
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
        best_player, best_score = None, 8000
        board = self.board_to_str()
        for player in self.active_players:
            score = evaluate(board, player.hand_to_str())
            if score < best_score:
                best_score, best_player = score, player
        return best_player


    def find_wealthiest(self):
        best = -1
        best_player = None
        for player in self.players:
            if player.money > best:
                best_player = player
                best = player.money
        return best_player


    def finish(self):
        best_player = self.find_best_player()
        best_player.money += self.pot
        self.print_live(finish=True)
        #print(self.players)

        self.rounds += 1
        if self.rounds > 100:
            self.game_over = True

        self.reset()



    def reset(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.board = []
        self.pot = 0
        self.round_started = True
        self.turn = 0


        def make_anti():
            for player in self.players:
                if player.money < 10:
                    self.pot += player.money
                    player.money = 0
                else:
                    player.money -= 10
                    self.pot += 10

        def remove_players():
            active_players = []
            for player in self.players:
                if player.money > 0:
                    active_players.append(player)
            return active_players


        make_anti()
        self.active_players = remove_players()



        for player in self.players:
            player.empty_hand()
            player.owes = 0


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

    def print_live(self, cards=True, name=None, bet=None, finish=False):
        if not self.liveprint:
            return

        def deuce_cards(cards):
            return [deuces.Card.new(card) for card in cards]

        if finish:
            winner = self.find_best_player()
            score = evaluate(self.board_to_str(), winner.hand_to_str())
            win_class = evaluator.class_to_string(evaluator.get_rank_class(score))
            print("Player {0} won with hand rank = {1} ({2})\n".format(winner.name, score, win_class))

        elif cards:
            if self.board == []:
                print("PLAYERS CARDS:")
                response = ''
                for player in self.active_players:
                    cards = deuce_cards(player.hand_to_str())
                    response += player.name + " : "
                    print(response, end=" ")
                    deuces.Card.print_pretty_cards(cards)
                    response = ''

            elif len(self.board) <= 5:
                cards = deuce_cards(self.board_to_str())
                print("BOARD CARDS:", end=" ")
                deuces.Card.print_pretty_cards(cards)
        else:
            if bet == bet_status.FOLD:
                bet = 'FOLD'
            if bet == 0:
                bet = 'PASS'
            print(name, "bets", bet)


    def run_game(self):
        while not self.game_over:
            self.deal()
            self.run_round()
def main():
    game = Game(4)

    while not game.game_over:
        game.deal()
        game.run_round()
        #game.print_game()
        print ('')

if __name__ == '__main__':
    main()
