import random
import copy
import numpy as np


# Player -1 is o(opponent), +1 is x (us)
class Game:
	def __init__(self):
		self.board = np.zeros((3**2, 3**2))
		self.curr_player = 1  
		self.valid_moves = [(x, y) for x in range(3 * 3) for y in range(3 * 3)]
		self.num_moves = 0
		self.winner = 0
		self.lastAction = tuple()

	def get_moves(self):
		return self.valid_moves

	def get_num_moves(self):
		return self.num_moves

	def get_random_move(self):
		return random.choice(self.valid_moves)

	def get_curr_player(self):
		return self.curr_player

	def get_board(self):
		return self.board

	def get_winner(self):
		return self.winner

	def is_end(self):
		return self.winner != 0 or not self.valid_moves
	
	def generate_successor(self, action):
		new_game = copy.deepcopy(self)
		new_game.move(action)
		return new_game

	# Option = 1: 9x9 board
	# Option = 2: 3x3 board of mini wins
	def print_board(self, option=1):
		print('*****'*5)
		board = self.board 
		for i in range(len(board)):
			if i % 3 == 0:
				print()
			row = board[i]
			str_row = []
			for player in row:
				if player == -1:
					str_row.append('o')
				elif player == 1:
					str_row.append('x')
				else:
					str_row.append('_')
			str_row = ' '.join(str_row)
			str_row2 = ''
			for j in range(3):
				str_row2 = str_row2 + str_row[2*3*j: 2*3*(j+1)] + ' '
			print(str_row2)
			if (i + 1) % 3 == 0:
				print

	# Make current player move to position pos specified by tuple (row, col)
	def move(self,pos):
		if not pos in self.valid_moves:
			print ('Exception for : ', pos)
			raise Exception("Invalid Move")
		self.board[pos[0]][pos[1]] = self.curr_player
		self.update_mini_winners(pos)
		self.update_valid_moves(pos)
		self.curr_player = -self.curr_player
		self.num_moves += 1
		self.lastAction = pos

	# Update list of valid moves for the player based on last played move by opponent
	def update_valid_moves(self, pos):
		self.valid_moves = []

		# Look at all the squares in the current mini-board
		r0 = pos[0] % 3
		c0 = pos[1] % 3
		for dr in range(3):
			for dc in range(3):
				r = 3*r0 + dr
				c = 3*c0 + dc
				if self.board[r][c] == 0:
					self.valid_moves.append((r, c))

	# TODO: doubt
	# Utility method called by move method
	# Updates the grid specifying which mini-boards have been won by which players
	def update_mini_winners(self, pos):
		r0 = pos[0]//3
		c0 = pos[1]//3

		row = r0 * 3
		col = c0 * 3

		mini_board = self.board[row: row + 3, col: col + 3]
		if self.has_winning_pattern(mini_board):
			self.winner = self.curr_player

	# Checks a 3 by 3 board to find a winning pattern
	def has_winning_pattern(self, board):
		# Check row totals
		for dr in range(3):
			row_total = sum(board[dr, i] for i in range(3))
			if abs(row_total) == 3:
				return True
				
		# Check column totals
		for dc in range(3):
			col_total = sum(board[i, dc] for i in range(3))
			if abs(col_total) == 3:
				return True

		# Check diagonal totals
		diag_total = sum(board[i, i] for i in range(3))
		if abs(diag_total) == 3:
			return True
		
		diag_total = sum(board[3 - 1 - i, i] for i in range(3))
		if abs(diag_total) == 3:
			return True
		return False

	# Find mini-board based on position(row, column) tuple
	def get_mini_board(self, game_state, pos):
		r0 = pos[0]//3
		c0 = pos[1]//3

		row = r0 * 3
		col = c0 * 3

		mini_board = game_state.board[row: row + 3, col: col + 3]
		return mini_board

	def calculate_heuristic(self, game_state, action, player):
		mini_board = self.get_mini_board(game_state, action)

		# x - player's heuritic points
		# o - opponent's heuritic points
		
		x1 = self.three_in_a_row(mini_board, player)
		x2 = self.two_p1_one_p2(mini_board, player)
		x3 = self.fork(mini_board, player)
		x4 = self.play_centre(mini_board, player)
		x5 = self.block_opposite_corner(mini_board, player)
		x6 = self.play_empty_corner(mini_board, player)
		x7 = self.two_p1_next_empty(mini_board, player)
		x8 = self.create_fork(mini_board, player)
		x9 = self.block_opp_fork(mini_board, player)
		x10 = self.two_p1_next_empty(mini_board, -player)

		o1 = self.three_in_a_row(mini_board, -player)
		o2 = self.two_p1_one_p2(mini_board, -player)
		o3 = self.fork(mini_board, -player)
		o4 = self.play_centre(mini_board, -player)
		o5 = self.block_opposite_corner(mini_board, -player)
		o6 = self.play_empty_corner(mini_board, -player)
		o7 = self.two_p1_next_empty(mini_board, -player)
		o8 = self.create_fork(mini_board, -player)
		o9 = self.block_opp_fork(mini_board, -player)
		o10 = self.two_p1_next_empty(mini_board, player)

		w1 = 1000
		w2 = -7.0
		w3 = 4
		w4 = 0.5
		w5 = 2
		w6 = 0.4
		w7 = 7
		w8 = 3
		w9 = 4
		w10 = 8

		t1 = w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + w6*x6 + w7*x7 + w8 * x8 + w9*x9 + w10*x10
		t2 = w1*o1 + w2*o2 + w3*o3 + w4*o4 + w5*o5 + w6*o6 + w7 * o7 + w8 * o8 + w9*o9 + w10*o10

		value = t1 - t2
		return value, action

	# Calculate number of 3 X/O in a row/column/diagonal
	def three_in_a_row(self, mini_board, player):
		total = 0

		for dr in range(3):
			row_total = sum(mini_board[dr, i] for i in range(3))
			if player == 1:
				if row_total == 3*player:
					total += 1
			else :
				if abs(row_total) == 3:
					total += 1
		
		# Check column totals
		for dc in range(3):
			col_total = sum(mini_board[i, dc] for i in range(3))
			if player == 1:
				if col_total == 3*player:
					total += 1
			else :
				if abs(col_total) == 3:
					total += 1

		# Check diagonal totals
		diag_total = sum(mini_board[i, i] for i in range(3))
		if player == 1:
			if diag_total == 3*player:
				total += 1
		else:
			if abs(diag_total) == 3:
				total += 1
		
		diag_total = sum(mini_board[3 - 1 - i, i] for i in range(3))
		if player == 1:
			if diag_total == 3*player:
				total += 1
		else:
			if abs(diag_total) == 3:
				total += 1
		
		return total

	def two_p1_next_empty(self, mini_board, player):
		row_total = 0
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if mini_board[dr][dc] == player:
					p1 += 1
				elif mini_board[dr][dc] == 0:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if mini_board[dc][dr] == player:
					p1 += 1
				elif mini_board[dc][dr] == 0:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		# L2R diagonal
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if dr != dc:
					continue

				if mini_board[dc][dr] == player:
					p1 += 1
				elif mini_board[dc][dr] == 0:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		# R2L diagonal
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				
				if dr + dc != 2: 
					continue
				
				if mini_board[dr][dc] == player:
					p1 += 1
				elif mini_board[dr][dc] == 0:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		return row_total

	# Calculate number of - 2 of 1 kind and 1 of other kind
	def two_p1_one_p2(self, mini_board, player):
		row_total = 0
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if mini_board[dr][dc] == player:
					p1 += 1
				elif mini_board[dr][dc] == -player:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if mini_board[dc][dr] == player:
					p1 += 1
				elif mini_board[dc][dr] == -player:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		# L2R diagonal
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				if dr != dc:
					continue

				if mini_board[dc][dr] == player:
					p1 += 1
				elif mini_board[dc][dr] == -player:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		# R2L diagonal
		for dr in range(0, 3):
			p1, p2 = 0, 0
			for dc in range(0, 3):
				
				if dr + dc != 2: 
					continue
				
				if mini_board[dr][dc] == player:
					p1 += 1
				elif mini_board[dr][dc] == -player:
					p2 += 1
				else:
					continue
			if p1 == 2 and p2 == 1:
				row_total += 1

		return row_total

	# Block Opponents Fork move
	def block_opp_fork(self, mini_board, player):
		total = 0

		corners = [mini_board[0][0], mini_board[0][2], mini_board[2][0], mini_board[2][2]]

		if corners[0] == -player and corners[1] == -player and mini_board[1][1] == 0:
			if corners[3] == 0  and mini_board[1][2] == 0 and mini_board[0][1]:
				total += 1
			elif corners[2] == 0 and mini_board[1][0] == 0 and mini_board[0][1]:
				total += 1
		
		if corners[1] == -player and corners[3] == -player and mini_board[1][1] == 0:
			if corners[0] == 0 and mini_board[1][2] == 0 and mini_board[0][1]:
				total += 1
			elif corners[2] == 0 and mini_board[2][1] == 0 and mini_board[1][2]:
				total += 1

		if corners[3] == -player and corners[2] == -player and mini_board[1][1] == 0:
			if corners[0] == 0 and mini_board[1][0] == 0 and mini_board[2][1]:
				total += 1
			elif corners[1] == 0 and mini_board[1][2] == 0 and mini_board[2][1]:
				total += 1

		if corners[0] == -player and corners[2] == -player and mini_board[1][1] == 0:
			if corners[3] == 0 and mini_board[2][1] == 0 and mini_board[1][0]:
				total += 1
			elif corners[1] == 0 and mini_board[0][1] == 0 and mini_board[1][0]:
				total += 1
		
		return total

	# Calculate number of moves where player can fork
	def fork(self, mini_board, player):
		row_total = 0
		if mini_board[0][0] == player and mini_board[0][2] == player and mini_board[2][0] == player and mini_board[1][1] == 0 and not mini_board[2][2] == player:
			if mini_board[0][1] != -player and mini_board[1][0] != -player:
				row_total += 1
		
		if mini_board[2][2] == player and mini_board[0][2] == player and mini_board[0][0] == player and mini_board[1][1] == 0 and not mini_board[2][0] == player:
			if mini_board[0][1] != -player and mini_board[1][2] != -player:
				row_total += 1
		
		if mini_board[2][2] == player and mini_board[0][2] == player and mini_board[2][0] == player and mini_board[1][1] == 0 and not mini_board[0][0] == player:
			if mini_board[2][1] != -player and mini_board[1][2] != -player:
				row_total += 1
		
		if mini_board[0][0] == player and mini_board[2][2] == player and mini_board[2][0] == player and mini_board[1][1] == 0 and not mini_board[0][2] == player:
			if mini_board[2][1] != -player and mini_board[1][0] != -player:
				row_total += 1

		return row_total
		# print (f'cols total 

	# Calculate heuristic  center if it is empty
	def play_centre(self, mini_board, player):
		if mini_board[1][1] == 0:
			return 1
		else:
			return -1

	# If opponent is in corner, play opposite corner
	def block_opposite_corner(self, mini_board, player):
		opp = {0: 2, 2: 0}
		row_total = 0

		for dr in range(0, 3):
			for dc in range(0, 3):

				if dr % 2 != 0 or dc % 2 != 0:
					continue
				
				if mini_board[dr][dc] == -player:
					if mini_board[opp[dr]][opp[dc]] == 0:
						row_total += 1

		return row_total
	
	# Heuristic to play at empty corner
	def play_empty_corner(self, mini_board, player):
		row_total = 0.0
		corners_list = [mini_board[0][0], mini_board[0][2], mini_board[2][0], mini_board[2][2]]

		for corner in corners_list:
			if corner == 0:
				row_total += 0.25
			
		return row_total
	
	def create_fork(self, mini_board, player):

		total = 0

		corners = [mini_board[0][0], mini_board[0][2], mini_board[2][0], mini_board[2][2]]

		if corners[0] == player and corners[1] == player and mini_board[1][1] == 0:
			if corners[3] == 0  and mini_board[1][2] == 0 and mini_board[0][1]:
				total += 1
			elif corners[2] == 0 and mini_board[1][0] == 0 and mini_board[0][1]:
				total += 1
		
		if corners[1] == player and corners[3] == player and mini_board[1][1] == 0:
			if corners[0] == 0 and mini_board[1][2] == 0 and mini_board[0][1]:
				total += 1
			elif corners[2] == 0 and mini_board[2][1] == 0 and mini_board[1][2]:
				total += 1

		if corners[3] == player and corners[2] == player and mini_board[1][1] == 0:
			if corners[0] == 0 and mini_board[1][0] == 0 and mini_board[2][1]:
				total += 1
			elif corners[1] == 0 and mini_board[1][2] == 0 and mini_board[2][1]:
				total += 1

		if corners[0] == player and corners[2] == player and mini_board[1][1] == 0:
			if corners[3] == 0 and mini_board[2][1] == 0 and mini_board[1][0]:
				total += 1
			elif corners[1] == 0 and mini_board[0][1] == 0 and mini_board[1][0]:
				total += 1
		
		return total

	