import tkinter as tk
import time, math
import axiompy

WIDTH = 500
HEIGHT = 500

counters_per_player = 4
counters = 2 * counters_per_player

TWO_PI = math.pi * 2


class Game:
    def __init__(self, app, config):
        self.outer_radius = config["sections"]["sizes"]["outer_radius"]
        self.center_radius = config["sections"]["sizes"]["center_radius"]
        self.outer_distance = config["sections"]["sizes"]["outer_distance"]

        self.app = app
        self.root = app.root
        self.canvas = app.canvas
        self.config = config

        self.setup()

    def setup(self):
        self.x = WIDTH
        self.y = HEIGHT
        self.scale = 3
        self.transition = False

        self.watch = False

        self.nodes = []
        self.moving_counters = []
        self.game_running = False
        self.game_finished = False
        self.visible = False

        counters = counters_per_player * 2
        self.nodes.append(Node(WIDTH/2, HEIGHT/2, self.center_radius, self))

        self.node_selected = False
        self.selected_node = None

        self.transition_speed = self.config["sections"]["animation_speeds"]["speed"]

        self.bg = self.config["sections"]["colours"]["background"]
        self.replay_button = Button(100, HEIGHT - 100, 150, 80, "Retry", self.restart, self.app, bg=self.bg)
        self.watch_button = Button(300, HEIGHT - 100, 150, 80, "Replay", self.watch_replay, self.app, bg=self.bg)
        self.player = 1
        for i in range(counters):
            angle = ((TWO_PI) / counters) * i

            dx = math.cos(angle) * self.outer_distance
            dy = math.sin(angle) * self.outer_distance

            if(i >= counters_per_player):
                player = 1
            else:
               player = 2

            self.nodes.append(Node(WIDTH/2 + dx, HEIGHT/2 + dy, self.outer_radius, self, player))

    def draw(self):
        if(not self.visible):
            return

        if(self.transition):
            self.transition_show()

        center_x = WIDTH / 2 + self.x
        center_y = HEIGHT / 2 + self.y

        x = self.x - self.outer_distance + WIDTH/2 
        y = self.y - self.outer_distance + HEIGHT/2
        self.canvas.create_oval(x, y, x + self.outer_distance * 2, y + self.outer_distance * 2)
       
        for node in self.nodes:
            self.canvas.create_line(center_x, center_y, node.x, node.y)
        
        for node in self.nodes:
            node.draw()

        if self.game_running:
            if(not self.node_selected):
                self.highlight_moveable_nodes()
            else:
                self.unhighlight_nodes()
        
            for node in self.moving_counters:
                node.update()
                node.draw()
        elif(self.game_finished):
            self.canvas.create_text(WIDTH/2, 30, fill="black", font="Times 40 italic bold", text=f"{'White' if self.player == 1 else 'Black'} wins!")
            self.replay_button.draw()
            self.watch_button.draw()
    
    def watch_replay(self):
        print("Watching Replay")


    def restart(self):
        self.setup()
        self.start()

    def start(self):
        self.transition = True
        self.visible = True
        self.canvas.bind("<Button-1>", self.mouse_clicked)
        self.replay_button.visible = False

    def get_outer_neighbours(self,i):
        if(i == 1):
            prevNode = self.nodes[-1]
        else:
            prevNode = self.nodes[i-1]
        
        if(i == len(self.nodes) - 1):
            nextNode = self.nodes[1]
        else:
            nextNode = self.nodes[i+1]

        return {"prev": prevNode, "next": nextNode}


    def unhighlight_nodes(self):
        for node in self.nodes:
            node.highlighted = False

    def highlight_moveable_nodes(self):
        self.unhighlight_nodes()

        moves = 0
        for node in self.nodes:
            if(node.player == self.player and self.can_move(self.nodes.index(node))):
                    node.highlighted = True
                    moves += 1

        if(moves == 0):
            self.end_game()

    def can_move(self,i):

        if(len(self.moving_counters) != 0):
            return False

        node = self.nodes[i]
        neighbours = self.get_outer_neighbours(i)

        prevNode = neighbours["prev"]
        nextNode = neighbours["next"]   
        center = self.nodes[0]

        if(node.player == None or node.player != self.player):
            return False

        if(i == 0): #Is the center node
            return True

        if(prevNode.player != node.player or nextNode.player != node.player): #isn't locked
            if(prevNode.player == None or nextNode.player == None or center.player == None):
                return True
        else:
            return False


    def mouse_clicked(self, event):
        global mouse_down
        for node in self.nodes:
            distance = dist(event.x, event.y, node.x, node.y)
            if(dist(event.x, event.y, node.x, node.y) < node.d/2):
                node.click()
        self.replay_button.check_clicked(event)


    def find_available_move(self, selected):
        for node in self.nodes:
            if(node != selected):
                if(node.player == None):
                    return node

    def move_counter(self, from_node, to_node):
        self.moving_counters.append(MovingNode(from_node, to_node, from_node.player, self))

    def swap_player(self):
        if(self.player == 1):
            self.player = 2
        else:
            self.player = 1


    def end_game(self):
        self.swap_player()
        self.game_running = False
        self.game_finished = True
        self.replay_button.visible = True

    def transition_show(self):
        self.x -= WIDTH / self.transition_speed
        self.y -= HEIGHT / self.transition_speed
        self.scale -= 0.1
        if(self.x < 0 or self.y < 0):
            self.x = 0
            self.y = 0
            self.transition = False
            self.game_running = True
        if(self.scale <= 1):
            self.scale = 1

