from tkinter import *
from Game import Game

def main():
    turn = input("Enter 1 to go first, Enter 2 to go second: ")
    game = Game(int(turn))
main()