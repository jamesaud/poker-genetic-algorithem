"""
The class Game should take a list of players as input so that
it can generate games for the next generation

also, the Game class should have a deepcopy of each players so
that each game play won't change the values of players

  - self.players (ListOfPlayers)

the list of players needs to be a set

bluff and risk
"""
from __future__ import print_function
import sys
from Player import *
import random
from copy import deepcopy
from math import ceil
import math
from collections import defaultdict
# Scatter Plot
import numpy as np
import matplotlib.pyplot as plt

Evo_Map = []
starting_money = 1000
num_players = 100  # Players in a Generation
numOfGames = 5 # Number of games played in a generation
numInGame = 5  # Players in a single game
numOfChoosen = 20
numOfIter = 30
mutation = .1
mutation_amount = 2
numOfGen = 1 # Don't Change!
graph_cutoff = 10
anti = 20



class Evaluator():
    def __init__(self, listOfPlayers):
        self.players = listOfPlayers
        self.numOfPlayers = len(self.players)
        self.games = []
        self.playerWin = {}
        for player in self.players:
            self.playerWin[player] = 0
        self.topPlayer = []

    """
    Returns a list of games that should be played.
    """
    def gamePlay(self, print_game=False):
        game_num = 0
        ## if the game class takes a list of players
        for i in range(numOfGames):
            players = copy.deepcopy(self.players)
            for j in range(int(math.ceil(self.numOfPlayers / numInGame))):
                lop = []
                for k in range(numInGame):
                    if k < (.5 * numInGame):
                        p = gen_random_player()
                    else:
                        p = random.choice(players)
                        players.remove(p)
                    lop.append(p)

                self.games.append(Game(lop, anti=anti))

        if print_game:
            self.games[-1].liveprint = True

        for game in self.games:
            sys.stdout.write("\rRunning Game " + str(game_num))
            game_num += 1
            game.run_game()

    """
    Appends top players of the generation to the list of top players
    """
    def topPlayers(self):
        # Update win counts for every game played
        for g in self.games:
            winner = g.find_wealthiest()
            self.playerWin[winner] = self.playerWin[winner] + 1

        pm = copy.deepcopy(self.playerWin)

        # this part chooses the best players
        for i in range(numOfChoosen):
            key_to_delete = max(pm, key=lambda k: pm[k])
            self.topPlayer.append(key_to_delete)
            del pm[key_to_delete]




    """
    Generate new generation.
    """
    def derive(self, num):

        # this part is for merging two parents together
        def merge(p1, p2, i):
            def combine(var1, var2):
                return random.choice([var1, var2])

            newc1 = combine(p1.c1, p2.c1)
            newc2 = combine(p1.c2, p2.c2)
            newc3 = combine(p1.c3, p2.c3)
            new_d = combine(p1.divisor, p2.divisor)
            new_b = combine(p1.bluff, p2.bluff)
            new_r = combine(p1.risk, p2.risk)
            new_pd = combine(p1.pot_divisor, p2.pot_divisor)
            newPlayer = Player(i, starting_money, newc1, newc2, newc3, new_b, new_r, new_d, new_pd)
            return newPlayer

        # this part is for mutation
        def mutate(p):
            def mute(attribute):
                if random.random() < mutation:
                    if random.random > .5:
                        attribute += random.uniform(-1, 1) * 100 * mutation_amount
                return attribute

            def mute_br(attribute):
                if random.random() < mutation:
                    attribute += random.uniform(-1, 1) / 10 * mutation_amount
                    if attribute < 0:
                        attribute = 0
                return attribute

            def mute_div(attribute):
                if random.random() < mutation:
                    if random.random() > .5:
                        return attribute + .5 * mutation_amount
                    else:
                        new = attribute - .5 * mutation_amount
                        if new < 3:
                            new = 3
                        return new
                return attribute

            p.c1 = mute(p.c1)
            p.c2 = mute(p.c2)
            p.c3 = mute(p.c3)
            p.bluff = mute_br(p.bluff)
            p.risk = mute_br(p.risk)
            p.divisor = mute_div(p.divisor)
            p.pot_divisor = mute_br(p.pot_divisor)

        new_generation = []
        tp = copy.deepcopy(self.topPlayer)
        #for n in tp:
        #    mutate(n)
        # this part is for deriving
        for i in range(num):
            p = random.choice(tp)
            q = random.choice(tp)
            m = merge(p, q, i)
            mutate(m)
            new_generation.append(m)
        return new_generation

    #def reset(self):
    #    self.games = []
    #    self.playerWin = {}
    #    for player in self.players:
    #        self.playerWin[player] = 0

def main(players, numOfIter, numOfGen):
    print_game = False

    if numOfIter % 10 == 0:
        print()
        print("=" * 50)
        print("Generation: ", numOfGen)
        print("=" * 50)
        print_game = True

    if numOfIter == 0:
        return players
    genetic = Evaluator(players)
    genetic.gamePlay(print_game)
    genetic.topPlayers()
    for p in genetic.topPlayer:
        Evo_Map.append([numOfGen, p])
    new_generation = genetic.derive(num_players)
    #    genetic.reset()
    #print(new_generation)

    main(new_generation, numOfIter - 1, numOfGen + 1)

# p is the list of players generated automatically
p = []

def add_money1():
    return random.uniform(1000, 7000)

def add_money2():
    return random.uniform(1000, 7000)

def add_money3():
    return random.uniform(1000, 7000)

def add_d():
    return random.uniform(2, 18)

def bluff_risk():
    return random.uniform(1, 0)

def pot_div():
    return random.uniform(.2, 1.8)

def gen_random_player():
    return Player(i, starting_money, add_money1(), add_money2(), add_money3(), bluff_risk(), bluff_risk(), add_d(), pot_div())

for i in range(num_players):
    p.append(gen_random_player())


if __name__ == '__main__':
    main(p, numOfIter, numOfGen)
    xs = []
    ys = []
    br_xs = []
    br_ys = []
    count = 0
    for ls in Evo_Map:
        if count % graph_cutoff == 0:
            xs += [ls[0], ls[0] + 0.25, ls[0] + 0.5]
            ys.append(ls[1].c1)
            ys.append(ls[1].c2)
            ys.append(ls[1].c3)

            br_xs += [ls[0], ls[0] + 0.25, ls[0] + 0.5, ls[0] + 0.75]
            br_ys.append(ls[1].bluff)
            br_ys.append(ls[1].risk)
            br_ys.append(ls[1].divisor)
            br_ys.append(ls[1].pot_divisor)

        count += 1

    # For the cutoffs
    X = np.array(xs)
    Y = np.array(ys)
    colors = np.array(["R", "G", "B",] * len(xs) * 3)
    area = np.array([15 * np.pi] * len(xs) * 3)
    plt.scatter(X, Y, s = area, c = colors, alpha = 0.5)
    plt.show()

    # For the risks
    X = np.array(br_xs)
    Y = np.array(br_ys)
    colors = np.array(["M", "C", "Y", "B"] * len(br_xs) * 4)
    area = np.array([15 * np.pi] * len(br_xs) * 4)
    plt.scatter(X, Y, s=area, c=colors, alpha=0.5)
    plt.show()

    
