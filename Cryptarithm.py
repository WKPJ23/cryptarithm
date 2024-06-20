from random import randint  # for random puzzle selection 
from tkinter import *  # for GUI
from tkinter.font import Font
import tkinter.messagebox
import itertools  # for solution
import re  # for solution

#################################################################

# SECTION 1

# Solution (solve, letter_replace, & valid) imported and modified based off of Peter Norvig, 2014
# Norvig, P. (2014). Cryptarithmetic (alphametic) problems. GitHub. https://github.com/norvig/pytudes/blob/main/ipynb/Cryptarithmetic.ipynb 

# NOTE: Depending on the puzzle, the solution can take up to 15 seconds to solve - please be patient.

def solve(formula):  # Given a certain cryptarithm (i.e., SEND + MORE = MONEY), this solution substitutes the letters with digits to solve it as if it were a mathematical equation
    return filter(valid, letter_replace(formula))

def letter_replace(formula):  # Goes over all possible letter/digit replacements in the formula
    formula = formula.replace(' = ', ' == ')  # Allow = or ==
    letters = cat(set(re.findall('[A-Z]', formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        yield formula.translate(str.maketrans(letters, cat(digits)))

def valid(exp):  # Expression is valid if it does not contain a leading 0 (as we do not write equations with them), and evaluates to true
    try:
        return not lead_zero(exp) and eval(exp) is True
    except ArithmeticError:
        return False
    
cat = ''.join  # Function to concatenate strings
lead_zero = re.compile(r'\b0[0-9]').search  # Function to check for illegal number

#################################################################

# SECTION 2

#List of a handful of potential cryptarithm puzzles; there are some puzzles that contain numbers (usually 2 as a substitute for 'to' or 'too') but they were excluded due to the nature of the syntax:

P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15 = ('NUM + BER = PLAY', "SEND + MORE = MONEY", "X / X = X ", "TWO + TWO = FOUR", "WRONG + WRONG = RIGHT", "ALPHABET + LETTERS = SCRABBLE", "POTATO + TOMATO = PUMPKIN", "WASH + YOUR = HANDS", "DOUBLE + DOUBLE + TOIL = TROUBLE", "NORTH / SOUTH = EAST / WEST", "DO + YOU + FEEL = LUCKY", "NOW + WE + KNOW + THE = TRUTH", "I + GUESS + THE + TRUTH = HURTS", "HAWAII + IDAHO + IOWA + OHIO = STATES", "ZEROES + ONES = BINARY") 

puzzle_list = (P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15)  # I feel like there's a more efficient way to do this...
n = randint(0, len(puzzle_list))  # generates random number to correspond to puzzle
puzzle_x = puzzle_list[n]  # selects puzzle based on randomly generated number

solution = next(solve(puzzle_x))  #This solves the given puzzle using the code above
solution_join = "".join(num for num in solution if num.isdigit())  # this series of steps extracts a list of unique digits to be matched against the user input
solution_sort = sorted(set(solution_join), key=solution_join.index)
solution_list = list(solution_sort)

#################################################################

#prompt that briefly explains the puzzle

tkinter.messagebox.showinfo("HOW TO PLAY", "Each letter in the cryptarithm puzzle corresponds to a number between 0 & 9. Enter the correct number in the fields so that the equation is balanced. For instance: in 'X/X = X', X is equal to 1. Press 'OK' to continue.") 

#################################################################

# SECTION 3

# GUI creation & puzzle checker

class Crypta: # creates Tkinter class

    def __init__(self):
        window = Tk() # Create a window
        window.title("Check Cryptarithm Solution") # Set title
        colour_main = "papaya whip" #make the window look pretty
        window.configure(bg = colour_main)
        window.geometry("375x400") # set window size (set to 400 to accomodate all 10 digits)
        puzzle_font = Font( # sets different fonts for different widgets
            family="Arial Narrow",
            size = 12,
            weight = "bold"
        )
        prompt_font = Font(
            family="Calibri Light",
            size=12,
            weight="normal",
            slant="roman"
        )

        user_list = []  # creates empty list, will be used to compare solution list

        def verify_values():  # this function will be enacted using the button below - this is the verification function, which will create a list from user entry and compare it with the solution list to determine whether it is correct
            entry_list = ""
            for entries in user_list:
                entry_list = entry_list + str(entries.get())
            entry_list = list(entry_list)
            if entry_list == solution_list:
                tkinter.messagebox.showinfo("Check Cryptarithm Solution", "Correct!") # displays window informing user if they are correct or incorrect
            else:
                tkinter.messagebox.showerror("Check Cryptarithm Solution", "Incorrect. Please try again.")

        prompt = Message(window, text="Enter the solution for the cryptarithm displayed here:", bg=colour_main, justify=CENTER, font=prompt_font)  # provides further instruction to the user
        prompt.grid(row=1, column=1)  # grid will help organize the widgets spatially
        puzzle = Message(window, text=puzzle_x, bg=colour_main, font=puzzle_font, relief ="sunken")  # displays the randomly selected puzzle
        puzzle.grid(row=1, column=2)

        puzzle_join = "".join(char for char in puzzle_x if char.isalpha())  # this series of code extracts the unique alphabetic values from the puzzle to determine the number of letters to be displayed
        puzzle_sorted = sorted(set(puzzle_join), key=puzzle_join.index)  # sorts to keep letters in proper order
        puzzle_list = list(puzzle_sorted)  # converts to a list

        for i in range(len(puzzle_list)):  # do below for every letter in puzzle (n <= 10)
            Label(window, text=(puzzle_list[i], "="),  bg=colour_main).grid(row = i+2, column=2)  # diplays every unique letter
            user_input = Entry(window, width=3, justify=CENTER, relief="ridge") # creates entry boxes for each letter
            user_input.grid(row=i+2, column=3, pady=5)
            user_list.append(user_input)  # will add each user entry to the list which will be compared against the solution_list

        Button(window, text="Check Answer", command=verify_values, bg="salmon").grid(row=1, padx=10, pady=10, column=3)  # this button will initiate the function verify_values outlined above when the user is done entering their numbers

        window.mainloop()  # runs the above code
        
        
Crypta()  # Creates the GUI

#################################################################