class MovingNode:
    def __init__(self, from_node, to_node, player, game):
        self.from_node = from_node
        self.to_node = to_node
        self.speed = game.config["sections"]["animation_speeds"]["counter_speed"]
        self.player = player
        self.game = game
        
        self.r = from_node.d

        self.distance_x = to_node.x - from_node.x
        self.distance_y = to_node.y - from_node.y
        self.distance_r = to_node.d - from_node.d

        self.x = from_node.x + self.game.x
        self.y = from_node.y + self.game.y

        self.from_node.player = None

        if(player == 1):
            self.colour = game.config["sections"]["colours"]["playerone"]
        else:
            self.colour = game.config["sections"]["colours"]["playertwo"]
    
    def update(self):
        global node_selected
        self.distance = dist(self.to_node.x, self.to_node.y, self.x, self.y)

        if(self.distance > 1):
            self.x += self.distance_x / self.speed
            self.y += self.distance_y / self.speed
            self.r += self.distance_r / self.speed
        else:
            self.to_node.player = self.player
            self.game.moving_counters.pop(self.game.moving_counters.index(self))
            game.node_selected = False
            game.swap_player()

    def draw(self):
        self.game.canvas.create_oval(self.x - self.r / 2, self.y - self.r / 2, self.x + self.r / 2, self.y + self.r / 2, fill=self.colour)


class Node:
    def __init__(self, x, y, d, game, player=None):
        self.x = x + game.x
        self.y = y + game.y
        self.raw_x = x
        self.raw_y = y
        self.raw_d = d
        self.d = d
        self.player = player
        self.game = game

        self.highlighted = False
        self.outline = self.game.config["sections"]["colours"]["outline"]

    def draw(self):
        self.d = self.raw_d * self.game.scale
        self.x = self.raw_x + self.game.x
        self.y = self.raw_y + self.game.y
        
        if(self.player == 1):
            self.colour = self.game.config["sections"]["colours"]["playerone"]
        elif(self.player == 2):
            self.colour = self.game.config["sections"]["colours"]["playertwo"]
        else:
            self.colour = self.game.config["sections"]["colours"]["empty"]

        if(self.highlighted == True):
            self.outline = self.game.config["sections"]["colours"]["highlight"]
        else:
            self.outline = self.game.config["sections"]["colours"]["outline"]

        self.game.canvas.create_oval(self.x - self.d/2, self.y - self.d/2, self.x+self.d - self.d/2, self.y+self.d-self.d/2, fill=self.colour, outline=self.outline, width=2)
        
    def click(self):
        if(self.highlighted):
            if(game.node_selected):
                self.player = game.selected_node.player
                game.selected_node.player = None
                game.node_selected = False
                game.selected_node = None
                game.swap_player()
            else:
                game.node_selected = True
                game.selected_node = self
                game.move_counter(self, game.find_available_move(self))

class Button:
    def __init__(self, x, y, width, height, text, callback, app, bg="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.root = app.root
        self.canvas = app.canvas
        self.font_size = 40
        self.scale = 1
        self.visible = True
        self.bg = bg

    def draw(self):
        if(self.visible):
            new_x = self.x * self.scale
            new_y = self.y * self.scale

            x_end = new_x + self.width * self.scale
            y_end = new_y + self.height * self.scale

            font = f"Times {max(int(self.scale * self.font_size), 0)} italic bold"
            font_x = new_x + (self.width * self.scale) / 2
            font_y = new_y + (self.height * self.scale) / 2
            self.canvas.create_rectangle(new_x, new_y, x_end, y_end, fill=self.bg)
            self.canvas.create_text(font_x, font_y, fill="black", font=font,text=self.text)

            if(new_x + self.width * self.scale < 0):
                self.callback()
    def check_clicked(self, event):
        if(self.visible):
            x = event.x
            y = event.y

            if(x < self.x + self.width and x > self.x):
                if(y < self.y + self.height and y > self.y):
                    self.callback()

class Menu:
    def __init__(self, app):
        self.visible = True
        self.app = app
        self.root = app.root
        self.canvas = app.canvas
        self.bg = app.game.config["sections"]["colours"]["background"]
        self.button = Button(WIDTH/2-150, HEIGHT/2-100, 300, 200, "Play", self.play_game, self.app, bg=self.bg)
   
        self.time = 0
        self.moving = False
        self.canvas.bind("<Button-1>", self.mouse_clicked)
    def draw(self):
        if(not self.visible):
            return
        
        if(self.moving):
            self.time += 0.001
            self.button.x -= 2000 * self.time
            self.button.scale -= 2 * self.time
        self.button.draw()

    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False

    def mouse_clicked(self, event):
        if(self.visible):
            self.button.check_clicked(event)

    def play_game(self):
        if(not self.moving):
            self.moving = True
        else:
            start_game()
            self.visible = False


class App:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, bg="white", height=HEIGHT, width=WIDTH)
        self.canvas.pack()
        self.canvas.configure(bg=config["sections"]["colours"]["background"])
    def update(self):
        self.canvas.update()
    def clear(self):
        self.canvas.delete("all")


def init():
    global game, menu, app
    
    config_lines = axiompy.fileutils.FileUtils.read_lines("config.acf")
    config = axiompy.ACF(config_lines)

    test_config(config.data)

    app = App(config.data)
    game = Game(app, config.data)
    app.game = game
    menu = Menu(app)

def test_config(config):
    #Test speeds
    for speed in config["sections"]["animation_speeds"]:
        if(0 > config["sections"]["animation_speeds"][speed]):
            raise Exception(f"Animation Speed '{speed}' must be above 0.")
    for size in config["sections"]["sizes"]:
        if(0 > config["sections"]["sizes"][size]):
            raise Exception(f"Size '{size}' must be above 0.")

def draw():
    app.clear()
    game.draw()
    menu.draw()
    app.update()


def start_game():
    menu.hide()
    game.start()

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
