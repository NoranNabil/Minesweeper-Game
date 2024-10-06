# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 21:23:03 2024

@author: Norana
"""

import tkinter
import settings
import random
import ctypes
import sys
import utils
import time


class Cell:
    all_cells =[]
    mines = []
    left_cells = settings.Cells_count
    
    
    def __init__(self, x,y, is_mine = False):
        self.is_mine = is_mine # to know if the cell is mine or not 
        self.button = None
        self.col = y
        self.row = x
        self.is_open = False
        self.is_candidate =False 
        
        Cell.all_cells.append(self)
        
    
    ### create a button and assign it to a cell
    def Create_button(self,frame,text=" ",bg="white"):
        self.button = tkinter.Button(frame,width =12,height = 4,text=text,bg=bg)
        self.button.bind('<Button-1>', self.Left_click_button_action) ### assign the button action to the button event 
        self.button.bind('<Button-3>', self.Right_click_button_action)
        
    ### place or grid the button
    def Place_button(self,x=0 ,y=0):
        if self.button != None:
            self.button.place(x=x, y=y)
        
    def Grid_button(self,col=0,row=0):
        if self.button != None:
            self.button.grid(column = col, row = row)
    
    ### define button actions of the button
    ### left >>> count the number of minds in surrounding
    ### helper functionsn 
    def Count_serrounding_mines(self,cell):
       mines_num = 0
       for mine in Cell.mines:            
               if (mine.col == cell.col) or (mine.col == cell.col-1) or (mine.col == cell.col+1):
                      #print(f"searching at col {mine.col}")
                      if (mine.row == cell.row) or (mine.row == cell.row-1) or (mine.row == cell.row+1):
                          if cell != mine:
                              mines_num+=1
                           
       cell.button.config(text=f"{mines_num}",bg='SystemButtonFace')
       return mines_num
    
    ### to find cells by row & col 
    def find_cell_by_axis(self,x,y):
        for cell in Cell.all_cells:
            if cell.row == x and cell.col == y:
                return cell
    ### to find a list of surroinding cells
    def find_serrounding_cells(self):
        serroundings = [self.find_cell_by_axis(self.row-1,self.col-1),
                        self.find_cell_by_axis(self.row-1,self.col),
                        self.find_cell_by_axis(self.row-1,self.col+1),
                        self.find_cell_by_axis(self.row,self.col-1),
                        self.find_cell_by_axis(self.row,self.col+1),
                        self.find_cell_by_axis(self.row+1,self.col-1),
                        self.find_cell_by_axis(self.row+1,self.col),
                        self.find_cell_by_axis(self.row+1,self.col+1),
                        ]
        serroundings = [cell for cell in serroundings if cell is not None]
        return serroundings
    #### left action 
    def Left_click_button_action(self,event): ### event should take an additional parameter 
        #1. minus the non clicked buttons by one:
        if self.is_open == False:
            Cell.left_cells -=1
            self.is_open = True
            if Cell.left_cells == settings.Mines:
                ctypes.windll.user32.MessageBoxW(0,"Winner !",0)
                sys.exit()
        else:
            pass
        #2. game over if it is a mine 
        if self.is_mine:
            self.button.config(bg='red')
            self.button.update_idletasks()
            ctypes.windll.user32.MessageBoxW(0,"Loser!","Game Over",0)
            sys.exit()
            
        #3. find number of surrounding mines 
        else: 
            mines_num = self.Count_serrounding_mines(cell = self)
            ### 4.in case of zero surrounding mines , show number of mines for each one
            if mines_num == 0: ### in case of zero surrounding mines , show number of mines for each one
                serroundings = self.find_serrounding_cells()
                for cell in serroundings:
                    self.Count_serrounding_mines(cell)
                    if cell.is_open == False and settings.Cells_count != 0:
                        Cell.left_cells -=1
                        cell.is_open = True
                        if Cell.left_cells == settings.Mines:
                            ctypes.windll.user32.MessageBoxW(0,"Winner !",0)
                            sys.exit()
        #5. update cell count on the label 
        Cell.label.configure(text=f"Cells left : {Cell.left_cells}")

    #### right action 
    
    def Right_click_button_action(self,event): ### event should take an additional parameter 
        if not self.is_open:
            if not self.is_candidate:
                self.button.config(bg='orange')
                self.is_candidate = True
            else:
               self.button.config(bg='SystemButtonFace')
               self.is_candidate = False 
    
    ### prepare mines
    @classmethod
    def Make_mines(cls):
        for cell in random.sample(Cell.all_cells,settings.Mines):
            cell.is_mine = True
            Cell.mines.append(cell)
            #cell.button.config(text=f"i am mine at {cell.row},{cell.col}")
            
  
                
    ### repr
    def __repr__(self):
        return f"cell({self.row},{self.col})"
    
    ### show number of not clicked cells 
    @classmethod
    def create_cell_count_label(cls,frame):
        Cell.label = tkinter.Label(frame,text=f"Cells left : {Cell.left_cells}",width = 18 , height = 6,font = ('',20) , bg= 'black',fg='white')
        Cell.label.place(x=utils.Width_Percentage(2),y=utils.Height_Percentage(10))
    ### show the game title 
    @classmethod
    def create_game_label(cls,frame):
        Cell.title = tkinter.Label(frame,text="Minesweepr Game",width = 25 , height = 4,font = ('',30) , bg= 'black',fg='white')
        Cell.title.place(x=utils.Width_Percentage(25),y=utils.Height_Percentage(1))
    


    