# Course: CS261 - Data Structures 
# Author: Spencer Wagner
# Assignment: 6
# Description: Undirected graph implementation

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        # If the vertex is not present in graph, init with empty list as val
        if v not in self.adj_list:
            self.adj_list[v] = []  
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # Do nothing if u is v
        if u is v:
            return 

        # If u or v are not in the graph, add them
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)
        
        # Add the other vertex to the list of adjacent vertices for each input
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # Do nothing if either vertices or the edge does not exist
        if (u not in self.adj_list or v not in self.adj_list
            or v not in self.adj_list[u]):
            return 

        # Delete the edge from both vertices
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # Do nothing if vertex does not exist
        if v not in self.adj_list:
            return
        
        # Delete v from teh adjacency lists of the connected edges 
        for idx in range(len(self.adj_list[v])):
            self.adj_list[self.adj_list[v][idx]].remove(v)

        # Delete v from the main data structure
        del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list.keys())
       

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        res = []

        # Loop through each of the vertices' edge list and add the tuple
        # of the key and edge to the result list
        for key in self.adj_list:
            # Loops through list of edge for current key
            for idx in range(len(self.adj_list[key])):
                # Add if tuple (in either order) does not exist in res
                if ((key, self.adj_list[key][idx]) not in res
                     and (self.adj_list[key][idx], key) not in res):
                    res.append((key, self.adj_list[key][idx]))
        
        return res
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # Input of only one vertex in path
        if len(path) == 1:
            if path[0] not in self.adj_list:
                return False

        # Loop through the input and check if an edge connecting each key
        # in the path order exists in that edge list
        for idx in range(len(path) - 1):
            cur_key = path[idx]
            next_key = path[idx + 1] 
            
            # Key does not exist, path cannot be completed
            if cur_key not in self.adj_list:
                return False

            # Edge does not exist
            if next_key not in self.adj_list[cur_key]:
                return False

        # Path successfully traversed
        return True 

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        # Initialize set of vertices visited and a stack
        visited = []
        stack = []   

        # If start vertex not in graph, exit method
        if v_start not in self.adj_list:
            return visited

        # Push starting vertex to stack to begin depth-first search
        stack.append(v_start)

        # While the stack is not empty
        while stack:
            # Pop the top of the stack
            cur_vert = stack.pop()
            
            # If that vertex has not been visited, append its succesors to stack 
            if cur_vert not in visited:
                visited.append(cur_vert)

                # Optional exit condition v_end
                if cur_vert is v_end:
                    return visited
            
            # Push next nodes to visit in descending lexographical order
            # Sorted adjacent vertex list
            self.adj_list[cur_vert].sort()
            self.adj_list[cur_vert].reverse() # Stack push order

            # Push to stack if node not visited
            for vert in self.adj_list[cur_vert]:
                if vert not in visited:
                    stack.append(vert)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        # Initialize list of visited vertices and a queue
        visited = []
        queue = deque() 

        # Exit if v_start does not exist
        if v_start not in self.adj_list:
            return visited

        # Enqueue v_start to initialize search
        queue.append(v_start)

        while queue:
            # Remove value from visited
            cur_vert = queue.popleft()

            if cur_vert not in visited:
                visited.append(cur_vert)

                # Optional early exit condition
                if cur_vert is v_end:
                    return visited

            # Queue items in ascending lexographical order
            # Sort the adjacent vertex list of current vertex
            self.adj_list[cur_vert].sort()

            for vert in self.adj_list[cur_vert]:
                if vert not in visited:
                    queue.append(vert)

        return visited

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        # Grab keys of adj list and initialize a count and visited node list
        keys = self.get_vertices()
        visited = []
        count = 0
        
        # Loop through the vertices and perform a search to determine
        # the components connected to it
        for key in keys:
            # If a vertex has not been visited via the search, perform another
            # search on that vertex to determine its connected components
            if key not in visited:
                visited.extend(self.dfs(key))
                count += 1  # New dfs = a new section of connected components

        return count
        

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        # Depth-first search that detects a cycle
        def dfs_helper(key, visited, stack): 
            # Unvisited node accessed via dfs_helper has no parent
            stack.append((key, None))
            visited.append(key)

            # Perform a dfs while marking the parents and visited nodes
            while stack:
                # Dequeue front node and its parent
                cur_vert, par = stack.pop()

                # Search for successor nodes
                for successor in self.adj_list[cur_vert]:
                    # Add successor to visited 
                    if successor not in visited:
                        visited.append(successor)

                        # Queue the node and list its parent
                        stack.append((successor, cur_vert))

                    # If that node has already been found and it isn't the parent
                    # of the current node, then a cycle has been found
                    elif successor is not par:
                        return True

        # Initialize list of visited vertices and a queue
        visited = []
        stack = []
        keys = self.get_vertices()

        # Loop through keys and call dfs_helper if the node hasn't been found
        # (detects subgraphs)
        for key in keys:
            if key not in visited:
                cycle_found = dfs_helper(key, visited, stack)
            
            if cycle_found:
                return True

        return False  # Search completed with no cycles found

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
