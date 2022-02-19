import numpy as np
import time

WIDTH = 10
HEIGHT = 10
ITERATIONS = 5

grid_matrix = np.zeros((HEIGHT,WIDTH)) #grid containing the cells
save_matrix = np.zeros((HEIGHT,WIDTH)) #matrix to store amount of alive neighbour cells

#starting cells
grid_matrix[0,1] = 1
grid_matrix[1,2] = 1
grid_matrix[2,0] = 1
grid_matrix[2,1] = 1
grid_matrix[2,2] = 1

n = 0
while(n < ITERATIONS):

    print(grid_matrix)
    print("")

    #check for neighbors
    for x in range(WIDTH):
        for y in range(HEIGHT):

            alive_counter = 0
            
            if(y == 0): #if in first row
                if(x != 0 and x != WIDTH-1): #if neither in first nor in last column
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x+1] == 1):
                        alive_counter += 1
                if(x == 0): #if in first column
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x+1] == 1):
                        alive_counter += 1
                if(x == WIDTH-1): #if in last column
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
            if(y == HEIGHT-1): #if in last row
                if(x != 0 and x != WIDTH-1): #if neither in first nor in last column
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x+1] == 1):
                        alive_counter += 1
                if(x == 0): #if in first column
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x+1] == 1):
                        alive_counter += 1
                if(x == WIDTH-1): #if in last column
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
            if(y != 0 and y != HEIGHT-1): #if neither in first nor last row
                if(x != 0 and x != WIDTH-1): #if neither in first nor in last column
                    if(grid_matrix[y-1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x+1] == 1):
                        alive_counter += 1
                if(x == 0): #if in first column
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x+1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x+1] == 1):
                        alive_counter += 1
                if(x == WIDTH-1): #if in last column
                    if(grid_matrix[y-1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y-1,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y,x-1] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x] == 1):
                        alive_counter += 1
                    if(grid_matrix[y+1,x-1] == 1):
                        alive_counter += 1

            save_matrix[y,x] = alive_counter
            
    #update cells
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if(grid_matrix[y,x] == 1): #if cell is alive
                if(save_matrix[y,x] < 2):
                    grid_matrix[y,x] = 0
                if(save_matrix[y,x] > 3):
                    grid_matrix[y,x] = 0
            if(grid_matrix[y,x] == 0): #if cell is dead
                if(save_matrix[y,x] == 3):
                    grid_matrix[y, x] = 1

    n += 1
    time.sleep(.5)