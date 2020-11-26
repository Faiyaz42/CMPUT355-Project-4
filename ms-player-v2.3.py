####################################
######Authors: Faiyaz Ahmed, Bryland Schoneck, Eden Knechtel, Hannan Ahmed, Kenny Ke
####################################



####################################
# Consulted Sources:
# https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
# https://stackoverflow.com/questions/104420/how-to-generate-all-permutations-of-a-list
# https://luckytoilet.wordpress.com/2012/12/23/2125/
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
# https://stackoverflow.com/questions/52336776/frequency-count-of-a-list-of-lists
####################################



import random
import time
import itertools
import sys
from collections import Counter
import operator

class Minesweeper:

        # Minesweeper Layout
        size = 0
        board = []
        revealed_board = []
        number_mines = 0
        marked_mines = 0
        searched = []

        completed_tiles = []

        impossible_mine_locations = []
        certain_mine_locations = []

        def __init__(self):

                return



        # board layout
        def printBoard(self):

                print("\n")
                cell = "   "
                for i in range(self.size):
                        cell = cell + "     " + str(i + 1)
                print(cell)

                for row in range(self.size):
                        cell = "     "
                        if row == 0:
                                for column in range(self.size):
                                        cell = cell + "______"
                                print(cell)

                        cell = "     "
                        for column in range(self.size):
                                cell = cell + "|     "
                        print(cell + "|")

                        cell = "  " + str(row + 1) + "  "
                        for column in range(self.size):
                                cell = cell + "|  " + str(self.revealed_board[row][column]) + "  "
                        print(cell + "|")

                        cell = "     "
                        for column in range(self.size):
                                cell = cell + "|_____"
                        print(cell + '|')

                print("\n\nNumber of remaining mines: ", (self.number_mines - self.marked_mines))



        # randomizing and planting the mines
        def minePlacer(self):

                i = 0
                while i < self.number_mines:

                        j = random.randint(0, self.size * self.size - 1)
                        column = j % self.size
                        row = j // self.size
                        if self.board[row][column] != -1:     #if no mine, place mine
                                self.board[row][column] = -1
                                i += 1



        # calculating tile values
        def calcTile(self):

                for row in range(self.size):
                        for column in range(self.size):

                                # skip if first one has mine
                                if self.board[row][column] == -1:
                                        continue

                                # up
                                if row > 0 and self.board[row - 1][column] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # down
                                if row < self.size - 1 and self.board[row + 1][column] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # left
                                if column > 0 and self.board[row][column - 1] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # right
                                if column < self.size - 1 and self.board[row][column + 1] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # top-left
                                if row > 0 and column > 0 and self.board[row - 1][column - 1] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # top-right
                                if row > 0 and column < self.size - 1 and self.board[row - 1][column + 1]== -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # below-left
                                if row < self.size - 1 and column > 0 and self.board[row + 1][column - 1] == -1:
                                        self.board[row][column] = self.board[row][column] + 1
                                # below-right
                                if row < self.size - 1 and column < self.size - 1 and self.board[row + 1][column + 1]== -1:
                                        self.board[row][column] = self.board[row][column] + 1



        # recursive call to reveal all hidden neighbours if it is 0
        def revealTile(self, row, column):

                # if not searched
                if [row, column] not in self.searched:

                        # insert in searched list
                        self.searched.append([row, column])

                        # if cell has 0
                        if self.board[row][column] == 0:

                                # reveal
                                self.revealed_board[row][column] = self.board[row][column]

                                # recursion to find neighbours
                                if row > 0:
                                        self.revealTile(row - 1, column)
                                if row < self.size - 1:
                                        self.revealTile(row + 1, column)
                                if column > 0:
                                        self.revealTile(row, column - 1)
                                if column < self.size - 1:
                                        self.revealTile(row, column + 1)
                                if row > 0 and column > 0:
                                        self.revealTile(row - 1, column - 1)
                                if row > 0 and column < self.size - 1:
                                        self.revealTile(row - 1, column + 1)
                                if row < self.size - 1 and column > 0:
                                        self.revealTile(row + 1, column - 1)
                                if row < self.size - 1 and column < self.size - 1:
                                        self.revealTile(row + 1, column + 1)

                        # if not 0
                        elif self.board[row][column] != 0:
                                self.revealed_board[row][column] = self.board[row][column]
        
        
        
        # show mine locations
        def revealMines(self):
        
                for row in range(self.size):
                        for column in range(self.size):
                                if self.board[row][column] == -1:
                                        self.revealed_board[row][column] = '*'
        
        
        
        # check game state
        def gameCheck(self):
        
                # numbered tiles count
                revealed_numbers = 0
        
                #check each cell
                for row in range(self.size):
                        for column in range(self.size):
                                #if revealed and not flagged and not sus
                                if self.revealed_board[row][column] != ' ' and self.revealed_board[row][column] != 'F' and self.revealed_board[row][column] != '?':
                                        revealed_numbers += 1   #increment revealed tiles
        
                # check if all non-mine tiles are found
                if revealed_numbers == self.size * self.size - self.number_mines:
                        return True
                else:
                        return False
        
        
        
        ######################################################
        ####################### PLAYER #######################
        ######################################################
        
        # Logic Calculations: 
        # at beginning of each turn, the player first attempts
        # to calculate logical moves, i.e., moves that are
        # certain to reveal a non-mine tile or mark a mine tile
        # INPUT: row, column: x, y coordinate of a particular tile
        # i.e., we are considering a particular tile and its
        # neighbours
        # RETURN: x, y coordinate (-1, -1) of no logical move can be 
        # made and bool value (True if a flag is to be placed, False otherwise)
        # WHERE: searched is a list of "face-up" tiles and completed_tiles
        # is a list of tiles where all neighbours of tiles have been revealed
        def logic_calc(self, row, column):
        
                # tiles that have been flagged as mines
                flagged_tiles = []
                # tiles that have not been flagged as mines
                unflagged_tiles = []
        
                # for the position [row, column], we are checking
                # the conditions that each neighbour:
                # a) is valid 
                # b) has not already been searched/revealed
                # upon passing these conditions, the neighbour is 
                # either added to flagged_tiles or unflagged_tiles
                # depending on its quality
        
                # check upper neighbour 
                if row > 0 and [row - 1, column] not in self.searched:
                        if self.revealed_board[row - 1][column] == 'F':
                                flagged_tiles.append([row - 1, column])
                        else:
                                unflagged_tiles.append([row - 1, column])
        
                # check lower neighbour
                if row < (self.size - 1)  and [row + 1, column] not in self.searched:
                        if self.revealed_board[row + 1][column] == 'F':
                                flagged_tiles.append([row + 1, column])
                        else:
                                unflagged_tiles.append([row + 1, column])
        
                # check left neighbour
                if column > 0 and [row, column - 1] not in self.searched:
                        if self.revealed_board[row][column - 1] == 'F':
                                flagged_tiles.append([row, column - 1])
                        else:
                                unflagged_tiles.append([row, column - 1])
        
                # check right neighbour
                if column < (self.size - 1) and [row, column + 1] not in self.searched:
                        if self.revealed_board[row][column + 1] == 'F':
                                flagged_tiles.append([row, column + 1])
                        else:
                                unflagged_tiles.append([row, column + 1])
        
                # check upper-left neighbour
                if row > 0 and column > 0 and [row - 1, column - 1] not in self.searched:
                        if self.revealed_board[row - 1][column - 1] == 'F':
                                flagged_tiles.append([row - 1, column - 1])
                        else:
                                unflagged_tiles.append([row - 1, column - 1])
        
                # check upper-right neighbour
                if row > 0 and column < (self.size - 1) and [row - 1, column + 1] not in self.searched:
                        if self.revealed_board[row - 1][column + 1] == 'F':
                                flagged_tiles.append([row - 1, column + 1])
                        else:
                                unflagged_tiles.append([row - 1, column + 1])
        
                # check lower-left neighbour
                if row < (self.size - 1) and column > 0 and [row + 1, column - 1] not in self.searched:
                        if self.revealed_board[row + 1][column - 1] == 'F':
                                flagged_tiles.append([row + 1, column - 1])
                        else:
                                unflagged_tiles.append([row + 1, column - 1])
        
                # check upper-right neighbour
                if row < (self.size - 1) and column < (self.size - 1) and [row + 1, column + 1] not in self.searched:
                        if self.revealed_board[row + 1][column + 1] == 'F':
                                flagged_tiles.append([row + 1, column + 1])
                        else:
                                unflagged_tiles.append([row + 1, column + 1])
        
            # Case 1:
            # if a tile has has same amount of hidden tiles around it as unflagged 
            # mines surrounding it, then all the hidden tiles are mines
            # return: x, y coordinates of first unflagged neighbour as well as
            # True boolean value associated with variable "flag" to indicate
            # the next move is flagging this particular x, y coordinate
                if self.revealed_board[row][column] == (len(unflagged_tiles) + len(flagged_tiles)) and len(unflagged_tiles) > 0:
                        if len(unflagged_tiles) == 1:
                                self.completed_tiles.append([row,column])
                        return unflagged_tiles[0][0], unflagged_tiles[0][1], True
        
            # Case 2:
            # if a tile has the same amount of flags around it as the number 
            # value of the current tile, then all remaining hidden tiles are
            # not mines
            # return: x, y coordinates of first unflagged neighbour as well as
            # False boolean value associated with variable "flag" to indicate
            # the next move is revealing this particular x, y coordinate
                if self.revealed_board[row][column] == len(flagged_tiles) and len(unflagged_tiles) > 0:
                        if len(unflagged_tiles) == 1:
                                self.completed_tiles.append([row,column])
                        return unflagged_tiles[0][0], unflagged_tiles[0][1], False
        
            # Note: if either Case 1 or Case 2 is fulfilled, the current tile is
            # added to a list completed_tiles as all of its neighbours have been 
            # identified, therefore, it no longer needs to be considered for future
            # turns
        
            # if no logical move can be made, coordinates (-1, -1) are returned
                return -1, -1, False
        
        
        
        # Find Sections:
        # 1) divides the board into lists that define its particular sections 
        # 2) calculates all possible configurations of mines on hidden border tiles
        # 3) calculates all legal configurations of mines on hidden border tiles
        # 4) calculates the probability of each hidden tile being a mine
        # RETURNS: What will be played, namely, 
        # a) INT value: the row to be played
        # b) INT value: the column to be played
        # c) BOOL value indicating True: that the tile will be flagged and 
        # False: that the tile will be revealed
        def find_sections(self):
        
                hidden_border_tiles = []
                hidden_exterior_tiles = []
                edge_tiles = []
        
                for row in range(self.size):
                        for column in range(self.size):
                                # find all edge tiles, i.e., revealed tiles that
                                # have unknown neighbours
                                if [row, column] not in self.completed_tiles and [row, column] in self.searched and self.revealed_board[row][column] != 0:
                                        edge_tiles.append([row, column])
                                        # find all hidden tiles that border the
                                        # edge tiles (not including flagged tiles)
                                        # check upper neighbour
                                        if row > 0 and [row - 1, column] not in self.searched:
                                                if self.revealed_board[row - 1][column] != 'F' and [row - 1, column] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row - 1, column])
                                        # check lower neighbour
                                        if row < (self.size - 1)  and [row + 1, column] not in self.searched:
                                                if self.revealed_board[row + 1][column] != 'F' and [row + 1,column] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row + 1, column])
                                        # check left neighbour
                                        if column > 0 and [row, column - 1] not in self.searched:
                                                if self.revealed_board[row][column - 1] != 'F' and [row, column - 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row, column - 1])
                                        # check right neighbour
                                        if column < (self.size - 1) and [row, column + 1] not in self.searched:
                                                if self.revealed_board[row][column + 1] != 'F' and [row, column + 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row, column + 1])
                                        # check upper-left neighbour
                                        if row > 0 and (column > 0) and [row - 1, column - 1] not in self.searched:
                                                if self.revealed_board[row - 1][column - 1] != 'F' and [row - 1, column - 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row - 1, column - 1])
                                        # check upper-right neighbour
                                        if row > 0 and column < (self.size - 1) and [row - 1, column + 1] not in self.searched:
                                                if self.revealed_board[row - 1][column + 1] != 'F' and [row - 1, column + 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row - 1, column + 1])
                                        # check lower-left neighbour
                                        if row < (self.size - 1) and column > 0 and [row + 1, column - 1] not in self.searched:
                                                if self.revealed_board[row + 1][column - 1] != 'F' and [row + 1, column - 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row + 1, column - 1])
                                        # check lower-right neighbour
                                        if row < (self.size - 1) and column < (self.size - 1) and [row + 1, column + 1] not in self.searched:
                                                if self.revealed_board[row + 1][column + 1] != 'F' and [row + 1, column + 1] not in hidden_border_tiles:
                                                        hidden_border_tiles.append([row + 1, column + 1])
        
                # find all non-border hidden tiles
                for row in range(self.size):
                        for column in range(self.size):
                                if [row, column] not in self.searched and [row, column] not in hidden_border_tiles and self.revealed_board[row][column] != 'F':
                                        hidden_exterior_tiles.append([row, column])
        
        
        
                ##################################
                # THIS IS THE PLACE TO SEGRAGATE #
                ##################################
                ### CHANGE VARIABLE NAMES
        
                visited = []
                segment_lst = []        
        
                for row in range(self.size):
                        for column in range(self.size):
                                if [row, column] in hidden_border_tiles and [row, column] not in visited:
        
                                        queue = [[row, column]]
        
                                        edge_temp_lst = []
        
                                        while queue:
        
                                                space = queue.pop(0)   
                                                if space in hidden_border_tiles and space not in visited:
                                                        visited.append(space)
                                                        edge_temp_lst.append(space)
        
                                                        row = space[0]
                                                        column = space[1]
        
                                                        # up
                                                        if row > 0 and [row - 1, column] not in visited and [row - 1, column] in hidden_border_tiles:
                                                                queue.append([row - 1, column])
        
                                                        # down
                                                        if row < self.size - 1  and [row + 1, column] not in visited and [row + 1, column] in hidden_border_tiles:
                                                                queue.append([row + 1, column])                            
        
                                                        # left
                                                        if column > 0 and [row, column - 1] not in visited and [row, column - 1] in hidden_border_tiles:
                                                                queue.append([row, column - 1])
        
                                                        # right
                                                        if column < self.size - 1 and [row, column + 1] not in visited and [row, column + 1] in hidden_border_tiles:
                                                                queue.append([row, column + 1])
        
                                                        # top-left
                                                        if row > 0 and column > 0 and [row - 1, column - 1] not in visited and [row - 1, column - 1] in hidden_border_tiles:
                                                                queue.append([row - 1, column - 1])
        
                                                        # top-right
                                                        if row > 0 and column < self.size - 1 and [row - 1, column + 1] not in visited and [row - 1, column + 1] in hidden_border_tiles:
                                                                queue.append([row - 1, column + 1])
        
                                                        # below-left
                                                        if row < self.size - 1 and column > 0 and [row + 1, column - 1] not in visited and [row + 1, column - 1] in hidden_border_tiles:
                                                                queue.append([row + 1, column - 1])
        
                                                        # below-right
                                                        if row < self.size-1 and column < self.size -1 and [row+1,column +1] not in visited and [row+1,column+1] in hidden_border_tiles:
                                                                queue.append([row+1,column+1])                        
        
                                        segment_lst.append(edge_temp_lst)
        
        
        
                ####################################
                # CHECK LEGAL #
                ####################################
                # for each configuration, for each edge tile, increases mine count if 
                # a) its hidden neighbour is marked as a mine or 
                # b) its hidden neighbour belongs to the possible configuration of mine placement
                # if the revealed board value of the tile is equal to the mine count,
                # it is a legal configuration and appended to a list 
        
                # WHERE: mine_config is a list of configurations for a particular range
                # and all_possible_mine_config is a complete list of all possible
                # mine configurations per segment, and num_combo_lst is number of combinations per segment
        
                legal_configurations = []
                num_combo_lst = []
        
                for tiles in segment_lst:
                        hidden_temp_lst = []
                        edge_temp_lst = []
                        instance = 0
                        for tile in tiles:
                                if tile in hidden_border_tiles:
                                        hidden_temp_lst.append(tile)
                                else:
                                        edge_temp_lst.append(tile)
        
                        for j in range(1, len(hidden_temp_lst) + 1):
                                mine_config = list(itertools.combinations(hidden_temp_lst, j))
                                for combo in mine_config:
                                        legal = True
                                        for tile in edge_temp_lst:
                                                        row = tile[0]
                                                        column = tile[1]
                                                        count = 0
                                                        # up
                                                        if row > 0 and [row - 1, column] not in self.searched:
                                                                if self.revealed_board[row - 1][column] == 'F' or [row - 1, column] in combo:
                                                                        count += 1
                                                        # down
                                                        if row < self.size - 1 and [row + 1, column] not in self.searched:
                                                                if self.revealed_board[row + 1][column] == 'F' or [row + 1, column] in combo:
                                                                        count += 1
                                                        # left
                                                        if column > 0 and [row, column - 1] not in self.searched:
                                                                if self.revealed_board[row][column - 1] == 'F' or [row, column - 1] in combo:
                                                                        count += 1
                                                        # right
                                                        if column < self.size - 1 and [row, column + 1] not in self.searched:
                                                                if self.revealed_board[row][column + 1] == 'F' or [row, column + 1] in combo:
                                                                        count += 1
                                                        # top-left
                                                        if row > 0 and column > 0 and [row - 1, column - 1] not in self.searched:
                                                                if self.revealed_board[row - 1][column - 1] == 'F' or [row - 1, column - 1] in combo:
                                                                        count += 1
                                                        # top-right
                                                        if row > 0 and column < self.size - 1 and [row - 1, column + 1] not in self.searched:
                                                                if self.revealed_board[row - 1][column + 1] == 'F' or [row - 1, column + 1] in combo:
                                                                        count += 1
                                                        # below-left
                                                        if row < self.size - 1 and column > 0 and [row + 1, column - 1] not in self.searched:
                                                                if self.revealed_board[row + 1][column - 1] == 'F' or [row + 1, column - 1] in combo:
                                                                        count += 1
                                                        # below-right
                                                        if row < self.size - 1 and column < self.size - 1 and [row + 1, column + 1] not in self.searched:
                                                                if self.revealed_board[row + 1][column + 1] == 'F' or [row + 1, column + 1] in combo:
                                                                        count += 1
        
                                                        # check if tile is legal
                                                        if self.revealed_board[row][column] != count or len(combo) > (self.number_mines - self.marked_mines):
                                                                legal = False
                                                                break
        
                                        if legal:
                                                instance += 1
                                                legal_configurations.append(combo) 
        
                        num_combo_lst.append(instance)
        
        
        
                ####################################
                # COUNT BOMBS #
                ####################################
        
                possible_mine_locations = []
        
                # from every legal configuration, create a list of positions
                # where the mine(s) could possibly be
        
                for configuration in legal_configurations:
                        for tile in configuration:
                                possible_mine_locations.append(tile)
        
                # make list of hidden border tiles that NEVER appear in 
                # possible mine locations
                for tile in hidden_border_tiles:
                        if tile not in possible_mine_locations:
                                self.impossible_mine_locations.append(tile)
        
                # make list of hidden border tiles that ALWAYS appear in 
                # possible mine locations
                for tile in hidden_border_tiles:
                        in_every_config = True
                        for configuration in legal_configurations:
                                if tile not in configuration:
                                        in_every_config = False
                        if in_every_config == True:
                                self.certain_mine_locations.append(tile)
        
                ## NEED if certain if impossible returns/pops
                if self.certain_mine_locations:
                        tile = self.certain_mine_locations.pop(0)
                        return tile[0], tile[1], True
        
                if self.impossible_mine_locations:
                        tile = self.impossible_mine_locations.pop(0)
                        return tile[0], tile[1], False 
        
                # if all hidden border tiles have the potential to be a mine 
                # then sort by lowest chance. Dictionary counts and sorts
                # by repetition
                # Counter() creates values like ([x, y], s) where s is the 
                # number of times the tile [x, y] appeared in possible_mine_locations
                possible_mine_locations = []
        
                for configuration in legal_configurations:
                        for tile in configuration:
                                tile = tuple(tile)
                                possible_mine_locations.append(tile)
                mine_dict = Counter(possible_mine_locations)
                possible_mine_locations = sorted(mine_dict.items(), key = lambda tileCount: tileCount[1])
        
                # if no potential mine placements can be discerned, a random
                # hidden border tile is played 
                # otherwise, the tile with the lowest likelihood of being a 
                # mine is calculated: safest_tile/ safest_tile_percent
                count = 0
                num_combo = 1
        
                if len(possible_mine_locations) > 0:
                        safest_tile = possible_mine_locations[0][0]
                        for seg in segment_lst: 
                                if safest_tile not in seg:
                                        count += 1
                                else:
                                        num_combo = num_combo_lst[count]
                                        continue
                        safest_tile_percent = possible_mine_locations[0][1] / num_combo
                else:
                        n = random.randint(0, len(hidden_border_tiles) - 1)
                        return hidden_border_tiles[n][0], hidden_border_tiles[n][1], False
        
                ####################################
                # NON BORDER BOMB ODDS #
                ####################################
        
                base_prob = ((self.number_mines - self.marked_mines) / (len(hidden_border_tiles) + len(hidden_exterior_tiles)))
        
                # the lowest probability tile is played from potential mines
                if safest_tile_percent <= base_prob:
                        return safest_tile[0], safest_tile[1], False
        
                # if the likelihood of the best tile being a mine is greater than 
                # that of the base probability, a random exeterior tile is played
                if len(hidden_exterior_tiles) > 0:
                        n = random.randint(0, len(hidden_exterior_tiles) - 1)
                        return hidden_exterior_tiles[n][0], hidden_exterior_tiles[n][1], False
                else:
                        return safest_tile[0], safest_tile[1], False
        
        
        
        # includes instructions for first randomized move. After first move,
        # first checks if a logical move can be made, then moves on to call
        # find_sections() which returns a probable move
        # INPUT: firstmove (BOOL)
        # RETURN: move_row (INT) x value of next move, move_column (INT) y 
        # value of next move and, flag (BOOL) indicates whether a tile will
        # be flagged (True) or revealed (False)
        def find_move(self, firstmove):
        
                # first move, player simply selects a random tile
                if firstmove:
                        j = random.randint(0, self.size * self.size - 1)
                        column = j % self.size
                        row = j // self.size
                        return row, column, False
        
                # player first checks if it can make a logical move
                # if return value of logic_calc() is -1, no logical move
                # can be made, and player instead moves on to make probable move
                for row in range(self.size):
                        for column in range(self.size):
                                if [row, column] not in self.completed_tiles and [row, column] in self.searched and self.revealed_board[row][column] != 0:
                                        move_row, move_column, flag = self.logic_calc(row, column)
                                        if move_row != -1:
                                                return move_row, move_column, flag
        
                #find_sections() calculates probable move
                move_row, move_column, flag = self.find_sections()
                return move_row, move_column, flag





