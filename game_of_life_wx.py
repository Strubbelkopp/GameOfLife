import numpy as np
import time
import wx

CELL_SIZE = 5
CELL_PADDING = 1
CELL_AMOUNT_X = 100 #min 36
CELL_AMOUNT_Y = 100 #min 23
SIDEBAR_WIDTH = 200
ITERATIONS = 150
GAME_SPEED = 2
RUN_FOREVER = False #run simulation forever or only the specified amount of iterations
INFINITE_BOARD = False #controls whether the board has walls, or continues on other side
RUNNING = False

BOARD_WIDTH = (CELL_SIZE + CELL_PADDING) * CELL_AMOUNT_X - CELL_PADDING
BOARD_HEIGHT = (CELL_SIZE + CELL_PADDING) * CELL_AMOUNT_Y - CELL_PADDING
WINDOW_WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH -8
WINDOW_HEIGHT = BOARD_HEIGHT + 39
WINDOW_SIDEBAR_RATIO = int(WINDOW_WIDTH/SIDEBAR_WIDTH)

grid_matrix = np.zeros((CELL_AMOUNT_Y,CELL_AMOUNT_X)) #grid containing the cells
save_matrix = np.zeros((CELL_AMOUNT_Y,CELL_AMOUNT_X)) #matrix to store amount of alive neighbour cells

#starting cells
start_configurations = ["Custom", "Space Ship", "Oscillator", "Glider Gun"]
empty = []
space_ship = [[0,1],[1,2],[2,0],[2,1],[2,2]]
oscillator = [[2,1], [2,2], [2,3]]
glider_gun = [[4,0],[4,1],[5,0],[5,1],[2,12],[2,13],[3,11],[4,10],[5,10],[6,10],[7,11],[8,12],[8,13],[5,14],[3,15],[4,16],[5,16],[5,17],[6,16],[7,15],[2,20],[2,21],[3,20],[3,21],[4,20],[4,21],[1,22],[5,22],[0,24],[1,24],[5,24],[6,24],[2,34],[2,35],[3,34],[3,35]]

def load_start_pattern(start_pattern):
    for i in start_pattern:
        grid_matrix[i[0]][i[1]] = 1

class AppFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), title="Game of Life", size=(WINDOW_WIDTH,WINDOW_HEIGHT))

        #main panel
        self.main_panel = wx.Panel(self)
        main_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #input panel
        input_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        width_input_panel = wx.BoxSizer(wx.HORIZONTAL)
        width_text = wx.StaticText(self.main_panel, label='Width:')
        width_input_panel.Add(width_text, 0, wx.ALL | wx.LEFT, 5)
        self.grid_width_input = wx.SpinCtrlDouble(self.main_panel)
        self.grid_width_input.SetValue(CELL_AMOUNT_X)
        width_input_panel.Add(self.grid_width_input, 1, wx.ALL, 5)          
        input_panel_sizer.Add(width_input_panel, 0, wx.CENTER | wx.EXPAND)

        height_input_panel = wx.BoxSizer(wx.HORIZONTAL)
        height_text = wx.StaticText(self.main_panel, label='Height:')
        height_input_panel.Add(height_text, 0, wx.ALL | wx.LEFT, 5)
        self.grid_height_input = wx.SpinCtrlDouble(self.main_panel)
        self.grid_height_input.SetValue(CELL_AMOUNT_Y)
        height_input_panel.Add(self.grid_height_input, 1, wx.ALL, 5)        
        input_panel_sizer.Add(height_input_panel, 0, wx.CENTER | wx.EXPAND)

        self.start_configurations_box = wx.ComboBox(self.main_panel, choices=start_configurations)
        self.start_configurations_box.Bind(wx.EVT_COMBOBOX, self.OnStartConfigSelect)
        input_panel_sizer.Add(self.start_configurations_box, 0, wx.ALL | wx.EXPAND, 5)

        self.infinite_board_check = wx.CheckBox(self.main_panel, label='Infinite Board')
        self.infinite_board_check.SetValue(INFINITE_BOARD)
        input_panel_sizer.Add(self.infinite_board_check, 0, wx.ALL | wx.LEFT, 5)

        self.run_forever_check = wx.CheckBox(self.main_panel, label='Run Forever')
        self.run_forever_check.SetValue(RUN_FOREVER)
        input_panel_sizer.Add(self.run_forever_check, 0, wx.ALL | wx.LEFT, 5)

        iterations_input_panel = wx.BoxSizer(wx.HORIZONTAL)
        iterations_text = wx.StaticText(self.main_panel, label='Iterations:')
        iterations_input_panel.Add(iterations_text, 0, wx.ALL | wx.LEFT, 5)
        self.iterations_input = wx.SpinCtrlDouble(self.main_panel)
        self.iterations_input.SetRange(0, 1000)
        self.iterations_input.SetValue(ITERATIONS)
        iterations_input_panel.Add(self.iterations_input, 1, wx.ALL, 5)        
        input_panel_sizer.Add(iterations_input_panel, 0, wx.CENTER | wx.EXPAND)

        game_speed_input_panel = wx.BoxSizer(wx.HORIZONTAL)
        game_speed_text = wx.StaticText(self.main_panel, label='Game Speed:')
        game_speed_input_panel.Add(game_speed_text, 0, wx.ALL | wx.LEFT, 5)
        self.game_speed_input = wx.SpinCtrlDouble(self.main_panel)
        self.game_speed_input.SetRange(0, 1000)
        self.game_speed_input.SetValue(GAME_SPEED)
        game_speed_input_panel.Add(self.game_speed_input, 1, wx.ALL, 5)        
        input_panel_sizer.Add(game_speed_input_panel, 0, wx.CENTER | wx.EXPAND)

        update_grid_btn = wx.Button(self.main_panel, label='Update Grid')
        update_grid_btn.Bind(wx.EVT_BUTTON, self.iterate_game)
        input_panel_sizer.Add(update_grid_btn, 0, wx.ALL | wx.CENTER, 5) 

        start_btn = wx.Button(self.main_panel, label='Start Game')
        start_btn.Bind(wx.EVT_BUTTON, self.on_start_press)
        input_panel_sizer.Add(start_btn, 0, wx.ALL | wx.CENTER, 5) 

        #grid panel
        self.grid_panel = wx.BoxSizer(wx.HORIZONTAL)
        self.image = wx.StaticBitmap(self.main_panel, 0, self.draw_bitmap())
        self.grid_panel.Add(self.image)

        main_panel_sizer.Add(input_panel_sizer, 1) #add input panel to main panel
        main_panel_sizer.Add(self.grid_panel, WINDOW_SIDEBAR_RATIO) #add grid panel to main panel

        self.main_panel.SetSizer(main_panel_sizer)
        self.Show() 

    def iterate_game(self, event):
        self.runGameStep()
        self.image.SetBitmap(self.draw_bitmap())
        #self.image.Refresh(eraseBackground=False)

    def draw_bitmap(self):
        bitmap = wx.Bitmap(BOARD_WIDTH, BOARD_HEIGHT)
        dc = wx.BufferedDC() 
        dc.SelectObject(bitmap)
        dc.Clear() 
        for y in range(CELL_AMOUNT_Y):
            for x in range(CELL_AMOUNT_X):
                if(grid_matrix[y,x] == 1):
                    dc.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))
                else:
                    dc.SetPen(wx.TRANSPARENT_PEN)
                    dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH))

                dc.DrawRectangle(
                x *(CELL_SIZE + CELL_PADDING),
                y * (CELL_SIZE + CELL_PADDING),
                CELL_SIZE, CELL_SIZE)
        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def OnStartConfigSelect(self, event):
        start_config = self.start_configurations_box.GetValue()
        if(start_config == "Custom"):
            start_configuration = empty
        elif(start_config == "Space Ship"):
            start_configuration = space_ship
        elif(start_config == "Oscillator"):
            start_configuration = oscillator
        elif(start_config == "Glider Gun"):
            start_configuration = glider_gun

        self.clear_grid()
        load_start_pattern(start_configuration)
        self.image.SetBitmap(self.draw_bitmap())
        #self.image.Refresh(eraseBackground=False)

    def clear_grid(self):
        for x in range(CELL_AMOUNT_X):
            for y in range(CELL_AMOUNT_Y):
                grid_matrix[y,x] = 0

    def on_start_press(self, event):
        global RUNNING
        global INFINITE_BOARD
        if(RUNNING == False):
            RUNNING = True
        else:
            RUNNING = False
        ITERATIONS = int(self.iterations_input.GetValue())
        GAME_SPEED = float(self.game_speed_input.GetValue())
        CELL_AMOUNT_X = int(self.grid_width_input.GetValue())
        CELL_AMOUNT_Y = int(self.grid_height_input.GetValue())
        RUN_FOREVER = bool(self.run_forever_check.GetValue())
        INFINITE_BOARD = bool(self.infinite_board_check.GetValue())

        if(RUN_FOREVER == True):
            while True:
                self.runGameStep()
                self.image.SetBitmap(self.draw_bitmap())
                #self.image.Refresh(eraseBackground=False)
                time.sleep(.1/GAME_SPEED)
        else:
            n = 0
            while(n < ITERATIONS):
                self.runGameStep()
                self.image.SetBitmap(self.draw_bitmap())
                #self.image.Refresh(eraseBackground=False)
                n += 1
                time.sleep(.1/GAME_SPEED)

    def runGameStep(self):

        #check for neighbors
        for x in range(CELL_AMOUNT_X):
            for y in range(CELL_AMOUNT_Y):
                alive_counter = 0

                if(y == 0): #if in first row
                        if(x != 0 and x != CELL_AMOUNT_X-1): #if neither in first nor in last column
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
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[-1,x-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,x] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,x+1] == 1):
                                    alive_counter += 1
                        if(x == 0): #if in first column
                            if(grid_matrix[y,x+1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y+1,x] == 1):
                                alive_counter += 1
                            if(grid_matrix[y+1,x+1] == 1):
                                alive_counter += 1
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[-1,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[1,-1] == 1):
                                    alive_counter += 1
                        if(x == CELL_AMOUNT_X-1): #if in last column
                            if(grid_matrix[y,x-1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y+1,x-1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y+1,x] == 1):
                                alive_counter += 1
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[-1,-2] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[1,0] == 1):
                                    alive_counter += 1
                if(y == CELL_AMOUNT_Y-1): #if in last row
                        if(x != 0 and x != CELL_AMOUNT_X-1): #if neither in first nor in last column
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
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[0,x+1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,x] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,x-1] == 1):
                                    alive_counter += 1
                        if(x == 0): #if in first column
                            if(grid_matrix[y,x+1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y-1,x] == 1):
                                alive_counter += 1
                            if(grid_matrix[y-1,x+1] == 1):
                                alive_counter += 1
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[0,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,-2] == 1):
                                    alive_counter += 1
                        if(x == CELL_AMOUNT_X-1): #if in last column
                            if(grid_matrix[y,x-1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y-1,x-1] == 1):
                                alive_counter += 1
                            if(grid_matrix[y-1,x] == 1):
                                alive_counter += 1
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[0,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-1,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[-2,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[0,-2] == 1):
                                    alive_counter += 1
                if(y != 0 and y != CELL_AMOUNT_Y-1): #if neither in first nor last row
                        if(x != 0 and x != CELL_AMOUNT_X-1): #if neither in first nor in last column
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
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[y-1,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[y,-1] == 1):
                                    alive_counter += 1
                                if(grid_matrix[y+1,-1] == 1):
                                    alive_counter += 1
                        if(x == CELL_AMOUNT_X-1): #if in last column
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
                            if(INFINITE_BOARD == True):
                                if(grid_matrix[y-1,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[y,0] == 1):
                                    alive_counter += 1
                                if(grid_matrix[y+1,0] == 1):
                                    alive_counter += 1
                
                save_matrix[y,x] = alive_counter
                
        #update cells
        for x in range(CELL_AMOUNT_X):
            for y in range(CELL_AMOUNT_Y):
                if(grid_matrix[y,x] == 1): #if cell is alive
                    if(save_matrix[y,x] < 2):
                        grid_matrix[y,x] = 0
                    if(save_matrix[y,x] > 3):
                        grid_matrix[y,x] = 0
                if(grid_matrix[y,x] == 0): #if cell is dead
                    if(save_matrix[y,x] == 3):
                        grid_matrix[y, x] = 1

if __name__ == '__main__':
    app = wx.App()
    frame = AppFrame()
    app.MainLoop()