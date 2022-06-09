import numpy as np
import time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

#starting values
CELL_AMOUNT_X = 100
CELL_AMOUNT_Y = 100
ITERATIONS = 150
SPEED = 5
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WIDGET_PANEL_WIDTH = 200
CELL_WIDTH = int((WINDOW_WIDTH-WIDGET_PANEL_WIDTH)/CELL_AMOUNT_X)
CELL_HEIGHT = int(WINDOW_HEIGHT/CELL_AMOUNT_Y)
WRAP_AROUND = True

#grid containing the cells
grid_matrix = np.zeros((CELL_AMOUNT_Y, CELL_AMOUNT_X), dtype=int)
#grid that stores the number of living neighbours 
save_matrix = np.zeros((CELL_AMOUNT_Y, CELL_AMOUNT_X), dtype=int)

#starting cells
start_configurations = ["Empty", "Space Ship", "Oscillator", "Glider Gun"]
empty = []
space_ship = [[0,1],[1,2],[2,0],[2,1],[2,2]]
oscillator = [[2,1], [2,2], [2,3]]
glider_gun = [[4,0],[4,1],[5,0],[5,1],[2,12],[2,13],[3,11],[4,10],[5,10],[6,10],[7,11],[8,12],[8,13],[5,14],[3,15],[4,16],[5,16],[5,17],[6,16],[7,15],[2,20],[2,21],[3,20],[3,21],[4,20],[4,21],[1,22],[5,22],[0,24],[1,24],[5,24],[6,24],[2,34],[2,35],[3,34],[3,35]]

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Game of Life')
        self.loadStartPattern(glider_gun)

        #Start button
        startButton = QPushButton(self)
        startButton.setText("Start Game")
        startButton.setShortcut('Enter')
        startButton.clicked.connect(self.runGame)
        startButton.move(50,20)

        #Run forever checkbox
        self.runForeverCheckbox = QCheckBox(self)
        self.runForeverCheckbox.setText("Run Forever")
        self.runForeverCheckbox.move(50, 50)

    def runGame(self):
        run_forever = self.runForeverCheckbox.checkState()
        generation = 0

        if(run_forever.name == "Unchecked"):
            while generation < ITERATIONS:
                self.updateCells(grid_matrix)
                self.repaint()
                time.sleep(.1/SPEED)
                generation += 1
        else:
            while True:
                self.updateCells(grid_matrix)
                self.repaint()
                time.sleep(.1/SPEED)
                generation += 1

    def loadStartPattern(self, start_pattern):
        for i in start_pattern:
            grid_matrix[i[0]][i[1]] = 1

    def calcNeighbours(self, grid_matrix):
        for y in range(CELL_AMOUNT_Y):
            for x in range(CELL_AMOUNT_X):
                
                if(WRAP_AROUND == False):
                    alive_neighbours = 0
                    try: # if wrap around is disabled try to calculate neighbours
                        for yOffset in range(-1, 2): # -1 to 1
                            for xOffset in range(-1, 2):
                                neighbourY = y + yOffset 
                                neighbourX = x + xOffset 
                                if grid_matrix[neighbourY, neighbourX] == 1:
                                    alive_neighbours += 1  
                    except: # move on if cell was non-existant and it gave an out of bounds error
                        pass               
                
                if(WRAP_AROUND == True):
                    alive_neighbours = 0
                    for yOffset in range(-1, 2): # -1 to 1
                        for xOffset in range(-1, 2):
                            neighbourY = (y + yOffset + CELL_AMOUNT_Y) % CELL_AMOUNT_Y # y + yOffset -> local y position of neighbour cell. If we add the grid width and take the modulus,
                            neighbourX = (x + xOffset + CELL_AMOUNT_X) % CELL_AMOUNT_X # we can wrap around for edge cases. Eg. y = 0, yOffset = -1, CELL_AMOUNT_Y = 10 -> neighbourY = (0 - 1 + 10) % 10 = 9
                            if grid_matrix[neighbourY, neighbourX] == 1:
                                alive_neighbours += 1
                    
                            
                save_matrix[y,x] = alive_neighbours - grid_matrix[y,x] #subtract own state again
                
        return save_matrix

    def updateCells(self, grid_matrix):
        neighbours = self.calcNeighbours(grid_matrix)
        for y in range(CELL_AMOUNT_Y):
            for x in range(CELL_AMOUNT_X):
                if grid_matrix[y,x] == 1: #if cell is alive
                    if neighbours[y,x] < 2:
                        grid_matrix[y,x] = 0
                    if neighbours[y,x] > 3:
                        grid_matrix[y,x] = 0
                if grid_matrix[y,x] == 0: #if cell is dead
                    if neighbours[y,x] == 3:
                        grid_matrix[y, x] = 1

    def paintEvent(self, e):
        self.painter = QPainter()
        self.painter.begin(self)
        self.drawRectangles()
        self.painter.end()

    def drawRectangles(self):
        for y in range(CELL_AMOUNT_Y):
            for x in range(CELL_AMOUNT_X):
                if grid_matrix[y,x] == 1:
                    self.painter.fillRect(x*CELL_WIDTH+WIDGET_PANEL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT, QBrush(Qt.GlobalColor.black))
                else:
                    self.painter.fillRect(x*CELL_WIDTH+WIDGET_PANEL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT, QBrush(Qt.GlobalColor.white))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())