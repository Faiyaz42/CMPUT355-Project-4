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
mines_locations=[]
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


                        cell = cell + "|  " + str(mines_locations[row][column]) + "  "
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
                        mines_locations[row][column] = board[row][column]

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
                        mines_locations[row][column] = board[row][column]



# show mine locations
def revealMines():
        for row in range(size):
                for column in range(size):

                        if board[row][column] == -1:
                                mines_locations[row][column] = '*'





# check game state
def gameCheck():


        # numbered tiles count
        revealed_numbers = 0

        #check each cell
        for row in range(size):
                for column in range(size):
                        #if revealed and not flagged and not sus
                        if mines_locations[row][column] != ' ' and mines_locations[row][column] != 'F' and mines_locations[row][column] != '?':
                                revealed_numbers += 1   #increment revealed tiles

        # check if all non-mine tiles are found
        if revealed_numbers == size * size - number_mines:
                return True
        else:
                return False




######################################################
####################### PLAYER #######################
######################################################



def logic_calc(row, column):
        flagged_tiles = []
        unflagged_tiles = []

        # up
        if row > 0 and [row-1,column] not in searched:
                if mines_locations[row-1][column] == 'F':
                        flagged_tiles.append([row-1,column])
                else:
                        unflagged_tiles.append([row-1,column])
        # down
        if row < size-1  and [row+1,column] not in searched:
                if mines_locations[row+1][column] == 'F':
                        flagged_tiles.append([row+1,column])
                else:
                        unflagged_tiles.append([row+1,column])
        # left
        if column > 0 and [row,column-1] not in searched:
                if mines_locations[row][column-1] == 'F':
                        flagged_tiles.append([row,column-1])
                else:
                        unflagged_tiles.append([row,column-1])
        # right
        if column < size-1 and [row,column +1] not in searched:
                if mines_locations[row][column +1] == 'F':
                        flagged_tiles.append([row,column +1])
                else:
                        unflagged_tiles.append([row,column +1])
        # top-left
        if row > 0 and column > 0 and [row-1,column -1] not in searched:
                if mines_locations[row-1][column -1] == 'F':
                        flagged_tiles.append([row-1,column -1])
                else:
                        unflagged_tiles.append([row-1,column -1])
        # top-right
        if row > 0 and column < size-1 and [row-1,column+1] not in searched:
                if mines_locations[row-1][column+1] == 'F':
                        flagged_tiles.append([row-1,column+1])
                else:
                        unflagged_tiles.append([row-1,column+1])
        # below-left
        if row < size -1 and column > 0 and [row+1,column-1] not in searched:
                if mines_locations[row+1][column-1] == 'F':
                        flagged_tiles.append([row+1,column-1])
                else:
                        unflagged_tiles.append([row+1,column-1])
        # below-right
        if row < size-1 and column < size -1 and [row+1,column +1] not in searched:
                if mines_locations[row+1][column +1] == 'F':
                        flagged_tiles.append([row+1,column +1])
                else:
                        unflagged_tiles.append([row+1,column +1])

    #Rule 1
    #If a tile has has same amount of hidden tiles around it as unflagged bombs remaining around it then all the hidden tiles are bombs
        if mines_locations[row][column] == (len(unflagged_tiles) + len(flagged_tiles)) and len(unflagged_tiles) > 0:
                if len(unflagged_tiles) == 1:
                        completed_tiles.append([row,column])
                return unflagged_tiles[0][0], unflagged_tiles[0][1], True


    #Rule 2
    #If a tile has the same amount of flags around it as the number on the square then all remaining hidden tiles around it are not bombs
        if mines_locations[row][column] == len(flagged_tiles) and len(unflagged_tiles) > 0:
                if len(unflagged_tiles) == 1:
                        completed_tiles.append([row,column])
                return unflagged_tiles[0][0], unflagged_tiles[0][1], False


        """if len(unflagged_tiles) == 0:
                completed_tiles.append([row,column])
                return -1, -1, False"""
        return -1, -1, False

