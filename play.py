import analyze
import sqlite3
import analyze
import random
import ast

database = 'perf_db.sqlite'

def play_game(start):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    surface = start
    moves = []
    while True:
        moves.append(surface)
        piece = random.choice(list(analyze.pieces.keys()))
        #print(piece)
        connections = analyze.connect_surface(surface)
        choices = []
        for surf in connections[piece]:
            c.execute('SELECT * FROM surfaces WHERE surface = ?', ("{}".format(surf),))
            data = c.fetchone()
            if data != None:
                choices.append(data)
        if len(choices) == 0:
            value = random.choice([0, 1, 2, 3, 4])
            #print('Lost')
            if break
        max_rank = max([rank for (name, number, rank) in choices])
        for (name, number, rank) in choices:
            if rank < max_rank:
                choices.remove((name, number, rank))
        max_number = max([number for (name, number, rank) in choices])
        for (name, number, rank) in choices:
            if number < max_number:
                choices.remove((name, number, rank))
        #if len(choices) > 1:
            #print('Multiple')
        choice = random.choice(choices)
        surface = ast.literal_eval(choice[0])
        #print(choice)
    return moves

def multiple_runs(runs):
    games = 0
    best = 0
    total = 0
    while games < runs:
        result = len(play_game([0, -1, 0, -2, 0, 0, -1, 1]))
        total += result
        if result > best:
            best = result
        games += 1
        if games % 100 == 0:
            print(games)
    print(best)
    print(total/games)

if __name__ == "__main__":
    multiple_runs(1000)
