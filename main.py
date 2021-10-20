import tkinter as tk
import time
import axiompy

from app import App
from game import Game
from menu import Menu

def init():
    global game, menu, app
    
    config_lines = axiompy.fileutils.FileUtils.read_lines("config.acf")
    config = axiompy.ACF(config_lines)

    test_config(config.data)

    app = App(config.data)

def test_config(config):
    #Test whether the speeds are valid (more than 0)
    for speed in config["sections"]["animation_speeds"]:
        if(0 > config["sections"]["animation_speeds"][speed]):
            raise Exception(f"Animation Speed '{speed}' must be above 0.")
    #Test whether the sizes are valid (more than 0)
    for size in config["sections"]["sizes"]:
        if(0 > config["sections"]["sizes"][size]):
            raise Exception(f"Size '{size}' must be above 0.")

def draw():
    app.update()

if __name__ == "__main__":
    init()
    draw()
    while True:
        time.sleep(1/50)
        draw()
