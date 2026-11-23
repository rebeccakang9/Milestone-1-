#------------------------------------------------------------------------------
'''Group member names: Rebecca Kang, Yusra Nazari 
   Programming Project: Milestone#1'''
#------------------------------------------------------------------------------
import pickle

class Stack:
    """Represent one tower using a list."""

    def __init__(self):
        """
        Purpose: Initialize an empty tower

        Parameters: None

        Returns: None
        """
        self.lst = []

    def push(self, disc):
        """
        Purpose: Add a disc to the top of the tower

        Parameters:
            disc (int): The disc number being added

        Returns: None
        """
        self.lst.append(disc)

    def pop(self):
        """
        Purpose: Remove and return the top disc

        Parameters: None

        Returns:
            int: The disc removed from the tower
        """
        return self.lst.pop()

    def peek(self):
        """
        Purpose: Return the top disc without removing it

        Parameters: None

        Returns:
            int: The disc at the top of the tower
        """
        return self.lst[-1]

    def is_empty(self):
        """
        Purpose: Check whether the tower is empty

        Parameters: None

        Returns:
            bool: True if the tower is empty, otherwise False
        """
        return len(self.lst) == 0


class Game:
    """Manage the Tower of Hanoi game."""

    def __init__(self):
        """
        Purpose: Initialize the game variables

        Parameters: None

        Returns: None
        """
        self.towers = []
        self.num_discs = 0
        self.num_moves = 0

    def get_number(self, prompt, minimum, maximum):
        """
        Purpose: Get a valid integer within a given range

        Parameters:
            prompt (str): Message displayed when requesting input
            minimum (int): Lowest accepted number
            maximum (int): Highest accepted number

        Returns:
            int: A number within the specified range
        """
        while True:
            number = input(prompt)

            if number.isdigit():
                number = int(number)
                if minimum <= number <= maximum:
                    return number

            print("Invalid selection! Try again.")

    def start_menu(self):
        """
        Purpose: Display the starting menu and get a selection

        Parameters: None

        Returns:
            int: The selected menu option (1 or 2)
        """
        print("\n1 - Start a new game")
        print("2 - Resume a saved game")
        return self.get_number("Select an option: ", 1, 2)

    def start_game(self):
        """
        Purpose: Start a new game or load a saved game

        Parameters: None

        Returns:
            bool: True if a game starts successfully,
                  otherwise False
        """
        choice = self.start_menu()

        if choice == 1:
            print("Starting new game!")
            self.new_game()
            return True

        print("Resuming saved game!")
        return self.load_game()

    def game_menu(self):
        """
        Purpose: Display the game menu and get a selection

        Parameters: None

        Returns:
            int: The selected menu option (1, 2, or 3)
        """
        print("\n1 - Move a disc")
        print("2 - Save and Quit")
        print("3 - Quit")
        return self.get_number("Select an option: ", 1, 3)

    def menu(self):
        """
        Purpose: Control the main game menu and game loop

        Parameters: None

        Returns: None
        """
        if not self.start_game():
            return

        self.display_towers()

        while True:
            choice = self.game_menu()

            if choice == 1:
                if self.move_turn():
                    break
            elif choice == 2:
                self.save_game()
                break
            else:
                print("Quitting ...")
                break

    def move_turn(self):
        """
        Purpose: Ask the player to make one disc move

        Parameters: None

        Returns:
            bool: True if the player wins, otherwise False
        """
        source = input("Source Tower: ")
        destination = input("Destination Tower: ")

        if not self.move_disc(source, destination):
            return False

        self.display_towers()

        if self.check_win():
            print("\nCongratulations, you won!")
            print("You finished in", self.num_moves, "moves!")
            return True

        return False

    def new_game(self):
        """
        Purpose: Create a new game with selected towers and discs

        Parameters: None

        Returns: None
        """
        self.num_moves = 0
        self.towers = []

        tower_count = self.get_num_towers()
        self.num_discs = self.get_num_discs()

        self.new_tower(tower_count)
        self.add_disc()

    def get_num_towers(self):
        """
        Purpose: Ask the user how many towers to create

        Parameters: None

        Returns:
            int: The number of towers, between 3 and 9
        """
        return self.get_number("Number of towers (3-9): ", 3, 9)

    def get_num_discs(self):
        """
        Purpose: Ask the user how many starting discs to create

        Parameters: None

        Returns:
            int: The number of discs, between 3 and 9
        """
        return self.get_number("Number of starting discs (3-9): ", 3, 9)

    def new_tower(self, tower_count):
        """
        Purpose: Create the requested number of Stack objects

        Parameters:
            tower_count (int): Number of towers to create
                Must be between 3 and 9

        Returns: None
        """
        for x in range(tower_count):
            self.towers.append(Stack())

    def add_disc(self):
        """
        Purpose: Add all starting discs to the first tower

        Parameters: None

        Returns: None
        """
        for disc in range(self.num_discs, 0, -1):
            self.towers[0].push(disc)

    def get_tower_index(self, source, destination):
        """
        Purpose: Validate tower numbers and return their list index

        Parameters:
            source (str): Number of the source tower
            destination (str): Number of the destination tower
            
        Returns:
            tuple: The source and destination list indices if valid
            None: If either tower number is invalid
        """
        if not source.isdigit() or not destination.isdigit():
            print("Invalid tower number!")
            return None

        source = int(source)
        destination = int(destination)

        if source < 1 or source > len(self.towers):
            print("Invalid source tower!")
            return None

        if destination < 1 or destination > len(self.towers):
            print("Invalid destination tower!")
            return None

        if source == destination:
            print("Choose two different towers!")
            return None

        return source - 1, destination - 1

    def move_disc(self, source, destination):
        """
        Purpose: Move a disc if the move follows the game rules

        Parameters:
            source (str): Number of the tower to move a disc from
            destination (str): Number of the tower to move a disc to

        Returns:
            bool: True if the disc was moved successfully,
                  otherwise False
        """
        index = self.get_tower_index(source, destination)

        if index is None:
            return False

        source, destination = index

        if self.towers[source].is_empty():
            print("Source tower is empty!")
            return False

        disc = self.towers[source].peek()
        target = self.towers[destination]

        if not target.is_empty() and disc > target.peek():
            print("Cannot place a larger disc on a smaller disc!")
            return False

        self.towers[source].pop()
        target.push(disc)
        self.num_moves += 1

        print("Disc moved successfully!")
        print("Total moves:", self.num_moves)
        return True

    def display_towers(self):
        """
        Purpose: Display centered towers with labels at the bottom.
    
        Parameters: None
       
        Returns: None
        """
        width = self.num_discs * 2 + 1

        for level in range(self.num_discs - 1, -1, -1):
            for tower in self.towers:
                if level < len(tower.lst):
                    disc = tower.lst[level]
                    symbol = "*" * disc + "|" + "*" * disc
                else:
                    symbol = "|"

                print(symbol.center(width), end="  ")
            print()

        for i in range(len(self.towers)):
            label = "===" + str(i + 1) + "==="
            print(label.center(width), end="  ")
        print()

    def check_win(self):
        """
        Purpose: Check whether all discs are on another tower
    
        Parameters: None
       
        Returns:
            bool: True if all discs are on a tower other than
                  the first tower, otherwise False
        """
        for tower in self.towers[1:]:
            if len(tower.lst) == self.num_discs:
                return True

        return False

    def get_save_names(self):
        """
        Purpose: Read the names of previously saved games
        
        Parameters: None
       
        Returns:
            list: A list of saved game names
                  An empty list is returned if no save list exists
        """
        try:
            file = open("saves.txt", "r")
            content = file.readlines()
            file.close()

            saves = []
            for name in content:
                if name.strip() != "":
                    saves.append(name.strip())

            return saves

        except FileNotFoundError:
            return []

    def save_game(self):
        """
        Purpose: Save the current game using a user-selected name
       
        Parameters: None
       
        Returns: None
        """
        name = input("Enter a name for your save: ").strip()

        while (name == "" or "/" in name or "\\" in name
               or ":" in name or name in self.get_save_names()):
            print("Invalid or already existing save name!")
            name = input("Enter another name: ").strip()

        filename = name + ".dat"
        tower_data = []

        for tower in self.towers:
            tower_data.append(tower.lst)

        data = [tower_data, self.num_moves, self.num_discs]

        file = open(filename, "wb")
        pickle.dump(data, file)
        file.close()

        file = open("saves.txt", "a")
        file.write(name + "\n")
        file.close()

        print("Game saved as:", name)

    def choose_save_file(self):
        """
        Purpose: Display saved games and let the player select one
        
        Parameters: None
       
        Returns:
            str: The selected save filename
            None: If there are no saved games 
        """
        saves = self.get_save_names()

        if len(saves) == 0:
            print("No saved games found!")
            return None

        print("\nSaved Games:")

        for i in range(len(saves)):
            print(i + 1, "-", saves[i])

        choice = self.get_number(
            "Select a game to load: ", 1, len(saves)
        )

        return saves[choice - 1] + ".dat"

    def load_game(self):
        """
        Purpose: Load a selected saved game.
        
        Parameters: None
        
        Returns:
            bool: True if the game loads successfully,
                  otherwise False.
        """
        filename = self.choose_save_file()

        if filename is None:
            return False

        try:
            file = open(filename, "rb")
            data = pickle.load(file)
            file.close()

            self.towers = []
            for tower_lst in data[0]:
                tower = Stack()

                for disc in tower_lst:
                    tower.push(disc)

                self.towers.append(tower)

            self.num_moves = data[1]
            self.num_discs = data[2]

            print("Save loaded successfully!")
            return True

        except FileNotFoundError:
            print("Unable to load this save!")
            return False
        
def main():
    """
    Purpose: Start the Tower of Hanoi program
   
    Parameters: None
   
    Returns: None
    """
    game = Game()
    game.menu()

main()
