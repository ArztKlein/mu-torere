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

        self.x = 0
        self.y = 0
        self.scale = 1
    def draw(self):
        if(not self.visible):
            return
        
        if(self.moving):
            self.time += 0.001
            self.x -= 2000 * self.time
            self.scale -= 2 * self.time

            self.button.x -= 2000 * self.time
            self.button.scale -= 2 * self.time
        self.button.draw()
        self.canvas.create_text(self.x + self.app.WIDTH/2, 50, fill="black", font=f"Times {int(25 * self.scale)} italic", text=f"Edit the config.acf file to \n configure the game.")

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
