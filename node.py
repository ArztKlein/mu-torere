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
            if(self.game.node_selected):
                self.player = game.selected_node.player
                self.game.selected_node.player = None
                self.game.node_selected = False
                self.game.selected_node = None
                self.game.swap_player()
            else:
                self.game.node_selected = True
                self.game.selected_node = self
                self.game.move_counter(self, self.game.find_available_move(self))
