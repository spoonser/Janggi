# Course: CS261 - Data Structures
# Author: Spencer Wagner
# Assignment: 6
# Description: Directed graph class implementation

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Input: None
        Output: None, modifies self
        Description: Places a new list in the adjacency matrix that represents
                     a new vertex 
        """
        # Add an empty list and increase the vertex count
        self.adj_matrix.append([])
        self.v_count += 1

        # For every existing vertex in the matrix, append a new zero for the
        # new-added component, and fill the new component list with zeros
        for sublist in self.adj_matrix:
            while len(sublist) < self.v_count:
                sublist.append(0)
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Input: src - Index to forms edge pointed at dst
               dst - Index to forms edge pointed at from src
               weight - Weight assigned to edge
        Output: None, modifies self
        Description: Assigns an edge pointed from src to dst in the adjacency
                     matrix with input weight
        """
        # Do nothing if vertices do not exist, are the same, or weight < 1
        if (src == dst) or (src < 0) or (dst < 0) or \
           (src >= self.v_count) or (dst >= self.v_count) or (weight < 1):
            return
        
        # Assign the weight to edge pointed from src to dst
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Input: src - Index that has edge pointed at dst
               dst - Index that has edge pointed at from src
        Output: None, modifies self
        Description: Removes edge that exists from the src to dst index
        """
        # Do nothing if either vertex does not exist
        if (src < 0) or (dst < 0) or \
           (src >= self.v_count) or (dst >= self.v_count):
           return

        # Revert the edge weight at index to zero
        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Input: None
        Output: List of vertices in adjacency matrix
        Description: Returns a list of vertices in the graph
        """
        res = []
        
        # Append a number to the result for each index in the adjacency matrix
        for idx in range(self.v_count):
            res.append(idx)
        return res
        
    def get_edges(self) -> []:
        """
        Input: None
        Output: A list of tuples that represent edges in self
        Description: Returns a list of edges in the format of tuple 
                     (src, dst, weight)
        """
        res = []

        # Loop through the adjacency matrix and append edges to the res list
        for idx in range(self.v_count):
            for sub_idx in range(len(self.adj_matrix[idx])):
                if self.adj_matrix[idx][sub_idx] > 0:
                    res.append((idx, sub_idx, self.adj_matrix[idx][sub_idx]))
        return res

    def is_valid_path(self, path: []) -> bool:
        """
        Input: path - a sequence of vertices
        Output: True/False
        Description: Returns True if the sequence of vertices represents a 
                     valid path in the graph
        """
        # Loop through the path and attempt to traverse the graph
        for idx in range(len(path) - 1):
            # Catch invalid vertex
            if (path[idx] < 0) or (path[idx] >= self.v_count):
                return False
            
            # Check if next index can be reached from the current index
            if not self.adj_matrix[path[idx]][path[idx + 1]]:
                return False
        return True  # Path successfully traversed

    def dfs(self, v_start, v_end=None) -> []:
        """
        Input: v_start - Index to begin search
               v_end - Optional index to end search
        Output: List of visited nodes
        Descriptions: Returns a list of nodes visited during a depth-first
                      search from v_start to v_end (if provided)
        """
        # Initialize set of vertices visited and stack
        visited = []
        stack = []

        # If the start index isn't in the graph, exit
        if (v_start < 0) or (v_start >= self.v_count):
            return visited

        # Push starting vertex to stack to initialize the search
        stack.append(v_start)

        while stack:
            # Pop top of stack 
            cur_vert = stack.pop()

            # If that vertex has yet to be visited, append its successors
            if cur_vert not in visited:
                visited.append(cur_vert)

                # Optional exit condition v_end
                if cur_vert is v_end:
                    return visited

            # Push successors in descending numerical vertex order
            for idx in range(self.v_count - 1, -1, -1):
                edge = self.adj_matrix[cur_vert][idx]
                if edge and (idx not in visited):
                    stack.append(idx)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Input: v_start - Index to begin search
               v_end - Optional index to end search
        Output: List of visited nodes
        Descriptions: Returns a list of nodes visited during a breadth-first
                      search from v_start to v_end (if provided
        """
        # Initialize list of visited vertices and a queue
        visited = []
        queue = deque()

        # Exit if v_start does not exist
        if (v_start < 0) or (v_start >= self.v_count):
            return

        # Enqueue v_start to initialize search
        queue.append(v_start)

        # Perform breadth-first search
        while queue:
            # Remove first from queue
            cur_vert = queue.popleft()

            # Add to visited set if not already visited
            if cur_vert not in visited:
                visited.append(cur_vert)

                # Optional exit condition
                if cur_vert is v_end:
                    return visited

            # Queue items in ascending numerical order
            for idx in range(self.v_count):
                edge = self.adj_matrix[cur_vert][idx]
                if edge and (idx not in visited):
                    queue.append(idx)
        return visited

    def has_cycle(self):
        """
        Input: None
        Output: True/False
        Description: Returns True if a cycle exists in the graph
        """
        # Loop through all the vertices
        for vert in range(self.v_count):
            # Look for direct successors of the current vertex
            for idx in range(self.v_count):
                # Perform a depth-first search at the current vertex
                if self.adj_matrix[vert][idx]:
                    search = self.dfs(idx)
                    # If the parent of the successor is found in the search
                    # there is a loop
                    if vert in search:
                        return True
        return False    # No loops found


    def dijkstra(self, src: int) -> []:
        """
        Input: src - Start index
        Output: A list with the path of all visited nodes from the algorithm
        Description: Returns a list of the lowest-cost path from src to each 
                     vertex where result indices are src -> index path weight
        """
        # Initialize priority queue and  for use in algorithm
        pq = []
        min_dists = {}

        # Initialize result as list of infinite distances
        res = [float('inf')] * self.v_count 

        # Return res as is if the src is not in the map
        if (src < 0) or (src >= self.v_count):
            return res

        # Find lowest cost paths from src to each vertex
        dist = 0    
        heapq.heappush(pq, (dist, src))

        # Find shortest path from src to each index
        while pq:
            # Pop lowest priority item from queue
            dist, cur_vert = heapq.heappop(pq)

            if cur_vert not in min_dists:
                min_dists[cur_vert] = dist

                # Add direct successors to priority queue
                for idx in range(self.v_count):
                    d = dist
                    edge = self.adj_matrix[cur_vert][idx]
                    if edge:
                        d += edge
                        heapq.heappush(pq, (d, idx))

        # Fill result array
        for key in min_dists.keys():
            res[key] = min_dists[key]
        return res



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