if __name__ == "__main__":

        minesweeper = Minesweeper()

        # instructions and board setup inputs
        welcome = "Welcome to Minesweeper Solver"
        print (welcome.rjust(50, ' ' ))

        keepPlaying = True
        firstmove = True
        replays = 0
        Times = []
        winTimes = []
        lossTimes = []
        Won = 0
        Lost = 0

        # game
        while keepPlaying and replays > -1:

                # initiating board if it is the first move of play
                if firstmove:
                        integer_input1 = False
                        while not integer_input1 and replays == 0:
                                try:
                                        minesweeper.size = int(input("\nEnter size of board: "))
                                        minesweeper.number_mines = int(input("\nEnter number of mines: "))
                                        integer_input1 = True
                                except ValueError:
                                        print("\nPlease enter size and number of mines in integers only!")
                                        continue
                        integer_input2 = False
                        while not integer_input2 and replays == 0:
                                try:
                                        replays = int(input("\nEnter number of games to be played: "))
                                        integer_input2 = True
                                except ValueError:
                                        print("\nPlease enter size and number of mines in integers only!")
                                        continue

                        # set number of marked mines
                        minesweeper.marked_mines = 0

                        # initiating the board
                        minesweeper.board = [[0 for y in range(minesweeper.size)] for x in range(minesweeper.size)]
                        # initiating array for mines
                        minesweeper.revealed_board = [[' ' for y in range(minesweeper.size)] for x in range(minesweeper.size)]

                        # flagged tiles
                        flags = []

                        #question mark suspected tiles
                        questionMark = []

                        # reset completed_tiles
                        minesweeper.completed_tiles = []

                        # plant mines
                        minesweeper.minePlacer()

                        # tile values
                        minesweeper.calcTile()

                        # timer start
                        start = time.time()

                        # finished first move
                        # firstmove = False

                minesweeper.printBoard()

                # Input from Player
                if not minesweeper.certain_mine_locations and not minesweeper.impossible_mine_locations:
                        row, column, flag = minesweeper.find_move(firstmove)
                        print("({}, {})".format(row, column))
                        firstmove = False

                else:
                        if minesweeper.certain_mine_locations:
                                tile = minesweeper.certain_mine_locations.pop(0)
                                row = tile[0]
                                column = tile[1]
                                flag = True
                        else: 
                                tile = minesweeper.impossible_mine_locations.pop(0)
                                row = tile[0]
                                column = tile[1]
                                flag = False

                if flag:
                        flags.append([row, column])
                        minesweeper.revealed_board[row][column] = 'F'
                        minesweeper.marked_mines += 1
                        continue

                gamecheck = True
                # if stepped on mine, game over
                if minesweeper.board[row][column] == -1:
                        gamecheck = False

                        minesweeper.revealed_board[row][column] = '*'
                        minesweeper.revealMines()
                        minesweeper.printBoard()

                        # end timer
                        end = time.time()

                        # print(end - start) #exact time in floating point
                        Times.append(end - start)
                        lossTimes.append(end - start)
                        Lost += 1
                        print("\nGame over.Stepped on a mine!!!")
                        print("\nTimespent = %.5f second(s)\n" %round(end - start,5))
                        

                        # check if reset
                        replays -= 1

                        # if no , quit game
                        if replays == 0:
                                keepPlaying = False
                                firstmove = False
                                minesweeper.board.clear()
                                minesweeper.revealed_board.clear()
                                minesweeper.completed_tiles.clear()                                
                                minesweeper.size = 0
                                minesweeper.number_mines = 0
                                minesweeper.marked_mines = 0

                        else:
                                keepPlaying = True

                        # reset and firstmove to reinitiate board
                        minesweeper.searched.clear()
                        flags.clear()
                        questionMark.clear()
                        firstmove = True

                # no mines in neighbouring cells, reveal neighbours
                elif minesweeper.board[row][column] == 0:
                        minesweeper.revealed_board[row][column] = '0'
                        # searched = []
                        minesweeper.revealTile(row, column)

                # if there is a mine in neighbouring cells
                else:
                        minesweeper.searched.append([row,column])
                        minesweeper.revealed_board[row][column] = minesweeper.board[row][column]

                # check game state
                if minesweeper.gameCheck() and gamecheck == True:

                        minesweeper.revealMines()
                        minesweeper.printBoard()

                        # end timer
                        end = time.time()

                        # print(end - start) , exact time in floating point
                        Times.append(end - start)
                        winTimes.append(end - start)
                        Won += 1                        
                        print("\nCongratulations.You won!!!")
                        print("\nTimespent = %.5f second(s)\n" %round(end - start,5))
                        

                        # check if reset
                        replays -= 1

                        # if no quit game
                        if replays == 0:
                                keepPlaying = False
                                firstmove = False
                                minesweeper.board.clear()
                                minesweeper.revealed_board.clear()
                                minesweeper.completed_tiles.clear()
                                minesweeper.size = 0
                                minesweeper.number_mines = 0
                                minesweeper.marked_mines = 0

                        else:
                                keepPlaying = True

                        # reset and firstmove to reinitiate board
                        minesweeper.searched.clear()
                        flags.clear()
                        questionMark.clear()
                        firstmove = True
                        
        print("\n\nRun Statistics:")
        print("\nTotal time = %.5f second(s)" %sum(Times))
        print("\nBest run time = %.5f second(s)" %min(Times))
        if winTimes:
                print("\nBest win time = %.5f second(s)" %min(winTimes))
        if lossTimes:
                print("\nBest loss time = %.5f second(s)" %min(lossTimes))
        print("\nTotal games played = %d" %(Won+Lost))
        print("\nGames won = %d" %(Won))
        print("\nGames lost = %d" %(Lost))
        print("\nPercentage of wins = %.2f" %round(Won / (Won+Lost) * 100, 2))
        
