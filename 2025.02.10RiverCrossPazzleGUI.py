import os 
os.system("clear")
print("Welcome to the River Crossing Puzzle")


class RiverCrossingGame:
    def __init__(self):
        # Initial positions: 'beach' or 'island'
        self.player = 'beach'
        self.boat = 'beach'
        self.goat = 'beach'
        self.lion = 'beach'
        self.grass = 'beach'

    def state(self):
        return f"Player: {self.player}, Boat: {self.boat}, Goat: {self.goat}, Lion: {self.lion}, Grass: {self.grass}"

    def is_game_won(self):
        """Check if all items have safely reached the island."""
        return self.goat == self.lion == self.grass == 'island'

    def is_game_lost(self):
        """Check if the game is lost due to unsafe conditions."""
        if self.goat == self.lion and self.player != self.goat:
            return "Game Over! The lion ate the goat!"
        if self.goat == self.grass and self.player != self.goat:
            return "Game Over! The goat ate the grass!"
        return False

    def move(self, item=None):
        """Move the player and optionally an item to the other side."""
        if self.player == 'beach':
            new_location = 'island'
        else:
            new_location = 'beach'

        # Move the player and the boat
        self.player = new_location
        self.boat = new_location

        # Move the item if it's in the boat
        if item and getattr(self, item) == self.boat:
            setattr(self, item, new_location)

        # Check for losing conditions
        lost = self.is_game_lost()
        if lost:
            print(lost)
            return False

        # Check for win condition
        if self.is_game_won():
            print("Congratulations! You won the game!")
            return True

        return True  # Game is still ongoing

# Example of using the game logic
game = RiverCrossingGame()
print(game.state())  # Initial state

game.move('goat')  # Move goat to island
print(game.state())

game.move()  # Player goes back alone
print(game.state())

game.move('lion')  # Move lion to island
print(game.state())

game.move('goat')  # Bring goat back
print(game.state())

game.move('grass')  # Move grass to island
print(game.state())

game.move()  # Player returns alone
print(game.state())

game.move('goat')  # Finally move goat to island
print(game.state())

import tkinter as tk
from tkinter import messagebox

class RiverCrossingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("River Crossing Game")

        self.canvas = tk.Canvas(root, width=600, height=300, bg="lightblue")
        self.canvas.pack()

        # Draw static elements
        self.canvas.create_rectangle(20, 100, 120, 200, fill="tan", tags="beach")  # Beach
        self.canvas.create_rectangle(480, 100, 580, 200, fill="tan", tags="island")  # Island
        self.canvas.create_oval(260, 180, 340, 220, fill="brown", tags="boat")  # Boat
        
        self.items = {"goat": "black", "lion": "orange", "grass": "green"}
        self.positions = {"goat": (50, 150), "lion": (50, 120), "grass": (50, 180)}
        
        for item, color in self.items.items():
            x, y = self.positions[item]
            self.canvas.create_oval(x, y, x+30, y+30, fill=color, tags=item)
            
        self.message_label = tk.Label(root, text="Double-click to move items", font=("Arial", 12))
        self.message_label.pack()
        
        self.canvas.tag_bind("goat", "<Double-Button-1>", lambda e: self.load_unload("goat"))
        self.canvas.tag_bind("lion", "<Double-Button-1>", lambda e: self.load_unload("lion"))
        self.canvas.tag_bind("grass", "<Double-Button-1>", lambda e: self.load_unload("grass"))
        self.canvas.tag_bind("boat", "<Double-Button-1>", lambda e: self.cross_river())

        self.boat_cargo = None
        self.boat_position = "beach"
        self.left_bank = ["goat", "lion", "grass"]
        self.right_bank = []
        self.valid_moves = ["goat", None, "grass", "goat", "lion", None, "goat"]
        self.move_index = 0

    def load_unload(self, item):
        if self.move_index >= len(self.valid_moves):
            return
        
        expected_item = self.valid_moves[self.move_index]
        
        if self.boat_cargo is None:  # Load item
            if expected_item == item and ((self.boat_position == "beach" and item in self.left_bank) or (self.boat_position == "island" and item in self.right_bank)):
                self.boat_cargo = item
                self.canvas.move(item, 210, 30)  # Move onto the boat
        elif self.boat_cargo == item:  # Unload item
            if self.boat_position == "island":
                self.right_bank.append(self.boat_cargo)
                self.left_bank.remove(self.boat_cargo)
                self.canvas.move(self.boat_cargo, 210, -30)
            else:
                self.left_bank.append(self.boat_cargo)
                self.right_bank.remove(self.boat_cargo)
                self.canvas.move(self.boat_cargo, -210, -30)
            self.boat_cargo = None
            self.move_index += 1
            self.check_game_over()
    
    def cross_river(self):
        if self.move_index >= len(self.valid_moves):
            return
        
        move_distance = 280 if self.boat_position == "beach" else -280
        self.boat_position = "island" if self.boat_position == "beach" else "beach"
        self.canvas.move("boat", move_distance, 0)
        if self.boat_cargo:
            self.canvas.move(self.boat_cargo, move_distance, 0)
        self.move_index += 1
        self.check_game_over()

    def check_game_over(self):
        if ("goat" in self.left_bank and "lion" in self.left_bank and self.boat_position == "beach") or \
           ("goat" in self.right_bank and "lion" in self.right_bank and self.boat_position == "island"):
            self.message_label.config(text="Game Over: The lion ate the goat!")
        elif ("goat" in self.left_bank and "grass" in self.left_bank and self.boat_position == "beach") or \
             ("goat" in self.right_bank and "grass" in self.right_bank and self.boat_position == "island"):
            self.message_label.config(text="Game Over: The goat ate the grass!")
        elif len(self.right_bank) == 3:
            self.message_label.config(text="Congratulations! You won the game!")
        else:
            self.message_label.config(text="Make your next move.")

root = tk.Tk()
app = RiverCrossingGUI(root)
root.mainloop()