def find_sections():

        h_border_tiles = []
        h_tiles = []
        border_tiles = []

        for row in range(size):
                for column in range(size):
                        #find all border tiles
                        if [row, column] not in completed_tiles and [row, column] in searched and mines_locations[row][column] != 0:
                                border_tiles.append([row, column])
                                # find all hidden bording tiles (not including flagged tiles)
                                # up
                                if row > 0 and [row-1,column] not in searched:
                                        if mines_locations[row-1][column] != 'F' and [row-1,column] not in h_border_tiles:
                                                h_border_tiles.append([row-1,column])
                                # down
                                if row < size-1  and [row+1,column] not in searched:
                                        if mines_locations[row+1][column] != 'F' and [row+1,column] not in h_border_tiles:
                                                h_border_tiles.append([row+1,column])
                                # left
                                if column > 0 and [row,column-1] not in searched:
                                        if mines_locations[row][column-1] != 'F' and [row,column-1] not in h_border_tiles:
                                                h_border_tiles.append([row,column-1])
                                # right
                                if column < size-1 and [row,column +1] not in searched:
                                        if mines_locations[row][column +1] != 'F' and [row,column +1] not in h_border_tiles:
                                                h_border_tiles.append([row,column +1])
                                # top-left
                                if row > 0 and column > 0 and [row-1,column -1] not in searched:
                                        if mines_locations[row-1][column -1] != 'F' and [row-1,column -1] not in h_border_tiles:
                                                h_border_tiles.append([row-1,column -1])
                                # top-right
                                if row > 0 and column < size-1 and [row-1,column+1] not in searched:
                                        if mines_locations[row-1][column+1] != 'F' and [row-1,column+1] not in h_border_tiles:
                                                h_border_tiles.append([row-1,column+1])
                                # below-left
                                if row < size -1 and column > 0 and [row+1,column-1] not in searched:
                                        if mines_locations[row+1][column-1] != 'F' and [row+1,column-1] not in h_border_tiles:
                                                h_border_tiles.append([row+1,column-1])
                                # below-right
                                if row < size-1 and column < size -1 and [row+1,column +1] not in searched:
                                        if mines_locations[row+1][column +1] != 'F' and [row+1,column +1] not in h_border_tiles:
                                                h_border_tiles.append([row+1,column +1])

        #find all non-border hidden tiles
        for row in range(size):
                for column in range(size):
                        if [row, column] not in searched and [row, column] not in h_border_tiles and mines_locations[row][column] != 'F':
                                h_tiles.append([row, column])


        ##################################
        # THIS IS THE PLACE TO SEGRAGATE #
        ##################################

        guess_mines = 0

        for n in border_tiles:
            guess_mines += mines_locations[n[0]][n[1]]

        full_combo_lst = []

        #for n in range(1,len(h_border_tiles)+1):
        for n in range(1,guess_mines+1):
                combo_lst = list(itertools.combinations(h_border_tiles, n))
                
                for i in combo_lst:
                        full_combo_lst.append(i)


        ####################################
        # CHECK LEGAL #
        ####################################

        legal_combo_lst = []

        for combo in full_combo_lst:
                legal = True
                for tile in border_tiles:
                        row = tile[0]
                        column = tile[1]
                        count = 0
                        # up
                        if row > 0 and [row-1,column] not in searched:
                                if mines_locations[row-1][column] == 'F' or [row-1,column] in combo:
                                        count += 1
                        # down
                        if row < size-1  and [row+1,column] not in searched:
                                if mines_locations[row+1][column] == 'F' or [row+1,column] in combo:
                                        count += 1
                        # left
                        if column > 0 and [row,column-1] not in searched:
                                if mines_locations[row][column-1] == 'F' or [row,column-1] in combo:
                                        count += 1
                        # right
                        if column < size-1 and [row,column +1] not in searched:
                                if mines_locations[row][column +1] == 'F' or [row,column +1] in combo:
                                        count += 1
                        # top-left
                        if row > 0 and column > 0 and [row-1,column -1] not in searched:
                                if mines_locations[row-1][column -1] == 'F' or [row-1,column -1] in combo:
                                        count += 1
                        # top-right
                        if row > 0 and column < size-1 and [row-1,column+1] not in searched:
                                if mines_locations[row-1][column+1] == 'F' or [row-1,column+1] in combo:
                                        count += 1
                        # below-left
                        if row < size -1 and column > 0 and [row+1,column-1] not in searched:
                                if mines_locations[row+1][column-1] == 'F' or [row+1,column-1] in combo:
                                        count += 1
                        # below-right
                        if row < size-1 and column < size -1 and [row+1,column +1] not in searched:
                                if mines_locations[row+1][column +1] == 'F' or [row+1,column +1] in combo:
                                        count += 1

                        # check if tile is legal
                        if mines_locations[row][column] != count or len(combo) > (number_mines - marked_mines):
                                legal = False
                                break

                if legal:
                        legal_combo_lst.append(combo)

        ####################################
        # COUNT BOMBS #
        ####################################

        # first check if any places there are no bombs
        bomb_lst = []

        for tiles in legal_combo_lst:
                for tile in tiles:
                    bomb_lst.append(tile)

        for tile in h_border_tiles:
            if tile not in bomb_lst:
                return tile[0], tile[1], False

        # if all places have a chance to have a bomb then sort by lowest chance
        bomb_lst = []

        for tiles in legal_combo_lst:
                for tile in tiles:
                        tile = tuple(tile)
                        bomb_lst.append(tile)
        bomb_dict = Counter(bomb_lst)
        bomb_lst = sorted(bomb_dict.items(), key=lambda kv: kv[1])


        if len(bomb_lst) > 0:
                best_tile = bomb_lst[0][0]
                best_tile_percent = bomb_lst[0][1] / len(legal_combo_lst)
        else:
                n = random.randint(0, len(h_border_tiles)-1)
                return h_border_tiles[n][0], h_border_tiles[n][1], False

        ####################################
        # NON BORDER BOMB ODDS #
        ####################################

        base_prob = ((number_mines - marked_mines)/(len(h_border_tiles) + len(h_tiles)))

        if best_tile_percent <= base_prob:
                return bomb_lst[0][0][0], bomb_lst[0][0][1], False

        n = random.randint(0, len(h_tiles)-1)
        return h_tiles[n][0], h_tiles[n][1], False






