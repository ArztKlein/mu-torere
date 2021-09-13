import tkinter as tk
import time, math

root = None
canvas = None
nodes = []


width = 500
height = 500

counters_per_player = 4

outer_radius = 70
center_radius = 100
outer_distance = 150

class Node:
    def __init__(self, x, y, r, player=None):
        self.x = x
        self.y = y
        self.r = r

        if(player == 1):
            self.colour = "white"
        elif(player == 2):
            self.colour = "black"
        else:
            self.colour = "#515151"

    def draw(self):
        canvas.create_oval(self.x - self.r/2, self.y - self.r/2, self.x+self.r - self.r/2, self.y+self.r-self.r/2, fill=self.colour, outline="black")

def init():
    global canvas, root, nodes
    root = tk.Tk()
    canvas = tk.Canvas(root, bg="white", height=height, width=width)
    
    counters = counters_per_player * 2
    nodes.append(Node(width/2, height/2, center_radius))

    offset = math.pi / 4 + (math.pi * 2 / counters) + math.pi / 8
    for i in range(counters):
        angle = ((math.pi * 2) / counters) * i + offset

        dx = math.cos(angle) * outer_distance
        dy = math.sin(angle) * outer_distance

        if(i >= counters_per_player):
            player = 1
        else:
            player = 2

        nodes.append(Node(width/2 + dx, height/2 + dy, outer_radius, player))

def draw():
    for node in nodes:
        node.draw()

    canvas.pack()

if __name__ == "__main__":
    init()
    draw()
    root.mainloop()
    #while True:
    #    time.sleep(0.5)
    #    draw()


