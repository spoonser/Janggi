# Author: Spencer Wagner
# Course: CS325 Section 400
# Date: 8/2/2021
# Description: Homework 6, question 5 - Finds the shortest path from a specified
# 			   Source to a Destination on a puzzle board where some spaces are
# 			   blocked off. Returns the number of spaces between the Source and
# 			   destination, and the path taken to get there 

import sys
from collections import deque

def solve_puzzle(Board, Source, Destination) -> int:
	"""
	Input: Board - A list of lists that represents a puzzle board the 
			       '-' character can be travelled to, '#' spaces may not
		   Source - Starting location on the board, tuple (x, y)
		   Destination - Ending location on the board, tuple (x, y)
	Output: Minimum moves required to travel from Source to Destination
	Description: Translates an input board into a graph, then uses BFS to
				 find the minimum number of moves to travel to the Destination
				 specified. Returns an integer.
	"""
	# Change inputs to match board indexing
	Source = (Source[0] - 1, Source[1] - 1)
	Destination = (Destination[0] - 1, Destination[1] - 1)

	# Exit if source or destination are invalid inputs
	if (Source[0] < 0 or Source[0] >= len(Board) or 
		Source[1] < 0 or Source[1] >= len(Board[0]) or
		Destination[0] < 0 or Destination[0] >= len(Board) or
		Destination[1] < 0 or Destination[1] >= len(Board[0])):
		return None


	# Perform no analysis if the Source or Destination is a barrier
	if (Board[Source[0]][Source[1]] != "-" or 
		Board[Destination[0]][Destination[1]] != "-"):
		return None


	def board_to_graph(Board):
		"""
		Translates the input board into a graph data structure
		"""
		# Initialize an empty adjacency matrix for the result
		num_nodes = len(Board) * len(Board[0])
		adj_matrix = [[0 for x in range(num_nodes)] for x in range(num_nodes)]

		# Loop through input board and fill the adjacency matrix
		cur_node = 0
		for idx in range(len(Board)):
			# Check the nodes above, below, left, and right of the current
			# node, fill the respect element in the matrix with 1 if reachable
			for node in range(len(Board[idx])):
				# Unreachable node
				if Board[idx][node] != "-":
					cur_node += 1
					continue
				
				# Check node above
				if idx - 1 >= 0:
					if Board[idx - 1][node] == "-":
						adj_matrix[cur_node][cur_node - len(Board[0])] = 1

				# Check node below
				if idx + 1 < len(Board):
					if Board[idx + 1][node] == "-":
						adj_matrix[cur_node][cur_node + len(Board[0])] = 1

				# Check node to left
				if node - 1 >= 0:
					if Board[idx][node - 1] == "-":
						adj_matrix[cur_node][cur_node - 1] = 1

				# Check node to right
				if node + 1 < len(Board[0]):
					if Board[idx][node + 1] == "-":
						adj_matrix[cur_node][cur_node + 1] = 1

				cur_node += 1

		return adj_matrix	


	def bfs(adj_matrix, Board, Source, Destination):
		"""
		Performs a breadth-first search on the input adjacency matrix and 
		returns the minimum path from the source to the destination
		"""
		# Initialize a queue and an array for storing whether the node has
		# been visited or not
		queue = deque()
		visited = [False for x in range(len(adj_matrix[0]))]

		# Distance array for storing the path length and prev_vert array
		# for storing the vertex used to get to that vertex
		dist = [sys.maxsize for x in range(len(adj_matrix[0]))]
		prev_vert = [-1 for x in range(len(adj_matrix[0]))]
	
		# Start position
		queue.append(src)
		visited[src] = True
		dist[src] = 0

		# BFS search
		while queue:
			vert = queue.popleft()
			row = adj_matrix[vert]

			for node in range(len(row)):
				# Unvisited nodes are added to the queue
				if visited[node] == False and row[node] == 1:

					visited[node] = True	# Set flag
					dist[node] = dist[vert] + 1	# Calculate distance
					prev_vert[node] = vert	# Set predecessor

					queue.append(node)	# Add to queue

					# If destination is found, end search
					if dest == node:
						return dist, prev_vert

		return False, False	# Path could not be reached				


	def get_path(prev_vert, dest):
		"""
		Returns the directions taken and the which spaces are landed on
		each move through the puzzle path in a nicely formatted string
		"""
		# Find the path taken from the source to the destination
		path = []
		cur_vert = dest
		path.append(cur_vert)
		
		while cur_vert != -1:
			path.append(prev_vert[cur_vert])
			cur_vert = prev_vert[cur_vert]

		# Convert the path to a list of tuples
		path_tups = []
		for vert in reversed(path[1:len(path)-1]):
			row = vert // len(Board[0])
			col = vert - len(Board[0]) * row

			path_tups.append((row + 1, col + 1))
			
		# Destination node added to result path
		row = dest // len(Board[0])
		col = dest - len(Board[0]) * row
		path_tups.append((row + 1, col + 1))

		# Transform the result tuples into a string with directions
		# where U = up, D = down, R = right, L = left
		directions = 'Directions: '
		prev_space = path_tups[0]
		for space in path_tups[1:]:
			if prev_space[0] - space[0] == 1:
				directions += 'U'
			
			elif prev_space[0] - space[0] == -1:
				directions += 'D'

			elif prev_space[1] - space[1] == 1:
				directions += 'L'
			
			else:
				directions += 'R'
			
			prev_space = space

		# Add the moves from source to destination in (x, y) form
		directions += '  Path: '
		path_str = '->'.join(str(space) for space in path_tups)
		directions += path_str

		return directions	


	"""
	Using the above helper functions, find the shortest path from Source
	to Destination
	"""
	# Assign the Source and Destination an integer based on the vertex
	# number. Board is assigned starting at 0, increasing by 1 left to right
	# first, then top to bottom
	src = len(Board[0])*Source[0] + Source[1]
	dest = len(Board[0])*Destination[0] + Destination[1]

	# Get the adjacency matrix and perform bfs
	adj_matrix = board_to_graph(Board)
	dist, prev_vert = bfs(adj_matrix, Board, src, dest)

	# If the destination could not be reached, return None
	if not dist:
		return None

	# Otherwise, print the result (does not count Source and Destination)
	return  (dist[len(Board[0])*Destination[0] + Destination[1]] - 1, 
			get_path(prev_vert, dest))

if __name__ == '__main__':
	board = [['-','-','-','-','-'],
			 ['-','-','#','-','-'],
			 ['-','-','-','-','-'],
			 ['#','-','#','#','-'],
			 ['-','#','-','-','-']]

	print('Example from Homework: ')
	print(solve_puzzle(board, (1,3), (3, 3)))
	print(solve_puzzle(board, (1, 1), (5, 5)))
	print(solve_puzzle(board, (1, 1), (5, 1)))
	print()

	board = [['-', '#', '-', '-'],
			 ['-', '-', '-', '#'],
			 ['#', '-', '#', '-']]

	print('Separate example: ')
	print(solve_puzzle(board, (1, 1), (3, 4)))
	print(solve_puzzle(board, (3, 2), (1, 4)))
	print(solve_puzzle(board, (1, 1), (1, 3)))