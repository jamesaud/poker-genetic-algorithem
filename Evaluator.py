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
        
        
# ------------------------------------------------------
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
        self.playerWin = dict()
        for p in self.players:
            self.playerWin[p] = 0
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

    def topPlayers(self, numOfChoosen = 20, retain = 0.2):
        for g in self.games:
            winner = g.find_best_player()
            self.playerWin[winner] = self.playerWin[Winner] + 1
        pm = copy.deepcopy(self.playerMoney)
        numOfRetain = len(pm) * retain
        # this part chooses the best players
        for i in range(numOfChoosen):
            self.topPlayer.append(max(pm))
            del pm[max(pm)]
        # this part adds(retain) some of other players into the top players 
        for j in range(numOfRetain):
            p = random.choice(pm)
            while (p in self.topPlayer):
                p = random.choice(pm)
            self.topPlayer.append(p)
        return self.topPlayer
            
    def derive(self, num, shift):
        def merge(p1, p2, i):
            newBluff = (p1.bluff + p2.bluff) / 2
            newRisk = (p1.risk + p2.risk) / 2
            newPlayer = Player(i, newBluff, newRisk, 100)
            return newPlayer
        # this part is for mutation
        def mutate(p):
            if random.random() < shift:
                if random.random() < .5:
                    p.bluff = p.bluff + random.random()
                if random.random() > .5:
                    p.risk = p.risk + random.random()
        new_generation = []
        tp = copy.deepcopy(self.topPlayer)
        for n in tp:
            mutate(n)
        # this part is for deriving
        for i in range(num):
            p = random.choice(tp)
            q = random.choice(tp)
            while (p == q):
                q = random.choice(tp)
            new_generation.appand(merge(p, q, i))
        return new_generation

def main(players, numOfIter):
    if numOfIter == 0:
        return players
    genetic = Evaluator(players)
    for i in range(numOfIter):
        genetic.gamePlay()
        genetic.topPlayer()
        new_generation = genetic.derive(len(players))
        main(new_generation, numOfIter - 1)

# p is the list of players generated automatically
p = [] 
for i in range(50):
    p.append(Player(i, random.uniform(1, -1), random.uniform(1, -1)))

