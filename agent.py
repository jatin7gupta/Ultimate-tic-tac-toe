#!/usr/bin/python3


import socket
import sys
import numpy as np
import math
import tictactoe
from minimax import AlphaBetaAgent

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#  -1 - They played here




# instantiate the alpha beta agent
agent = AlphaBetaAgent(depth=4)  
myGame = tictactoe.Game()

# instantiate global variables
user_played_board = -1
last_tile = -1
user_played_tile = int()


# choose a move to play
def play():
    global myGame, user_played_board, user_played_tile
    
    position_played = agent.get_action(myGame)
    myGame.move(position_played)

    board_tile = numpy2board(position_played)
    user_played_board = board_tile[0]
    user_played_tile = board_tile[1]
    # print("playing", board_tile)

    return board_tile[1]

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        
        pos = board2numpy(int(args[0]), int(args[1]))
        myGame.board[pos[0]][pos[1]] = -1
        myGame.update_valid_moves(pos)
        
        return play()

    elif command == "third_move":
        # update the first move
        ourMove = board2numpy(int(args[0]), int(args[1]))
        myGame.board[ourMove[0]][ourMove[1]] = 1
        # update the second move
        oppMove = board2numpy(int(args[1]), int(args[2]))
        myGame.board[oppMove[0]][oppMove[1]] = -1

        myGame.update_valid_moves(oppMove)

        return play()

    elif command == "next_move":
        pos = board2numpy(user_played_tile, int(args[0]))
        myGame.curr_player = 1
        myGame.board[pos[0]][pos[1]] = -1
        myGame.update_valid_moves(pos)

        if myGame.get_num_moves() == 10:
            agent.depth += 1

        return play()

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0


# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])  # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    
    myGame.currPlayer = 1   
    while True:
        text = s.recv(1024).decode()
        response = ''
        if not text:
            continue
        for line in text.split("\n"):
            
            response = parse(line)
            if response == -1:
                # print ('number of moves: ',myGame.num_moves)
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())
        myGame.print_board()
        # print("Sending response: " + str(response))
        # print("***"*10)


# board, tile - [1, 9] for the server
# row, col - [0, 8] for us
def board2numpy(board, tile):
    board_to_numpy = {
        (1, 1): (0, 0),
        (1, 2): (0, 1),
        (1, 3): (0, 2),
        (1, 4): (1, 0),
        (1, 5): (1, 1),
        (1, 6): (1, 2),
        (1, 7): (2, 0),
        (1, 8): (2, 1),
        (1, 9): (2, 2),
        (2, 1): (0, 3),
        (2, 2): (0, 4),
        (2, 3): (0, 5),
        (2, 4): (1, 3),
        (2, 5): (1, 4),
        (2, 6): (1, 5),
        (2, 7): (2, 3),
        (2, 8): (2, 4),
        (2, 9): (2, 5),
        (3, 1): (0, 6),
        (3, 2): (0, 7),
        (3, 3): (0, 8),
        (3, 4): (1, 6),
        (3, 5): (1, 7),
        (3, 6): (1, 8),
        (3, 7): (2, 6),
        (3, 8): (2, 7),
        (3, 9): (2, 8),
        (4, 1): (3, 0),
        (4, 2): (3, 1),
        (4, 3): (3, 2),
        (4, 4): (4, 0),
        (4, 5): (4, 1),
        (4, 6): (4, 2),
        (4, 7): (5, 0),
        (4, 8): (5, 1),
        (4, 9): (5, 2),
        (5, 1): (3, 3),
        (5, 2): (3, 4),
        (5, 3): (3, 5),
        (5, 4): (4, 3),
        (5, 5): (4, 4),
        (5, 6): (4, 4),
        (5, 7): (5, 3),
        (5, 8): (5, 4),
        (5, 9): (5, 5),
        (6, 1): (3, 6),
        (6, 2): (3, 7),
        (6, 3): (3, 8),
        (6, 4): (4, 6),
        (6, 5): (4, 7),
        (6, 6): (4, 8),
        (6, 7): (5, 6),
        (6, 8): (5, 7),
        (6, 9): (5, 8),
        (7, 1): (6, 0),
        (7, 2): (6, 1),
        (7, 3): (6, 2),
        (7, 4): (7, 0),
        (7, 5): (7, 1),
        (7, 6): (7, 2),
        (7, 7): (8, 0),
        (7, 8): (8, 1),
        (7, 9): (8, 2),
        (8, 1): (6, 3),
        (8, 2): (6, 4),
        (8, 3): (6, 5),
        (8, 4): (7, 3),
        (8, 5): (7, 4),
        (8, 6): (7, 5),
        (8, 7): (8, 3),
        (8, 8): (8, 4),
        (8, 9): (8, 5),
        (9, 1): (6, 6),
        (9, 2): (6, 7),
        (9, 3): (6, 8),
        (9, 4): (7, 6),
        (9, 5): (7, 7),
        (9, 6): (7, 8),
        (9, 7): (8, 6),
        (9, 8): (8, 7),
        (9, 9): (8, 8)
    }
    return board_to_numpy[(board, tile)]

