import math, time
from button import Button
from node import Node
from movingnode import MovingNode
import maths

class Game:
    def __init__(self, app, config):
        self.OUTER_RADIUS = config["sections"]["sizes"]["outer_radius"]
        self.CENTER_RADIUS = config["sections"]["sizes"]["center_radius"]
        self.OUTER_DISTANCE = config["sections"]["sizes"]["outer_distance"]

        self.app = app
        self.root = app.root
        self.canvas = app.canvas
        self.config = config

        self.COUNTERS_PER_PLAYER = 4
        self.COUNTERS = 2 * self.COUNTERS_PER_PLAYER
        self.WIDTH = self.app.WIDTH
        self.HEIGHT = self.app.HEIGHT

        self.setup()

        

    def setup(self):
        self.x = self.WIDTH
        self.y = self.HEIGHT
        self.scale = 3
        self.transition = False

        self.nodes = []
        self.moving_counters = []
        self.game_running = False
        self.game_finished = False
        self.visible = False

        self.node_selected = False
        self.selected_node = None

        self.transition_speed = self.config["sections"]["animation_speeds"]["transition_speed"]

        self.bg = self.config["sections"]["colours"]["background"]
        self.replay_button = Button(self.WIDTH - 300, self.HEIGHT - 100, 150, 80, "Retry", self.restart, self.app, bg=self.bg)

        self.create_counters()
        
    def create_counters(self):
        self.nodes.append(Node(self.WIDTH/2, self.HEIGHT/2, self.CENTER_RADIUS, self)) # Center Counter

        self.player = 1
        for i in range(self.COUNTERS):
            angle = ((3.14 * 2) / self.COUNTERS) * i

            dx = math.cos(angle) * self.OUTER_DISTANCE
            dy = math.sin(angle) * self.OUTER_DISTANCE

            if(i >= self.COUNTERS_PER_PLAYER):
                player = 1
            else:
               player = 2

            self.nodes.append(Node(self.WIDTH/2 + dx, self.HEIGHT/2 + dy, self.OUTER_RADIUS, self, player))

    def draw(self):
        if(not self.visible):
            return

        if(self.transition):
            self.transition_show()

        center_x = self.WIDTH / 2 + self.x
        center_y = self.HEIGHT / 2 + self.y

        x = self.x - self.OUTER_DISTANCE + self.WIDTH/2 
        y = self.y - self.OUTER_DISTANCE + self.HEIGHT/2
        self.canvas.create_oval(x, y, x + self.OUTER_DISTANCE * 2, y + self.OUTER_DISTANCE * 2)
       
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
            self.canvas.create_text(self.WIDTH/2, 30, fill="black", font="Times 40 italic bold", text=f"{'White' if self.player == 1 else 'Black'} wins!")
            self.replay_button.draw()

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
            prev_node = self.nodes[-1]
        else:
            prev_node = self.nodes[i-1]
        
        if(i == len(self.nodes) - 1):
            next_node = self.nodes[1]
        else:
            next_node = self.nodes[i+1]

        return {"prev": prev_node, "next": next_node}


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

        prev_node = neighbours["prev"]
        next_node = neighbours["next"]   
        center = self.nodes[0]

        if(node.player == None or node.player != self.player):
            return False

        if(i == 0): #Is the center node
            return True

        if(prev_node.player != node.player or next_node.player != node.player): #isn't locked
            if(prev_node.player == None or next_node.player == None or center.player == None):
                return True
        else:
            return False


    def mouse_clicked(self, event):
        global mouse_down
        for node in self.nodes:
            if(maths.dist(event.x, event.y, node.x, node.y) < node.d/2):
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
        self.x -= self.WIDTH / self.transition_speed
        self.y -= self.HEIGHT / self.transition_speed
        self.scale -= 0.1
        if(self.x < 0 or self.y < 0):
            self.x = 0
            self.y = 0
            self.transition = False
            self.game_running = True
        if(self.scale <= 1):
            self.scale = 1
