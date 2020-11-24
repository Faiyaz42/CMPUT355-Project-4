####################################
######author:Faiyaz Ahmed
####################################


####################################
# Sources:
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

# Minesweeper Layout
size = 0
board = []
revealed_board=[]
number_mines = 0
marked_mines = 0
searched = []

completed_tiles = []


#board layout
def printBoard():

        print("\n")
        cell = "   "
        for i in range(size):
                cell = cell + "     " + str(i + 1)
        print(cell)

        for row in range(size):
                cell = "     "
                if row == 0:
                        for column in range(size):
                                cell = cell + "______"
                        print(cell)

                cell = "     "
                for column in range(size):
                        cell = cell + "|     "
                print(cell + "|")

                cell = "  " + str(row + 1) + "  "



                for column in range(size):


                        cell = cell + "|  " + str(revealed_board[row][column]) + "  "
                print(cell + "|")

                cell = "     "


                for column in range(size):
                        cell = cell + "|_____"
                print(cell + '|')

        print("\n\n Number of remaining mines: ", (number_mines - marked_mines))





# randomizing and planting the mines
def minePlacer():



        i = 0
        while i < number_mines:

                j = random.randint(0, size*size-1)
                column = j % size
                row = j // size
                if board[row][column] != -1:      #if no mine,place mine
                        board[row][column] = -1

                        i += 1




# calculating tile values
def calcTile():



        for row in range(size):
                for column in range(size):

                        # skip if first one has mine
                        if board[row][column] == -1:
                                continue

                        # up
                        if row > 0 and board[row-1][column] == -1:
                                board[row][column] = board[row][column] + 1
                        # down
                        if row < size-1  and board[row + 1][column] == -1:
                                board[row][column] = board[row][column]+ 1
                        # left
                        if column > 0 and board[row][column -1] == -1:
                                board[row][column] = board[row][column] + 1
                        # right
                        if column < size-1 and board[row][column +1] == -1:
                                board[row][column] = board[row][column]+ 1
                        # top-left
                        if row > 0 and column > 0 and board[row-1][column -1] == -1:
                                board[row][column] = board[row][column]+ 1
                        # top-right
                        if row > 0 and column < size-1 and board[row-1][column+1]== -1:
                                board[row][column] = board[row][column]+ 1
                        # below-left
                        if row < size -1 and column > 0 and board[row+1][column-1] == -1:
                                board[row][column] = board[row][column]+ 1
                        # below-right
                        if row < size-1 and column < size -1 and board[row+1][column +1]== -1:
                                board[row][column] = board[row][column]+ 1




# recursive call to reveal all hidden neighbours if it is 0
def revealTile(row, column):


        # if not searched
        if [row,column] not in searched:

                # insert in searched list
                searched.append([row,column])

                # if cell has 0
                if board[row][column] == 0:

                        # reveal
                        revealed_board[row][column] = board[row][column]

                        # recursion to find neighbours
                        if row > 0:
                                revealTile(row-1, column)
                        if row < size-1:
                                revealTile(row+1, column)
                        if column > 0:
                                revealTile(row, column-1)
                        if column < size-1:
                                revealTile(row, column+1)
                        if row > 0 and column > 0:
                                revealTile(row-1, column-1)
                        if row > 0 and column < size-1:
                                revealTile(row-1, column+1)
                        if row < size-1 and column > 0:
                                revealTile(row +1, column-1)
                        if row < size-1 and column < size -1:
                                revealTile(row +1, column  +1)

                # if not 0
                elif board[row][column] != 0:
                        revealed_board[row][column] = board[row][column]



# show mine locations
def revealMines():
        for row in range(size):
                for column in range(size):

                        if board[row][column] == -1:
                                revealed_board[row][column] = '*'





