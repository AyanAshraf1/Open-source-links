from tkinter import *
from tkinter import messagebox, colorchooser
import random

user = ["", "#00FF00"]
food_color = ["", "#FF0000"]

class SnakeGame:
    def __init__(self):
        global user, food_color
        self.window = Tk()
        self.window.title("Snake Game")
        #self.window.iconbitmap('snake.ico')
        self.window.attributes('-fullscreen', True)
        self.SPEED = 100
        self.SPACE_SIZE = 50
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = user[1]
        self.FOOD_COLOR = food_color[1]
        self.BACKGROUND_COLOR = "#000000"
        self.score = 0
        self.direction = 'down'
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.canvas = Canvas(self.window, bg=self.BACKGROUND_COLOR, width=self.screen_width, height=self.screen_height, highlightthickness=0)
        self.canvas.pack()
        self.initialize_game()

    def initialize_game(self):
        self.score_text = self.canvas.create_text(50, 30, text=f"Score: {self.score}", fill="white", font=('Arial', 24), anchor="w")
        self.snake = Snake(self)
        self.food = Food(self)
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))
        self.window.bind('<Escape>', self.toggle_fullscreen)
        self.next_turn()

    def toggle_fullscreen(self, event=None):
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))

    def next_turn(self):
        head_x, head_y = self.snake.coordinates[0]
        if self.direction == "up":
            head_y -= self.SPACE_SIZE
        elif self.direction == "down":
            head_y += self.SPACE_SIZE
        elif self.direction == "left":
            head_x -= self.SPACE_SIZE
        elif self.direction == "right":
            head_x += self.SPACE_SIZE
        self.snake.coordinates.insert(0, (head_x, head_y))
        square = self.canvas.create_rectangle(head_x, head_y, head_x + self.SPACE_SIZE, head_y + self.SPACE_SIZE, fill=self.SNAKE_COLOR, outline="")
        self.snake.squares.insert(0, square)
        food_x, food_y = self.food.coordinates
        if abs(head_x - food_x) < self.SPACE_SIZE and abs(head_y - food_y) < self.SPACE_SIZE:
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food.spawn()
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]
        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(self.SPEED, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        head_x, head_y = self.snake.coordinates[0]
        if head_x < 0 or head_x >= self.screen_width or head_y < 0 or head_y >= self.screen_height:
            return True
        for body_part in self.snake.coordinates[1:]:
            if head_x == body_part[0] and head_y == body_part[1]:
                return True
        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.screen_width/2, self.screen_height/2 - 50, text="GAME OVER", fill="red", font=('Arial', 70, 'bold'))
        self.canvas.create_text(self.screen_width/2, self.screen_height/2 + 50, text=f"Final Score: {self.score}", fill="white", font=('Arial', 36))
        self.canvas.create_text(self.screen_width/2, self.screen_height/2 + 150, text="Press R to Restart", fill="white", font=('Arial', 24))
        self.window.bind('<r>', lambda event: self.restart_game())
        self.window.bind('<R>', lambda event: self.restart_game())

    def restart_game(self):
        self.canvas.delete(ALL)
        self.score = 0
        self.direction = 'down'
        self.initialize_game()

class Snake:
    def __init__(self, game):
        self.game = game
        self.body_size = game.BODY_PARTS
        self.coordinates = []
        self.squares = []
        start_x = game.screen_width // 2
        start_y = game.screen_height // 2
        for i in range(self.body_size):
            self.coordinates.append([start_x - (i * game.SPACE_SIZE), start_y])
        for x, y in self.coordinates:
            square = game.canvas.create_rectangle(x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE, fill=game.SNAKE_COLOR, outline="", tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, game):
        self.game = game
        self.spawn()

    def spawn(self):
        x = random.randint(0, (self.game.screen_width // self.game.SPACE_SIZE) - 1) * self.game.SPACE_SIZE
        y = random.randint(0, (self.game.screen_height // self.game.SPACE_SIZE) - 1) * self.game.SPACE_SIZE
        self.coordinates = [x, y]
        self.game.canvas.create_oval(x, y, x + self.game.SPACE_SIZE, y + self.game.SPACE_SIZE, fill=self.game.FOOD_COLOR, outline="", tag="food")

def game_start():
    game = SnakeGame()
    game.window.mainloop()

def custom_color():
    global user
    customize.destroy()
    user = colorchooser.askcolor()

def custom_food():
    global food_color
    customize.destroy()
    food_color = colorchooser.askcolor()

def custom_snake():
    global customize
    customize = Tk()
    customize.geometry("800x600")
    customize.title("Customization Tab")
    customize.config(bg="#00ff00")
    Label(customize, text="Customization Tab", font=("Impact", 38), bg="#00ff00").pack(pady=20)
    snake_color_button = Button(customize, text="Snake color", font=("Impact", 35), command=custom_color, bg="black", fg="#00ff00", activebackground="black", activeforeground="#00ff00")
    snake_color_button.pack(pady=20)
    snake_color_button.bind("<Enter>", lambda e: snake_color_button.config(font=("Impact", 40)))
    snake_color_button.bind("<Leave>", lambda e: snake_color_button.config(font=("Impact", 35)))
    food_color_button = Button(customize, text="Food color", font=("Impact", 35), command=custom_food, bg="black", fg="#00ff00", activebackground="black", activeforeground="#00ff00")
    food_color_button.pack(pady=20)
    food_color_button.bind("<Enter>", lambda e: food_color_button.config(font=("Impact", 40)))
    food_color_button.bind("<Leave>", lambda e: food_color_button.config(font=("Impact", 35)))
    customize.mainloop()

def create_main_menu():
    global mainmenu
    mainmenu = Tk()
    mainmenu.title("Main Menu")
    mainmenu.config(bg="black")
    mainmenu.geometry("1300x600")
    welcome_label = Label(mainmenu, text="Welcome to Snake Game", font=("Impact", 40), bg="black", fg="#00ff00")
    welcome_label.pack(pady=20)
    author_label = Label(mainmenu, text="by Ayan Ashraf", font=("Impact", 25), bg="black", fg="#00ff00")
    author_label.pack(pady=10)
    play_button = Button(mainmenu, text="Play", command=game_start, font=("Impact", 38), bg="black", fg="#00ff00", activebackground="black", activeforeground="#00ff00")
    play_button.pack(pady=20)
    play_button.bind("<Enter>", lambda e: play_button.config(font=("Impact", 40)))
    play_button.bind("<Leave>", lambda e: play_button.config(font=("Impact", 38)))
    customize_button = Button(mainmenu, text="Customize", command=custom_snake, font=("Impact", 38), bg="black", fg="#00ff00", activebackground="black", activeforeground="#00ff00")
    customize_button.pack(pady=20)
    customize_button.bind("<Enter>", lambda e: customize_button.config(font=("Impact", 40)))
    customize_button.bind("<Leave>", lambda e: customize_button.config(font=("Impact", 38)))
    mainmenu.mainloop()

create_main_menu()
