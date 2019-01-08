import tkinter
import analyze
import sqlite3
import play
import ast

class Board(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.blocks = []
        self.bg_default = '#b1b5bc'
        self.bind('<Left>', self.left)
        self.bind('<Right>', self.right)
        for y in range(20):
            self.blocks.append([])
            for x in range(10):
                self.blocks[y].append(tkinter.Frame(self, height = 32, width = 32, bd = 2, bg = self.bg_default, relief = 'raised'))
                self.blocks[y][x].grid(row = 20 - y, column = x)
        self.results = play.play_game([-1, 0, -1, 0, 1, 0, 0, 0])
        self.surface = self.results[0]
        self.index = 0
        print(self.results)

    def clear_display(self):
        for y in range(20):
            for x in range(10):
                self.blocks[y][x].config(bg = self.bg_default)

    def display_surface(self):
        surface = self.surface
        self.clear_display()
        counter = 0
        outline = [0]
        for y in surface:
            next_height = outline[counter] + y
            outline.append(next_height)
            counter += 1
        floor = min(outline)
        for x in range(9):
            for y in range(0, outline[x] - floor):
                self.blocks[y][x].config(bg = 'green')

    def right(self, event):
        self.index += 1
        self.surface = self.results[self.index]
        self.display_surface()
        print(self.results[self.index])

    def left(self, event):
        self.index -= 1
        self.surface = self.results[self.index]
        self.display_surface()
        print(self.results[self.index])

    def extract_list(self, table, interval):
        target = 'perf_db.sqlite'
        conn = sqlite3.connect(target)
        c = conn.cursor()
        c.execute('SELECT surface FROM {} WHERE number <= ? AND number >= ?'.format(table), (interval[1], interval[0]))
        results = c.fetchall()
        result_list = [ast.literal_eval(result[0]) for result in results]
        conn.close()
        return result_list

root = tkinter.Tk()
board = Board(root)
board.focus_set()
board.pack()
board.display_surface()
#print(analyze.test_surface(surface))
root.mainloop()
