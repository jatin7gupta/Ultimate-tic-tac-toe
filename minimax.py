import tictactoe
import random

# This evaluation file gives the heuristic value for a particular game state
# and the last move played in it


class AlphaBetaAgent():
	def __init__(self, evalFn = None, depth = 2):
		self.index = 0
		self.depth = depth

	def evaluation_function(self, game_state):
		value = game_state.calculate_heuristic(game_state, game_state.lastAction, game_state.curr_player)
		return value[0]

	def get_action(self, game_state):
		"""
		Returns the minimax action using self.depth and self.evaluation_function
		"""

		def recurse(game_state, player, depth, alpha, beta):
			if game_state.is_end() or depth == 0:
				return self.evaluation_function(game_state), (-1, -1)

			moves = game_state.get_moves()
			if player == 1:
				ans = (-float('Inf'), (-1, -1))
				for action in moves:
					successor_state = game_state.generate_successor(action)
					ans = max(ans, (recurse(successor_state, -player, depth - 1, alpha, beta)[0], action))
					
					alpha = max(alpha, ans)
					# if alpha >= beta:
					# 	break
				return alpha
			else:
				ans = (float('Inf'), (-1, -1))
				for action in moves:
					successor_state = game_state.generate_successor(action)
					ans = min(ans, (recurse(successor_state, -player, depth - 1, alpha, beta)[0], action)) 	
					beta = min(beta, ans)
					# if alpha >= beta:
					# 	break
				return beta
		alpha0 = (-float('Inf'), (-1, -1))
		beta0 = (+float('Inf'), (-1, -1))
		_, action = recurse(game_state, game_state.get_curr_player(), self.depth, alpha0, beta0)
		
		if action != (-1, -1):
			return action
		else:

			random_move = game_state.get_random_move()
			return random_move
