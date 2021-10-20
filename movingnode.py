import maths

class MovingNode:
    def __init__(self, from_node, to_node, player, game):
        self.from_node = from_node
        self.to_node = to_node
        self.game = game
        self.speed = self.game.config["sections"]["animation_speeds"]["counter_speed"]
        self.player = player
        
        self.r = from_node.d

        self.distance_x = to_node.x - from_node.x
        self.distance_y = to_node.y - from_node.y
        self.distance_r = to_node.d - from_node.d

        self.x = from_node.x + self.game.x
        self.y = from_node.y + self.game.y

        self.from_node.player = None

        if(player == 1):
            self.colour = self.game.config["sections"]["colours"]["playerone"]
        else:
            self.colour = self.game.config["sections"]["colours"]["playertwo"]
    
    def update(self):
        global node_selected
        self.distance = maths.dist(self.to_node.x, self.to_node.y, self.x, self.y)

        if(self.distance > 1):
            self.x += self.distance_x / self.speed
            self.y += self.distance_y / self.speed
            self.r += self.distance_r / self.speed
        else:
            self.to_node.player = self.player
            self.game.moving_counters.pop(self.game.moving_counters.index(self))
            self.game.node_selected = False
            self.game.swap_player()

    def draw(self):
        self.game.canvas.create_oval(self.x - self.r / 2, self.y - self.r / 2, self.x + self.r / 2, self.y + self.r / 2, fill=self.colour)
