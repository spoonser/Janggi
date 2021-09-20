# Author: Spencer Wagner
# Date: 3/10/2021
# Description: A game of Janggi implemented with classes

class JanggiPiece:
    """ Represents a Janggi game piece """
    def __init__(self):



class JanggiGame:
    """ Represents a game of Janggi """
    def __init__(self):
        self._current_player = 'B'
        self._blue_in_check = False
        self._red_in_check = False
        self._game_state = 'UNFINISHED'
        self._board = [['RCh', 'REl', 'RHo', 'RGu', '   ', 'RGu', 'REl', 'RHo', 'RCh'],
                       ['   ', '   ', '   ', '   ', 'RGe', '   ', '   ', '   ', '   '],
                       ['   ', 'RCa', '   ', '   ', '   ', '   ', '   ', 'RCa', '   '],
                       ['RSo', '   ', 'RSo', '   ', 'RSo', '   ', 'RSo', '   ', 'RSo'],
                       ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                       ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                       ['BSo', '   ', 'BSo', '   ', 'BSo', '   ', 'BSo', '   ', 'BSo'],
                       ['   ', 'BCa', '   ', '   ', '   ', '   ', '   ', 'BCa', '   '],
                       ['   ', '   ', '   ', '   ', 'BGe', '   ', '   ', '   ', '   '],
                       ['BCh', 'BEl', 'BHo', 'BGu', '   ', 'BGu', 'BEl', 'BHo', 'BCh']]
        self._board_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
                           '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8,
                           '10': 9}

    def get_game_state(self):
        """ Returns the current state of the game """
        return self._game_state

    def get_current_player(self):
        """ Return whose turn it is """
        return self._current_player

    def is_in_check(self, player):
        """ Returns T/F if the player specified is in check """
        if player == 'blue':
            return self._blue_in_check
        elif player == 'red':
            return self._red_in_check
        else:
            return False

    def print_board(self):
        """ Prints the current game board state to the console """
        print('-'*37)
        for row in self._board:
            print('|' + '|'.join(row) + '|')
            print('-'*37)

    def board_pos_map(self, pos):
        """ Returns the content in the position specified by the user """
        return self._board[self._board_map[pos[1:]]][self._board_map[pos[0]]]

    def make_move(self, start, end):
        """ Takes two positions on the Janggi board as an input and moves the piece in the start
            position to the end position if it is a valid move """
        # grab content in the specified positions and the current player
        p1 = self.board_pos_map(start)
        p2 = self.board_pos_map(end)
        player = self._current_player

        # register a player passing their turn (start string = end string)
        if start == end and player in p1:
            # swap current player
            if player == 'B':
                self._current_player = 'R'
            else:
                self._current_player = 'B'
            return True

        # invalid moves: current player does not choose a starting space with their piece in it,
        # or they have one of their own pieces in the end space
        if player not in p1 or player in p2:
            return False




game = JanggiGame()
game.print_board()
