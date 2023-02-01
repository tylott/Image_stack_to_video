"""
Created on Tue Jan 31 20:07:11 2023

@author: tyler

A short script to convert an image stack to video

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
import cv2
import os
import tkinter as tk
from tkinter import filedialog
import copy

root = tk.Tk()
root.withdraw()

choose_dir = filedialog.askdirectory()

image_folder = choose_dir

video_name = 'test.avi'

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
    int_images.append(int(val))
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
    
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fps = (10*1.1901878532998256) 

# Window name in which image is displayed
window_name = 'Image'
  
# Font
font = cv2.FONT_HERSHEY_SIMPLEX
   
frame_count = 0
time = float(frame_count)/fps
cv2.putText(frame, str(time), (10,500), font, 4, (255,255,255), 2, cv2.LINE_AA)
video = cv2.VideoWriter(video_name, 0, fps, (width,height))

frame_count = 0
for image in final_lst_adjusted:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
