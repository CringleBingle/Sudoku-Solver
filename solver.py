from test_case import board


#Input in the form of 9x9 board
# [
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0]
# ]



#Checking if board is empty
def empty(puzzle):
    for x in range(9):
        for y in range(9):
            if puzzle[x][y] == 0:
                return (x,y)
    return False

def valid(puzzle, num, coord):
    #row checker
    for x in range(len(puzzle[0])):
        if puzzle[coord[0]][x] == num and coord[1] != x:
            return False
    #column checker
    for x in range(len(puzzle)):
        if puzzle[x][coord[1]] == num and coord[0] != x:
            return False
    #grid checker
    for x in range((coord[0]//3)*3, (coord[0]//3)*3 + 3):
        for y in range((coord[1]//3)*3, (coord[1]//3)*3 + 3):
            if num == puzzle[x][y] and (x,y) != coord:
                return False
            
    return True
        

def solver(puzzle):

    #Check if there are blank spaces left, if not then board is solved
    if not empty(puzzle):
        return puzzle
    
    else:
        i, j = empty(puzzle)
        
    for m in range(1,10):
        if valid(puzzle, m, (i,j)):
            puzzle[i][j] = m
            if solver(puzzle):  #Checking if board is solved with a number 'm' at empty square
                return True
            
            puzzle[i][j] = 0    #If not solved then backtracking to next possibility

    return False


#output
print('puzzle:')
for x in board:
    print(x)

print()
print('solution:')
solver(board)
for x in board:
    print(x)