# Tulane University, CMPS 1500, Spring 2023
#
# STUDENTS MUST FILL IN BELOW
#
# Student name: Kevin Skelly
# Student email address: kskelly@tulane.edu
#
# Collaborators:

# NOTE: you must write your own code. You may discuss the assignment with 
#       professors, TAs, other students, or family members. But you MUST
#       list anyone you collaborated with in the space above.

# ALSO NOTE: You must add comments which explain how your solution works.
#            If you do not do this, your solution will not receive credit.

from BoggleFunctions import BoggleBoardGenerator, remove_letter
from BoggleWordlist import BoggleWordlist


class GameBoard():
    """ an instance of a boggle board, for use by BoggleGame """

    def __init__(self, game_size=4):
        self.edge_length = game_size  # boards are always square
        self.board_letters = BoggleBoardGenerator(game_size)  # don't change this line
        # Students may set their own board for testing below, but any custom
        # board below here must be commented out before submitting for grading
        # self.board_letters = [['H', 'B', 'W', 'O'],
        #                       ['T', 'G', 'I', 'C'],
        #                       ['W', 'G', 'E', 'R'],
        #                       ['B', 'T', 'S', 'U']]

    def __len__(self):
        """ the length of a GameBoard will be the length of one edge """
        return self.edge_length

    def __str__(self):  ### TODO STEP 1: make the game board printable
        """ Convert our GameBoard object to a string for printing"""
        rows = ""
        for x in self.board_letters:
            line = " "
            for y in x:
                line += y
                if y != x[-1]:
                    line += " - "
            line += "\n"
            rows += line
        return rows


