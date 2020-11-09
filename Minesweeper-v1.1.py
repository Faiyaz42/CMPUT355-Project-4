####################################
######author:Faiyaz Ahmed
####################################


import random
import time

# Minesweeper Layout
size = 0
board = []
mines_locations=[]
number_mines = 0
searched = []


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









if __name__ == "__main__":

        # instructions and board setup inputs
        welcome = "Welcome to Minesweeper"
        print (welcome.rjust(50, ' ' ))
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
        
        
        play = True

        #game
        while play:
                printBoard()

                # Input from the user
                move = input("\nInstructions:\n 1. Enter row and column to select the tile.Input format example: 1 2 \
                \n 2. To flag a tile,enter flag after row and column.Input format example: 1 2 flag \
                \n 3. To unflag a flagged tile,enter unflag after row and column.Input format example: 1 2 unflag \
                \n 4. To sus a tile,enter sus after row and column.Input format example: 1 2 sus \
                \n 5. To unsus a sus tile,enter unsus after row and column.Input format example: 1 2 unsus \
                \n 6. Type r to reset current board. \
                \n 7. Type q to quit. \
                \nInput : ").split()
                
                
                #quit game
                if move[0] == 'q':
                        play = False
                        
                #reset current board
                if move[0] == 'r': 
                        mines_locations = [[' ' for y in range(size)] for x in range(size)]
                        searched.clear()
                        flags.clear()
                        questionMark.clear()

                #check if numerical input or not
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



                        #check if first 2 inputs integers or not
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



                        # check to make sure number of flags = bombs
                        if len(flags) < number_mines :
                                                                      
                                if mark == 'flag' and [row, column] not in questionMark:
                                        flags.append([row, column])
                                        mines_locations[row][column] = 'F'
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
               

                # if stepped on mine,game over  
                if board[row][column] == -1:
                        mines_locations[row][column] = '*'
                        revealMines()
                        printBoard()
                        print("\nGame over.stepped on a mine!!!")
                        play = False
                        

                # no mines in neighbouring cells,reveal neighbours
                elif board[row][column] == 0:
                        mines_locations[row][column] = '0'
                        searched = []
                        
                        revealTile(row, column)

                # if theres a mine in neighbouring cells  
                else:   
                        mines_locations[row][column] = board[row][column]

                # check game state
                if(gameCheck()):
                        revealMines()
                        printBoard()
                        print("\nYou won!!")
                        play = False
                        
        
        #end timer
        end = time.time()
        
        #print(end - start) #exact time in floating point
        print("\nTimespent = %d second(s)" %round(end - start))