# reverse of board and title
def numpy2board(position):
    numpy_to_board = {
        (0, 0): (1, 1),
        (0, 1): (1, 2),
        (0, 2): (1, 3),
        (1, 0): (1, 4),
        (1, 1): (1, 5),
        (1, 2): (1, 6),
        (2, 0): (1, 7),
        (2, 1): (1, 8),
        (2, 2): (1, 9),
        (0, 3): (2, 1),
        (0, 4): (2, 2),
        (0, 5): (2, 3),
        (1, 3): (2, 4),
        (1, 4): (2, 5),
        (1, 5): (2, 6),
        (2, 3): (2, 7),
        (2, 4): (2, 8),
        (2, 5): (2, 9),
        (0, 6): (3, 1),
        (0, 7): (3, 2),
        (0, 8): (3, 3),
        (1, 6): (3, 4),
        (1, 7): (3, 5),
        (1, 8): (3, 6),
        (2, 6): (3, 7),
        (2, 7): (3, 8),
        (2, 8): (3, 9),
        (3, 0): (4, 1),
        (3, 1): (4, 2),
        (3, 2): (4, 3),
        (4, 0): (4, 4),
        (4, 1): (4, 5),
        (4, 2): (4, 6),
        (5, 0): (4, 7),
        (5, 1): (4, 8),
        (5, 2): (4, 9),
        (3, 3): (5, 1),
        (3, 4): (5, 2),
        (3, 5): (5, 3),
        (4, 3): (5, 4),
        (4, 4): (5, 5),
        (4, 5): (5, 6),
        (5, 3): (5, 7),
        (5, 4): (5, 8),
        (5, 5): (5, 9),
        (3, 6): (6, 1),
        (3, 7): (6, 2),
        (3, 8): (6, 3),
        (4, 6): (6, 4),
        (4, 7): (6, 5),
        (4, 8): (6, 6),
        (5, 6): (6, 7),
        (5, 7): (6, 8),
        (5, 8): (6, 9),
        (6, 0): (7, 1),
        (6, 1): (7, 2),
        (6, 2): (7, 3),
        (7, 0): (7, 4),
        (7, 1): (7, 5),
        (7, 2): (7, 6),
        (8, 0): (7, 7),
        (8, 1): (7, 8),
        (8, 2): (7, 9),
        (6, 3): (8, 1),
        (6, 4): (8, 2),
        (6, 5): (8, 3),
        (7, 3): (8, 4),
        (7, 4): (8, 5),
        (7, 5): (8, 6),
        (8, 3): (8, 7),
        (8, 4): (8, 8),
        (8, 5): (8, 9),
        (6, 6): (9, 1),
        (6, 7): (9, 2),
        (6, 8): (9, 3),
        (7, 6): (9, 4),
        (7, 7): (9, 5),
        (7, 8): (9, 6),
        (8, 6): (9, 7),
        (8, 7): (9, 8),
        (8, 8): (9, 9)
    }
    return numpy_to_board[position]


if __name__ == "__main__":
    main()
