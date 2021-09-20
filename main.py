import tkinter as tk
import time, math
import random
import colorsys

root = None
canvas = None
nodes = []

width = 500
height = 500

counters_per_player = 4
counters = 2 * counters_per_player

moving_counters = []

offset = math.pi / 4 + (math.pi * 2 / counters) + math.pi / 8

outer_radius = 70
center_radius = 100
outer_distance = 150

TWO_PI = math.pi * 2

node_selected = False
selected_node = None

player = 1

class MovingNode:
    def __init__(self, from_node, to_node, player):
        self.from_node = from_node
        self.to_node = to_node
        self.speed = 10
        self.player = player
        
        self.r = from_node.r

        self.distance_x = to_node.x - from_node.x
        self.distance_y = to_node.y - from_node.y
        self.distance_r = to_node.r - from_node.r

        self.x = from_node.x
        self.y = from_node.y

        self.from_node.player = None

        if(player == 1):
            self.colour = "white"
        else:
            self.colour = "black"
    
    def update(self):
        global node_selected
        self.distance = math.sqrt((self.to_node.x - self.x) ** 2 + (self.to_node.y - self.y) ** 2)

        if(self.distance > 1):
            self.x += self.distance_x / self.speed
            self.y += self.distance_y / self.speed
            self.r += self.distance_r / self.speed
        else:
            self.to_node.player = self.player
            moving_counters.pop(moving_counters.index(self))
            node_selected = False
            change_player()

    def draw(self):
        canvas.create_oval(self.x - self.r / 2, self.y - self.r / 2, self.x + self.r / 2, self.y + self.r / 2, fill=self.colour)


class Node:
    def __init__(self, x, y, r, player=None):
        self.x = x
        self.y = y
        self.r = r
        self.player = player

        self.outline_colour = { #HSV
            "h": 0,
            "s": 73,
            "v": 96
        }

        self.highlighted = False


        
        self.outline = "black"

    def draw(self):
        #raw = self.outline_colour
        #rgb = colorsys.hsv_to_rgb(raw["h"]/359,raw["s"]/100,raw["v"]/100)
        #outline_rgb = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        #outline = rgb_to_hex(outline_rgb)
        
        
        if(self.player == 1):
            self.colour = "white"
        elif(self.player == 2):
            self.colour = "black"
        else:
            self.colour = "#515151"

        #colour = f"#{outline}"

        if(self.highlighted == True):
            self.outline = "yellow"
        else:
            self.outline = "black"

        canvas.create_oval(self.x - self.r/2, self.y - self.r/2, self.x+self.r - self.r/2, self.y+self.r-self.r/2, fill=self.colour, outline=self.outline, width=2)
        
        self.outline_colour["h"] += 3
        if(self.outline_colour["h"] > 359):
            self.outline_colour["h"] = 0

    def click(self):
        global node_selected, selected_node

        if(self.highlighted):
            if(node_selected):
                self.player = selected_node.player
                selected_node.player = None
                node_selected = False
                selected_node = None
                change_player()
            else:
                node_selected = True
                selected_node = self
                move_counter(self, find_available_move(self))

def init():
    global canvas, root, nodes
    root = tk.Tk()
    canvas = tk.Canvas(root, bg="white", height=height, width=width)
    
    canvas.bind("<Button-1>", mouseClicked)

    counters = counters_per_player * 2
    nodes.append(Node(width/2, height/2, center_radius))

    for i in range(counters):
        angle = ((TWO_PI) / counters) * i + offset

        dx = math.cos(angle) * outer_distance
        dy = math.sin(angle) * outer_distance

        if(i >= counters_per_player):
            player = 1
        else:
            player = 2

        nodes.append(Node(width/2 + dx, height/2 + dy, outer_radius, player))

    canvas.pack()

def draw():
    global node_selected, selected_node

    canvas.delete("all")

    i = 1
    angle = 360 / counters
    while i < len(nodes):
        node = nodes[i]
        canvas.create_arc(width/2-outer_distance, height/2-outer_distance, width/2+outer_distance,height/2+outer_distance, style=tk.ARC, start=angle*i+offset+360/outer_radius, extent=angle+360/(outer_radius*2))
        canvas.create_line(node.x, node.y, nodes[0].x, nodes[0].y)       
        i += 1

    if(not node_selected):
        highlight_moveable_nodes()

    for node in nodes:
        node.draw()

    for node in moving_counters:
        node.update()
        node.draw()

    root.update()

def move_counter(from_node, to_node):
    moving_counters.append(MovingNode(from_node, to_node, from_node.player))

def change_player():
    global player

    if(player == 1):
        player = 2
    else:
        player = 1

def highlight_moveable_nodes():
    unhighlight_nodes()
    for node in nodes:
        if(node.player == player and can_move(nodes.index(node))):
                node.highlighted = True

def can_move(i):
    node = nodes[i]
    neighbours = get_outer_neighbours(i)
    
    prevNode = neighbours["prev"]
    nextNode = neighbours["next"]   
    center = nodes[0]

    if(node.player == None or node.player != player):
        return False

    if(i == 0): #Is the center node
        return True

    if(prevNode.player != node.player or nextNode.player != node.player): #isn't locked
        if(prevNode.player == None or nextNode.player == None or center.player == None):
            return True
    else:
        return False

def unhighlight_nodes():
    for node in nodes:
        node.highlighted = False


def find_available_move(selected):
    for node in nodes:
        if(node != selected):
            if(node.player == None):
                return node
    #i = nodes.index(selected)
    #neighbours = get_outer_neighbours(i)
    
    #prev_node = neighbours["prev"]
    #next_node = neighbours["next"]
    #center = nodes[0]

    #unhighlight_nodes()

    #if(not can_move(i)):
    #    return

    #if(prev_node.player == None):
    #    prev_node.highlighted = True
    #if(next_node.player == None):
    #    next_node.highlighted = True
    #if(center.player == None):
    #    center.highlighted = True

    #if(i == 0):
    #    for node in nodes:
    #        if(node.player == None):
    #            node.highlighted = True

def get_outer_neighbours(i):
    if(i == 1):
        prevNode = nodes[-1]
    else:
        prevNode = nodes[i-1]
        
    if(i == len(nodes) - 1):
        nextNode = nodes[1]
    else:
        nextNode = nodes[i+1]

    return {"prev": prevNode, "next": nextNode}

def mouseClicked(event):
    global mouse_down

    mouse_down = True
    for node in nodes:
        distance = dist(event.x, event.y, node.x, node.y)
        if(dist(event.x, event.y, node.x, node.y) < node.r/2):
            node.click()


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def dist(x1, y1, x2, y2):
    xlen = x2 - x1
    ylen = y2 - y1

    return math.sqrt(xlen**2 + ylen**2)

if __name__ == "__main__":
    init()
    draw()
    while True:
        time.sleep(1/50)
        draw()


