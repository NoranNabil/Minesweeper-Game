# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 16:12:53 2024

@author: Norana
"""

import tkinter 
### my modules
import settings
import utils
### my classes
from cell import Cell

### Window create 
#1.create object
root = tkinter.Tk()
#2.window configurations
root.title("MineSweeper Game")
root.geometry(f"{settings.Window_Width}x{settings.Window_Height}")
root.resizable(False,False)
root.configure(bg='black')


### window division into three frames
#1. top frame
top_frame=tkinter.Frame(root,bg = 'black',width = utils.Width_Percentage(100),height = utils.Height_Percentage(25))
top_frame.place(x=0,y=0) #place at the window 
#1. left frame
left_frame=tkinter.Frame(root,bg = 'black',width = utils.Width_Percentage(25),height = utils.Height_Percentage(75))
left_frame.place(x=0,y=utils.Height_Percentage(25))
#1. right frame
right_frame=tkinter.Frame(root,bg = 'black',width = utils.Width_Percentage(75),height = utils.Height_Percentage(75))
right_frame.place(x=utils.Width_Percentage(25),y=utils.Height_Percentage(25))


### make the grid in the right 
for i in range(settings.Grid_Size):
    for j in range (settings.Grid_Size):
        cell = Cell(x=i,y=j)
        cell.Create_button(right_frame)
        cell.Grid_button(j,i)
        
# make mines
Cell.Make_mines()

# show the number of non clicked cells on the left frame
Cell.create_cell_count_label(left_frame)

# show the game title
Cell.create_game_label(top_frame)
    


#Window run
root.mainloop()