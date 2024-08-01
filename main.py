import os
from tkinter import *
from tkinter import filedialog, messagebox
from _utils import get_duration, get_framerate_float
from tkinter import PhotoImage
from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results
from pathlib import Path
from tqdm import tqdm
from math import trunc
from PIL import ImageTk, Image
 
 
root = Tk()
root.title("Bit Rate Calculator")
root.geometry('600x400')
 

# create an entry and variable for the username.
user_label = Label(root, text = 'Username', font=('calibre',10, 'bold'))
user_label.grid()
# user_entry = Entry(root, textvariable=username, font=('calibre',10,'normal'))
# user_entry.grid(row=0, column=1)
 
 
 
def CurSelet(evt):
    value = str(histbox.get(ACTIVE))
    # just a test to see if click functionality works
    print(value + "hi")
    print(os.path.abspath(value))
    filedialog.askopenfilename(  
      title = "Select a file of any type",  
      filetypes = [("All files", "*.*")]  
      )  
   
 
histlabel = Label(root, text="History", font=('calibre',10, 'bold'))
histlabel.grid(column=0, row=3)
histbox = Listbox(root)
histbox.grid(column=0, row = 6)
histbox.bind('<<ListboxSelect>>', CurSelet)
 
def calcFiles():
   
   
   
    # open file explorer
    filename = filedialog.askopenfilename(initialdir="/Users", title="Select a File", filetypes=(("MP4 File", "*.mp4*"), ("All Files", "*.*")))
   
    file_no_upath = filename[13:-1]
    print(file_no_upath)
    inst_1 = file_no_upath.find("/")
    print(inst_1)
    user = file_no_upath[0:inst_1]
    print(user)
   
 
    # set a path for the history
    uPath = "/mnt/c/Users/" + user
    fPath = uPath + "/BitRateHistory"
    if not os.path.exists(fPath):
        os.mkdir(fPath)
 
    json = analyze_bitrate(filename, fPath)
    # save json to history
    graph_filename = Path(filename).stem
    print("graph_filename: " + graph_filename)
    plot_results(json, filename, graph_filename, user)
   
 
    # get the file size from os
    vid_path = os.path.abspath(filename)
    vid_size = round(os.path.getsize(filename) / 1000000, 1)
    # display file size
    file_size_label = Label(root, text = "Video Size: " + str(vid_size) + " MB")
    file_size_label.grid(column=5, row=3)
    # get the video duration
    duration = round(float(get_duration(vid_path)))
    # display video duration
    duration_label = Label(root, text = "Video Duration: " + str(duration) + " seconds")
    duration_label.grid(column=5, row=4)
    # create the history list
    folder_contents = os.listdir(fPath)
   
    histbox.insert(END, os.path.basename(filename))
   
 
   
    fps = get_framerate_float(vid_path)
    total_frames = trunc(int(duration) * fps) + 1
    #print(f'Now analyzing ~ {total_frames} frames.')
    progress_bar = tqdm(total_frames, unit=' frames', ncols=80)
 

   
calc_btn = Button(root, text = "Calculate", command = calcFiles)
calc_btn.grid(row=0,column=2)
 
 
root.mainloop()