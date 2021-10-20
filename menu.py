from button import Button

class Menu:
    def __init__(self, app):
        self.visible = True
        self.app = app
        self.root = app.root
        self.canvas = app.canvas
        self.bg = app.game.config["sections"]["colours"]["background"]
        self.button = Button(self.app.WIDTH/2-150, self.app.HEIGHT/2-100, 300, 200, "Play", self.play_game, self.app, bg=self.bg)
   
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
            self.app.start_game()
            self.visible = False
