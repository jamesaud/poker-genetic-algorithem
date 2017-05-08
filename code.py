import deuces
import copy

evaluator = deuces.Evaluator()


def evaluate(board, hand):
    board = [deuces.Card.new(card) for card in board]
    hand = [deuces.Card.new(card) for card in hand]
    return evaluator.evaluate(board, hand)


p = [deuces.Card.new('2s'), deuces.Card.new('5h')]
b = [deuces.Card.new('3c'), deuces.Card.new('4c'), deuces.Card.new('5h')]
score = evaluator.evaluate(p, b)
print(score)