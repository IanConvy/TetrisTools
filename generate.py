import sqlite3
import analyze
import ast

def generate_next_perfects(cursor):
    counter = 0
    rows = set(cursor.fetchall())
    for row in rows:
        perf_number = 0
        surface = ast.literal_eval(row[0])
        connections = analyze.connect_surface(surface)
        for piece in connections.keys():
            perf_piece = False
            for next_surface in connections[piece]:
                if (str(next_surface),) in rows:
                    perf_piece = True
            if perf_piece == True:
                perf_number += 1
        cursor.execute('INSERT INTO quintuple VALUES (?, ?)', (row[0], perf_number))
        counter += 1
        if (counter % 10000) == 0:
            print(counter)

def generate_web(cursor, start):
    check_list = [start]
    check_list_new = []
    counter = 0
    ply = 0
    cursor.execute('BEGIN TRANSACTION')
    while True:
        for surface in check_list.copy():
            perf_number = 0
            connections = analyze.connect_surface(surface)
            for piece in connections.keys():
                perf_piece = False
                for next_surface in connections[piece]:
                    rev_surf = list(reversed(next_surface))
                    total = 0
                    rev_total = 0
                    check = True
                    for y in range(8):
                        height = next_surface[y]
                        total += height
                        rev_total += rev_surf[y]
                        if (y != 7 and height > 4) or (y != 0 and height < -4) or abs(height) > 7 or abs(total) > 7 or abs(rev_total) > 7:
                            check = False
                    if check == True:
                        if analyze.check_perfect(analyze.connect_surface(next_surface)):
                            perf_piece = True
                            try:
                                cursor.execute('INSERT INTO single VALUES (?, ?)', (str(next_surface), 0))
                                check_list_new.append(next_surface)
                            except sqlite3.IntegrityError: pass
                if perf_piece == True:
                    perf_number += 1
            cursor.execute('UPDATE single SET number = ? WHERE surface = ?', (perf_number, str(surface)))
        conn.commit()
        print(len(check_list_new))
        check_list = check_list_new.copy()
        check_list_new = []
        ply += 1
        print(ply)
        if check_list == []: break

def generate_all(cursor, height):
    surface = [0, 0, 0, 0, 0, 0, 0, 0]
    surface[0] = surface[1] = surface[2] = surface[3] = surface[4] = surface[5] = surface[6] = surface[7] = -height
    finished = False

    while not finished:
        if abs(sum(surface)) <= 20:
            create_entry(cursor, surface)
        surface[0] += 1
        if surface[0] > height:
            surface[0] = -height
            surface[1] += 1
        if surface[1] > height:
            surface[1] = -height
            surface[2] += 1
        if surface[2] > height:
            surface[2] = -height
            surface[3] += 1
        if surface[3] > height:
            surface[3] = -height
            surface[4] += 1
        if surface[4] > height:
            surface[4] = -height
            surface[5] += 1
        if surface[5] > height:
            surface[5] = -height
            surface[6] += 1
        if surface[6] > height:
            surface[6] = -height
            surface[7] += 1
        if surface[7] > height:
            finished = True

def create_table(target):
    conn = sqlite3.connect(target)
    c = conn.cursor()
    c.execute(
    'CREATE TABLE quintuple ('
    'surface TEXT,'
    'number INTEGER,'
    'PRIMARY KEY (surface))'
    )
target = 'perf_db.sqlite'
create_table(target)
conn = sqlite3.connect(target)
c = conn.cursor()
c.execute('SELECT surface FROM quadruple WHERE number = 7')
generate_next_perfects(c)
conn.commit()
conn.close()
