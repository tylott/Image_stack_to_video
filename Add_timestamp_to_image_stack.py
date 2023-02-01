#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:16:15 2023

@author: tyler

A short script to label an image stack before video conversion

MIT License

Copyright (c) 2023 Tyler Lott

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import matplotlib as mpl
import numpy as np
import copy

root = tk.Tk()
root.withdraw()

image_folder = filedialog.askdirectory()

images = [img for img in os.listdir(image_folder) if img.endswith(".tif")]
int_images= []
num = ["0","1","2","3","4","5","6","7","8","9"]
new_lst = []

test_lst = []
file_name_lst = []
count = 0
while count < len(images):
    for i in images[count]:
        if i in num:
            new_lst.append(i)
        elif count == 0:
            test_lst.append(i)
    val = ''.join(new_lst)
    if len(val) == 1:
        int_images.append("%01d" % int(val))
    elif len(val) == 2:
        int_images.append("%02d" % int(val))
    elif len(val) == 3:
        int_images.append("%03d" % int(val))
    elif len(val) == 4:
        int_images.append("%04d" % int(val))
    elif len(val) == 5:
        int_images.append("%05d" % int(val))
    elif len(val) == 6:
        int_images.append("%06d" % int(val))
    new_lst = []
    count += 1 
    
int_images.sort()

final_lst = []
count = 0

while count < len(int_images):
    text_lst = copy.deepcopy(test_lst)
    text_lst.insert(test_lst.index('.'),int_images[count])
    count += 1
    final_lst.append(text_lst)
 
   
final_lst_adjusted = []
count = 0


while count < len(final_lst):
    filename_adjusted = ''.join(str(final_lst[count]))
    filename_adjusted = filename_adjusted.replace("'","")
    filename_adjusted = filename_adjusted.replace("[","")
    filename_adjusted = filename_adjusted.replace("]","")
    filename_adjusted = filename_adjusted.replace(",","")
    filename_adjusted = filename_adjusted.replace(" ", "")
    final_lst_adjusted.append(filename_adjusted)
    count += 1 
    
path_to_tif = image_folder.count("/") # Counting the number of sub-folders within the root folder 
def remove_last(s):
    num_removed = 0 
    while s.count("/") == path_to_tif:   
        try:
            s = s[0:-1]
            if s.count('/') == path_to_tif:
                num_removed += 1
                continue
            else:
                return [s,num_removed]
            
        except ValueError:
            return ""
        
initial_file_path = remove_last(image_folder)[0] # Finding the root file path
image_ID = image_folder[len(image_folder)-remove_last(image_folder)[1]:-4] # Finding the name of the file ("linescan ID")
print(initial_file_path)
main_path = str(initial_file_path) + "/" + str(image_ID)

# First we check to see whether the specified path exists or not

isExist = os.path.exists(main_path)

if not isExist:
  # We create a new directory because it does not exist 
  os.makedirs(main_path)

path = str(main_path) + "/" + str(image_ID) + str("Testing")
        
system_fonts = mpl.font_manager.findSystemFonts(fontpaths=None, fontext='ttf') ### List of system fonts 

value_array = [0]
frame_time = 0.8402035 
count = 0
time = 0

while count < len(images):
    time += frame_time
    value_array.append(round(time)) # Rounding to the nearest integer 
    count += 1
count = 0

with open(str(path), "w") as output:
    for image in final_lst_adjusted:
        # Call draw Method to add 2D graphics in an image
        img = Image.open(str(image_folder)+ "/" + str(image))
        I1 = ImageDraw.Draw(img)
         
        # Custom font style and font size
        myFont = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=60)
        myFont2 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=40)
        
        # Add Text to an image
        I1.text((10, 10), str(str(value_array[count])+str(" seconds")), fill = "#FFFFFF", font=myFont)
        # Add Text to an image
        I1.text((800, 35), "10x speed", fill = "#FFFFFF", font=myFont2)
        I1.text((250, 900), "Unstained Liposomes", fill = "#FFFFFF", font=myFont)
        # Display edited image
        if count == 0:
            img.show()
         
        # Save the edited image
        img.save(path + str(count) + ".tif")
        count += 1
