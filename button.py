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