def find_move(firstmove):

        if firstmove:
                j = random.randint(0, size*size-1)
                column = j % size
                row = j // size
                return row, column, False

        for row in range(size):
                for column in range(size):
                    if [row, column] not in completed_tiles and [row, column] in searched and mines_locations[row][column] != 0:
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
        """
        integer = False
        while integer == False:
                try:
                        size = int(input("\nEnter size of board: "))
                        number_mines = int(input("\nEnter number of mines: "))
                        integer = True
                except ValueError:
                        print("\nPlease enter size and number of mines in integers only!")
                        continue


        # initiating the board
        board = [[0 for y in range(size)] for x in range(size)]
        # initiating array for mines
        mines_locations = [[' ' for y in range(size)] for x in range(size)]

        # flagged tiles
        flags = []

        #question mark suspected tiles
        questionMark = []

        # plant mines
        minePlacer()

        # tile values
        calcTile()

        #timer start
        start = time.time()
        """

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
                        mines_locations = [[' ' for y in range(size)] for x in range(size)]

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
                """
                # Input from the user
                move = input("\nInstructions:\n 1. Enter row and column to select the tile.Input format example: 1 2 \
                \n 2. To flag a tile,enter flag after row and column.Input format example: 1 2 flag \
                \n 3. To unflag a flagged tile,enter unflag after row and column.Input format example: 1 2 unflag \
                \n 4. To sus a tile,enter sus after row and column.Input format example: 1 2 sus \
                \n 5. To unsus a sus tile,enter unsus after row and column.Input format example: 1 2 unsus \
                \n 6. Type r to reset current board. \
                \n 7. Type q to quit. \
                \nInput : ").split()
                """
                """
                # quit game
                if move[0] == 'q':
                        play = False

                # reset current board
                if move[0] == 'r':
                        searched.clear()
                        flags.clear()
                        questionMark.clear()
                        firstmove = True
                        continue

                        '''
                        mines_locations = [[' ' for y in range(size)] for x in range(size)]
                        searched.clear()
                        flags.clear()
                        questionMark.clear()
                        '''

                # check if numerical input or not
                if len(move) == 2:
                        try:
                                tile = [int(item) for item in move]
                        except ValueError:
                                print("\nPlease enter row and column numbers in integers only!")
                                continue


                # input with flag/unflag or sus/unsus
                elif len(move) == 3:
                        if  move[2] != 'flag' and move[2] != 'unflag' and move[2] != 'sus' and move[2] != 'unsus':
                                print("\nthird command flag,unflag,sus or unsus only!")
                                continue



                        # check if first 2 inputs integers or not
                        try:

                                tile = [int(item) for item in move[:2]]
                                mark = move[2]
                        except ValueError:
                                print("\nPlease enter row and column numbers in integers only!")
                                continue






                        #check if input is in range
                        if tile[0] > size or tile[0] < 1 or tile[1] > size or tile[1] < 1:
                                print("\nposition out of range,must be a location on the board!")
                                continue


                        row = tile[0]-1
                        column = tile[1]-1

                        #dont flag already flagged tile
                        if [row, column] in flags and mark != 'unflag':
                                print("\nAlready flagged.\nUnflag first to sus.")
                                continue



                        # if already revealed
                        #if mines_locations[row][column] != ' ' and mark != 'unflag' and mark != 'unsus':
                                #print("\nValue already known")
                                #continue


                        #dont sus already sus tile
                        if [row, column] in questionMark and mark != 'unsus':
                                print("\nAlready sus.\nUnsus first to flag.")
                                continue

                        # if already revealed
                        if mines_locations[row][column] != ' ' and mines_locations[row][column] != '?' and mines_locations[row][column] != 'F':
                                print("\nValue already known")
                                continue


                        if [row, column] in questionMark and mark == 'unsus' :
                                print("\nUnsus tile")
                                mines_locations[row][column] = ' '
                                for item in questionMark:
                                        i = 0
                                        if item[i] == row:
                                                if item[i+1] == column:
                                                        questionMark.remove([row,column])


                        if mark == 'sus' and [row, column] not in flags:
                                questionMark.append([row, column])
                                mines_locations[row][column] = '?'
                                print("\nSus tile")



                        if [row, column] in flags and mark == 'unflag' :
                                print("\nUnflagged tile")
                                mines_locations[row][column] = ' '
                                for item in flags:
                                        i = 0
                                        if item[i] == row:
                                                if item[i+1] == column:
                                                        flags.remove([row,column])
                                                        marked_mines -= 1



                        # check to make sure number of flags = bombs
                        if len(flags) < number_mines :

                                if mark == 'flag' and [row, column] not in questionMark:
                                        flags.append([row, column])
                                        mines_locations[row][column] = 'F'
                                        marked_mines += 1
                                        print("\nFlagged tile")
                                continue
                        else:
                                if mark != 'sus' and mark != 'unsus':
                                        print("\nNo more flags.Number of flags = Number of mines!")
                                continue

                else:

                        if move[0] != 'r' and move[0] != 'q':
                                print("\nInvalid input")
                        continue






                #check if input is in range
                if tile[0] > size or tile[0] < 1 or tile[1] > size or tile[1] < 1:
                        print("\nposition out of range,must be a location on board!")
                        continue


                row = tile[0]-1
                column = tile[1]-1

                """
                if flag:
                        flags.append([row, column])
                        mines_locations[row][column] = 'F'
                        marked_mines += 1
                        continue

                # if stepped on mine,game over
                if board[row][column] == -1:

                        mines_locations[row][column] = '*'
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
                        mines_locations[row][column] = '0'
                        #searched = []

                        revealTile(row, column)

                # if theres a mine in neighbouring cells
                else:
                        searched.append([row,column])
                        mines_locations[row][column] = board[row][column]

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


        '''
        # end timer
        end = time.time()

        # print(end - start) #exact time in floating point
        print("\nTimespent = %d second(s)" %round(end - start))
        '''