class BoggleGame():
    """ This class will contain everything needed to play a game of Boggle."""

    def __init__(self, game_size=4):
        """ Create a new game object."""
        # default board size is 4x4
        self.gameboard = GameBoard(game_size)  # GameBoard object
        self.wordlist = BoggleWordlist().words  # all valid words
        self.words_already_used = []  # begin with empty list
        self.score = 0  # score begins at zero

    def compute_word_score(self, word):
        """ given a word, return a number corresponding to the score for that word"""
        word_score = 0  # Set empty counter for the length of the word
        if len(word) == 3 or len(word) == 4:  # If the word is 3 or 4 characters award 1 point
            word_score = 1
        if len(word) == 5:  # If the worst is 5 characters award 2 points
            word_score = 2
        if len(word) == 6:  # If the word is 6 characters award 3 points
            word_score = 3
        if len(word) == 7:  # If the word is 7 characters award 5 points
            word_score = 5
        if len(word) >= 8:  # And if the word is 8 or more characters award 11 points
            word_score = 11
        return word_score  # TODO STEP 2: compute score according to rules on handout

    def is_valid_guess(self, word):
        """ returns True if word is a valid guess, False if not"""
        # check 4 things:
        # 1. is word greater than or equal to 3 letters long?
        # 2. is word in the wordlist? (note: wordlist is lower case)
        # 3. has the word already been used? (note: words_already_used is case)
        # 4. can word be found using the letters in the game board?
        #    (This can be done in phases. A full solution should use
        #     the helper functions below)
        if len(word) < 3:  # If the word is too short for boggle rules it won't be counted
            return False
        if word.lower() not in self.wordlist:  # If the word is not a registered word it won't be counted
            return False
        if word.lower() in self.words_already_used:  # If the word has already been used it won't be counted
            return False
        for x in str(word):  # If each letter in the word exists on the board then continue
            if self.find_letter_on_board(x) == []:  # If a letter can't be found return false
                return False
        list = self.find_letter_on_board(word[0])  # Create a list of the locations of the starting letter
        for var in list:
            row = var[0]  # Set the row variable using the row,col tuple
            col = var[1]  # Do the same thing with col
            board = self.gameboard.board_letters  # Set the board
            if self.check_string_starting_at(word, board, row, col):  # Run the boggle string function and
                return True  # Return true if the string can be completely found
        else:
            return False  # If the function fails then return false
        # TODO STEP 3+: check if the guess is valid

    def find_letter_on_board(self, letter):
        tuplelist = []  # Empty list for tuples
        row = -1  # Row counter
        for x in self.gameboard.board_letters:  # Iterates through each row list
            row += 1  # Sets the current row
            column = -1  # Column counter
            for y in x:  # Iterate through the first row
                column += 1  # Sets current column
                if y == letter:  # If the letter is equal to the list element
                    pair = (row, column)  # Set the pair
                    tuplelist.append(pair)  # Add the pair to the list
        """ returns a list of tuples of (row,column) for each location on the
        gameboard where the letter can be found. (Empty list returned if
        the letter cannot be found"""

        return tuplelist  # TODO: write helper function to be used in is_valid_guess

    def is_in_bounds(self, row, col):
        if row < 0 or col < 0:
            return False
        if row >= self.gameboard.edge_length or col >= self.gameboard.edge_length:
            return False
        else:
            return True  # TODO: write helper function here

    def check_string_starting_at(self, string, board, row, col):
        if len(string) == 0:  # Begin by checking the length as a base case
            return True  # Once the string has been run through return true
        if not self.is_in_bounds(row, col):  # Checks to see if the letter returns out of bounds
            return False
        letter = string[0]
        if board[row][col] != letter:  # Another function to make sure the recursion is starting at the right point
            return False
        else:  # Begin the recursive function
            newboard = remove_letter(board, row, col)  # Set a mew board without our starting letter
            downleft = self.check_string_starting_at(string[1:], newboard, row - 1, col - 1) # Set each direction variable
            left = self.check_string_starting_at(string[1:], newboard, row - 1, col)
            upleft = self.check_string_starting_at(string[1:], newboard, row - 1, col + 1)
            up = self.check_string_starting_at(string[1:], newboard, row, col - 1)
            down = self.check_string_starting_at(string[1:], newboard, row, col + 1)
            downright = self.check_string_starting_at(string[1:], newboard, row + 1, col - 1)
            right = self.check_string_starting_at(string[1:], newboard, row + 1, col)
            upright = self.check_string_starting_at(string[1:], newboard, row + 1, col + 1)
            if downleft:  # Check through each direction variable to see if the recursion can be run starting from the
                return True  # Next letter in a certain direction
            elif left:
                return True
            elif upleft:
                return True
            elif up:
                return True
            elif down:
                return True
            elif downright:
                return True
            elif right:
                return True
            elif upright:
                return True
            else:
                return False

        """ checks to see if a string can be found starting at position
        (row, col) on the board given as a parameter. If it can be found
        there (according to the Boggle rules), return True. If it can't,
        return False.

        Note that it takes a board as input. You should check this board,
        and not self.gameboard. Why? Because the Boggle rules specify that
        a valid word can only use each letter on the board once. So, when
        checking for a valid word, once a letter is ``used'' for that word,
        we'll need to remove it from a copy of the board, and then search
        for the rest of the word on that copy (which has the ``used'' letter
        removed).

        To make this easier, we have provided a function to make this copy
        of the board for you: remove_letter(board, row, col)

        You should only need to use this in the check_string_starting_at
        method. self.gameboard should stay unchanged, so that the game can
        continue after we're done checking for a word's validity.

        Note: this method is intended to be used RECURSIVELY! So smaller slices 
        of string will get passed back to this function until reaching a base 
        case."""
        return True  # TODO: write helper function to be used in is_valid_guess

    # Students: there is no need to change anything below here
    def play_game(self):
        print("Game board:\n")
        print(self.gameboard)
        print(f"Current score is: {self.score}")

        guessedword = input("Guess a word: ").upper()
        # guessedword will be upper case since the letters on the board are upper case

        while (guessedword != 'Q'):
            if self.is_valid_guess(guessedword):
                print(f"Correct! You get {self.compute_word_score(guessedword)} points.")
                self.score += self.compute_word_score(guessedword)
                self.words_already_used.append(guessedword.lower())
            print(self.gameboard)
            print(f"Current score: {self.score} Correct words: {self.words_already_used}")
            guessedword = input("Guess a word (type q when finished): ").upper()
        print(f"Done, final score: {self.score}")


if __name__ == '__main__':  # your program will begin execution here
    game = BoggleGame()
    game.play_game()