"""
The class Game should take a list of players as input so that
it can generate games for the next generation

also, the Game class should have a deepcopy of each players so
that each game play won't change the values of players

  - self.players (ListOfPlayers)

the list of players needs to be a set

bluff and risk
"""
from Player import *
from Game import *
from random import *
from copy import deepcopy
from math import ceil

class Evaluator():
    def __init__(self, listOfPlayers):
        self.players = listOfPlayers
        self.numOfPlayers = len(this.players)
        self.games = []
        self.playerMoney = dict()
        self.topPlayer = []

    def gamePlay(self, numInGame = 8, numOfGames = 5):
        ## if the game class takes a list of players
        for i in range(numOfGames):
            players = copy.deepcopy(this.players)
            for j in range(int(math.ceil(this.numOfPlayers / numInGame))):
                lop = []
                for k in range(numInGame):
                    p =  random.choice(players)
                    player.remove(p)
                    lop.append(p)
                self.games.append(Game(lop))
        return self.games

    def topPlayers(self, numOfChoosen = 20):
        for g in self.games:
            for p in g.players:
                if p in self.playerMoney:
                    self.playerMoney[p] = self.playerMoney[p] + p.money
                else:
                    self.playerMoney[p] = p.money
        pm = copy.deepcopy(self.playerMoney)
        for i in range(numOfChoosen):
            self.topPlayer.append(max(pm))
            del pm[max(pm)]
        return self.topPlayer
            
    def derive(self, num, ): ## percentage, shiftingRange):
        new_generation = []
        tp = copy.deepcopy(self.topPlayer)
        for i in range(num):
            p = random.choice(tp)
            q = random.choice(tp)
            while (p == q):
                q = random.choice(tp)
            # new_generation.appand(Player(p.name + q.name, (p.bluff + q.bluff) / 2, (p.risk + q.risk) / 2, ...))
        return new_generation

def main(players, numOfIter):
    genetic = Evaluator(players)
    for i in range(numOfIter):
        genetic.gamePlay()
        genetic.topPlayer()
        new_generation = genetic.derive(len(players))
        main(new_generation, numOfIter - 1)