# check game state
def gameCheck():


        # numbered tiles count
        revealed_numbers = 0

        #check each cell
        for row in range(size):
                for column in range(size):
                        #if revealed and not flagged and not sus
                        if revealed_board[row][column] != ' ' and revealed_board[row][column] != 'F' and revealed_board[row][column] != '?':
                                revealed_numbers += 1   #increment revealed tiles

        # check if all non-mine tiles are found
        if revealed_numbers == size * size - number_mines:
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
def logic_calc(row, column):
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
        if row > 0 and [row - 1, column] not in searched:
                if revealed_board[row - 1][column] == 'F':
                        flagged_tiles.append([row - 1, column])
                else:
                        unflagged_tiles.append([row - 1, column])
        # check lower neighbour
        if row < (size - 1)  and [row + 1, column] not in searched:
                if revealed_board[row + 1][column] == 'F':
                        flagged_tiles.append([row + 1, column])
                else:
                        unflagged_tiles.append([row + 1, column])
        # check left neighbour
        if column > 0 and [row, column - 1] not in searched:
                if revealed_board[row][column - 1] == 'F':
                        flagged_tiles.append([row, column - 1])
                else:
                        unflagged_tiles.append([row, column - 1])
        # check right neighbour
        if column < (size - 1) and [row, column + 1] not in searched:
                if revealed_board[row][column + 1] == 'F':
                        flagged_tiles.append([row, column + 1])
                else:
                        unflagged_tiles.append([row, column + 1])
        # check upper-left neighbour
        if row > 0 and column > 0 and [row-1, column - 1] not in searched:
                if revealed_board[row - 1][column - 1] == 'F':
                        flagged_tiles.append([row - 1, column - 1])
                else:
                        unflagged_tiles.append([row - 1, column - 1])
        # check upper-right neighbour
        if row > 0 and column < (size - 1) and [row - 1, column + 1] not in searched:
                if revealed_board[row - 1][column + 1] == 'F':
                        flagged_tiles.append([row - 1, column + 1])
                else:
                        unflagged_tiles.append([row - 1, column + 1])
        # check lower-left neighbour
        if row < (size - 1) and column > 0 and [row + 1, column - 1] not in searched:
                if revealed_board[row + 1][column - 1] == 'F':
                        flagged_tiles.append([row + 1, column - 1])
                else:
                        unflagged_tiles.append([row + 1, column - 1])
        # check upper-right neighbour
        if row < (size - 1) and column < (size - 1) and [row + 1, column + 1] not in searched:
                if revealed_board[row + 1][column + 1] == 'F':
                        flagged_tiles.append([row + 1, column + 1])
                else:
                        unflagged_tiles.append([row + 1, column + 1])

    # Case 1:
    # if a tile has has same amount of hidden tiles around it as unflagged 
    # mines surrounding it, then all the hidden tiles are mines
    # return: x, y coordinates of first unflagged neighbour as well as
    # True boolean value associated with variable "flag" to indicate
    # the next move is flagging this particular x, y coordinate
        if revealed_board[row][column] == (len(unflagged_tiles) + len(flagged_tiles)) and len(unflagged_tiles) > 0:
                if len(unflagged_tiles) == 1:
                        completed_tiles.append([row,column])
                return unflagged_tiles[0][0], unflagged_tiles[0][1], True


    # Case 2:
    # if a tile has the same amount of flags around it as the number 
    # value of the current tile, then all remaining hidden tiles are
    # not mines
    # return: x, y coordinates of first unflagged neighbour as well as
    # False boolean value associated with variable "flag" to indicate
    # the next move is revealing this particular x, y coordinate
        if revealed_board[row][column] == len(flagged_tiles) and len(unflagged_tiles) > 0:
                if len(unflagged_tiles) == 1:
                        completed_tiles.append([row,column])
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
def find_sections():

        hidden_border_tiles = []
        hidden_exterior_tiles = []
        edge_tiles = []

        for row in range(size):
                for column in range(size):
                        # find all edge tiles, i.e., revealed tiles that
                        # have unknown neighbours
                        if [row, column] not in completed_tiles and [row, column] in searched and revealed_board[row][column] != 0:
                                edge_tiles.append([row, column])
                                # find all hidden tiles that border the
                                # edge tiles (not including flagged tiles)
                                # check upper neighbour
                                if row > 0 and [row - 1, column] not in searched:
                                        if revealed_board[row - 1][column] != 'F' and [row - 1, column] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row - 1, column])
                                # check lower neighbour
                                if row < (size - 1)  and [row + 1, column] not in searched:
                                        if revealed_board[row + 1][column] != 'F' and [row + 1,column] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row + 1, column])
                                # check left neighbour
                                if column > 0 and [row, column - 1] not in searched:
                                        if revealed_board[row][column - 1] != 'F' and [row, column - 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row, column - 1])
                                # check right neighbour
                                if column < (size - 1) and [row, column + 1] not in searched:
                                        if revealed_board[row][column + 1] != 'F' and [row, column + 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row, column + 1])
                                # check upper-left neighbour
                                if row > 0 and (column > 0) and [row - 1, column - 1] not in searched:
                                        if revealed_board[row - 1][column - 1] != 'F' and [row - 1, column - 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row - 1, column - 1])
                                # check upper-right neighbour
                                if row > 0 and column < (size - 1) and [row - 1, column + 1] not in searched:
                                        if revealed_board[row - 1][column + 1] != 'F' and [row - 1, column + 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row - 1, column + 1])
                                # check lower-left neighbour
                                if row < (size - 1) and column > 0 and [row + 1, column - 1] not in searched:
                                        if revealed_board[row + 1][column - 1] != 'F' and [row + 1, column - 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row + 1, column - 1])
                                # check lower-right neighbour
                                if row < (size - 1) and column < (size - 1) and [row + 1, column + 1] not in searched:
                                        if revealed_board[row + 1][column + 1] != 'F' and [row + 1, column + 1] not in hidden_border_tiles:
                                                hidden_border_tiles.append([row + 1, column + 1])

        # find all non-border hidden tiles
        for row in range(size):
                for column in range(size):
                        if [row, column] not in searched and [row, column] not in hidden_border_tiles and revealed_board[row][column] != 'F':
                                hidden_exterior_tiles.append([row, column])


        ##################################
        # THIS IS THE PLACE TO SEGRAGATE #
        ##################################
        
        # calculates the high end of mines that may be surrounding
        # the edge tiles before generating all possible configurations
        # of mines on the hidden border tiles (ranging from all configurations
        # of one mine to all configurations of maximum_mines)
        # WHERE: mine_config is a list of configurations for a particular range
        # and all_possible_mine_config is a complete list of all possible
        # mine configurations
        maximum_mines = 0

        for n in edge_tiles:
            maximum_mines += revealed_board[n[0]][n[1]]

        all_possible_mine_config = []

        for n in range(1, (maximum_mines + 1)):
                mine_config = list(itertools.combinations(hidden_border_tiles, n))
                
                for i in mine_config:
                        all_possible_mine_config.append(i)


        ####################################
        # CHECK LEGAL #
        ####################################
        # for each configuration, for each edge tile, increases mine count if 
        # a) its hidden neighbour is marked as a mine or 
        # b) its hidden neighbour belongs to the possible configuration of mine placement
        # if the revealed board value of the tile is equal to the mine count,
        # it is a legal configuration and appended to a list 

        legal_configurations = []

        for configuration in all_possible_mine_config:
                legal = True
                for tile in edge_tiles:
                        row = tile[0]
                        column = tile[1]
                        count = 0
                        # check upper neighbour
                        if row > 0 and [row - 1, column] not in searched:
                                if revealed_board[row - 1][column] == 'F' or [row - 1, column] in configuration:
                                        count += 1
                        # check lower neighbour
                        if row < (size - 1)  and [row + 1, column] not in searched:
                                if revealed_board[row + 1][column] == 'F' or [row + 1, column] in configuration:
                                        count += 1
                        # check left neighbour
                        if column > 0 and [row, column - 1] not in searched:
                                if revealed_board[row][column - 1] == 'F' or [row, column - 1] in configuration:
                                        count += 1
                        # check right neighbour
                        if column < (size - 1) and [row, column + 1] not in searched:
                                if revealed_board[row][column + 1] == 'F' or [row, column + 1] in configuration:
                                        count += 1
                        # check upper-left neighbour
                        if row > 0 and column > 0 and [row - 1, column - 1] not in searched:
                                if revealed_board[row - 1][column - 1] == 'F' or [row - 1, column - 1] in configuration:
                                        count += 1
                        # check upper-right neighbour
                        if row > 0 and column < (size - 1) and [row - 1, column + 1] not in searched:
                                if revealed_board[row - 1][column + 1] == 'F' or [row - 1, column + 1] in configuration:
                                        count += 1
                        # check lower-left neighbour
                        if row < (size - 1) and column > 0 and [row + 1, column - 1] not in searched:
                                if revealed_board[row + 1][column - 1] == 'F' or [row + 1, column - 1] in configuration:
                                        count += 1
                        # check lower-right neighbour
                        if row < (size - 1) and column < (size - 1) and [row + 1, column + 1] not in searched:
                                if revealed_board[row + 1][column + 1] == 'F' or [row + 1, column + 1] in configuration:
                                        count += 1

                        # check if tile is legal
                        if revealed_board[row][column] != count or len(configuration) > (number_mines - marked_mines):
                                legal = False
                                break

                if legal:
                        legal_configurations.append(configuration)

        ####################################
        # COUNT BOMBS #
        ####################################

        possible_mine_locations = []

        # from every legal configuration, create a list of positions
        # where the mine(s) could possibly be

        for configuration in legal_configurations:
                for tile in configuration:
                    possible_mine_locations.append(tile)

        # if any hidden border tiles have no chance of being a mine,
        # play that move
        for tile in hidden_border_tiles:
            if tile not in possible_mine_locations:
                return tile[0], tile[1], False

        # if all hidden border tiles have the potential to be a mine 
        # then sort by lowest chance. Dictionary counts and sorts
        # by repetition
        possible_mine_locations = []

        for configuration in legal_configurations:
                for tile in configuration:
                        tile = tuple(tile)
                        possible_mine_locations.append(tile)
        mine_dict = Counter(possible_mine_locations)
        possible_mine_locations = sorted(mine_dict.items(), key=lambda kv: kv[1])

        # if no potential mine placements can be discerned, a random
        # hidden border tile is played
        if len(possible_mine_locations) > 0:
                best_tile = possible_mine_locations[0][0]
                best_tile_percent = possible_mine_locations[0][1] / len(legal_configurations)
        else:
                n = random.randint(0, len(hidden_border_tiles) - 1)
                return hidden_border_tiles[n][0], hidden_border_tiles[n][1], False

        ####################################
        # NON BORDER BOMB ODDS #
        ####################################

        base_prob = ((number_mines - marked_mines) / (len(hidden_border_tiles) + len(hidden_exterior_tiles)))

        # the lowest probability tile is played from potential mines
        if best_tile_percent <= base_prob:
                return best_tile[0], best_tile[1], False

        # if the likelihood of the best tile being a mine is greater than 
        # that of the base probability, a random exeterior tile is played
        n = random.randint(0, len(hidden_exterior_tiles) - 1)
        return hidden_exterior_tiles[n][0], hidden_exterior_tiles[n][1], False






