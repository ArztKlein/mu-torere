import tkinter as tk
from game import Game
from menu import Menu

class App:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.WIDTH = config["sections"]["app"]["width"]
        self.HEIGHT = config["sections"]["app"]["height"]
        self.canvas = tk.Canvas(self.root, bg="white", width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.canvas.configure(bg=config["sections"]["colours"]["background"])

        self.game = Game(self, config)
        self.menu = Menu(self)

    def update(self):
        self.clear()
        self.game.draw()
        self.menu.draw()
        self.canvas.update()

    def clear(self):
        self.canvas.delete("all")

    def start_game(self):
        self.menu.hide()
        self.game.start()