def find_move(firstmove):

        if firstmove:
                j = random.randint(0, size*size-1)
                column = j % size
                row = j // size
                return row, column, False

        for row in range(size):
                for column in range(size):
                    if [row, column] not in completed_tiles and [row, column] in searched and revealed_board[row][column] != 0:
                        move_row, move_column, flag = logic_calc(row, column)
                        if move_row != -1:
                            print("logic")
                            print(completed_tiles)
                            return move_row, move_column, flag

        move_row, move_column, flag = find_sections()
        print("prob")
        return move_row, move_column, flag






if __name__ == "__main__":

        # instructions and board setup inputs
        welcome = "Welcome to Minesweeper"
        print (welcome.rjust(50, ' ' ))
 
        play = True
        firstmove = True

        #game
        while play:

                # initiating board if it is the first move of play
                if firstmove:
                        integer = False
                        while integer == False:
                                try:
                                        size = int(input("\nEnter size of board: "))
                                        number_mines = int(input("\nEnter number of mines: "))
                                        integer = True
                                except ValueError:
                                        print("\nPlease enter size and number of mines in integers only!")
                                        continue

                        # set number of marked mines
                        marked_mines = 0

                        # initiating the board
                        board = [[0 for y in range(size)] for x in range(size)]
                        # initiating array for mines
                        revealed_board = [[' ' for y in range(size)] for x in range(size)]

                        # flagged tiles
                        flags = []

                        #question mark suspected tiles
                        questionMark = []

                        # reset completed_tiles
                        completed_tiles = []

                        # plant mines
                        minePlacer()

                        # tile values
                        calcTile()

                        # timer start
                        start = time.time()

                        # finished first move
                        #firstmove = False


                printBoard()

                # Input from Player

                row, column, flag = find_move(firstmove)
                print("({}, {})".format(row, column))
                firstmove = False

                if flag:
                        flags.append([row, column])
                        revealed_board[row][column] = 'F'
                        marked_mines += 1
                        continue

                # if stepped on mine, game over
                if board[row][column] == -1:

                        revealed_board[row][column] = '*'
                        revealMines()
                        printBoard()

                        # end timer
                        end = time.time()

                        # print(end - start) #exact time in floating point
                        print("\nTimespent = %d second(s)" %round(end - start))
                        print("\nGame over. Stepped on a mine!!!\n")

                        # check if reset
                        replay = input("Would you like to play again (y/n): ")

                        # if no quit game
                        if replay[0] == 'n':
                                play = False

                        # reset and firstmove to reinitiate board
                        searched.clear()
                        flags.clear()
                        questionMark.clear()
                        firstmove = True

                # no mines in neighbouring cells,reveal neighbours
                elif board[row][column] == 0:
                        revealed_board[row][column] = '0'
                        #searched = []

                        revealTile(row, column)

                # if theres a mine in neighbouring cells
                else:
                        searched.append([row,column])
                        revealed_board[row][column] = board[row][column]

                # check game state
                if(gameCheck()):

                        revealMines()
                        printBoard()

                        # end timer
                        end = time.time()

                        # print(end - start) #exact time in floating point
                        print("\nTimespent = %d second(s)" %round(end - start))
                        print("\nYou won!!\n")

                        # check if reset
                        replay = input("Would you like to play again (y/n): ")

                        # if no quit game
                        if replay[0] == 'n':
                                play = False

                        # reset and firstmove to reinitiate board
                        searched.clear()
                        flags.clear()
                        questionMark.clear()
                        firstmove = True