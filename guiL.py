import os
from tkinter import *
from tkinter import filedialog
from _utils import get_duration, get_framerate_float
from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results
from pathlib import Path 
from tqdm import tqdm
from math import trunc
 
 
root = Tk()
root.title("Bit Rate Calculator")
root.geometry('600x400')
 
username = StringVar()
 
# create an entry and variable for the username.
user_label = Label(root, text = 'Username', font=('calibre',10, 'bold'))
user_label.grid()
user_entry = Entry(root, textvariable=username, font=('calibre',10,'normal'))
user_entry.grid(row=0, column=1)
 
 
 
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

file = StringVar()
file.set('')
 
def calcFiles():
    print(os.getcwd())
    user = username.get()
    username.set("")
    # set a path for the history
    uPath = "/mnt/c/Users/" + user
    fPath = uPath + "/BitRateHistory"
    if not os.path.exists(fPath):
        os.mkdir(fPath)
    # open file explorer
    filename = filedialog.askopenfilename(initialdir=uPath, title="Select a File", filetypes=(("MP4 File", "*.mp4*"), ("All Files", "*.*")))
    json = analyze_bitrate(filename, user, 'json')
    # save json to history
    graph_filename = Path(filename).stem
    plot_results(json, filename, graph_filename, user)

    print(os.path.basename(filename))
    print("graph_fiulename: " + graph_filename)
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
 
   
 
    """""
    img_path = fPath + "/" + graph_filename + ".png"
    print("image path: " + img_path)
    image =  PhotoImage(file=img_path)
    image_lbl = Label(root, image=image)
    image_lbl.grid(row=3, column=3)
    """""
   
calc_btn = Button(root, text = "Calculate", command = calcFiles)
calc_btn.grid(row=0,column=2)

dJSON_btn = Button(root, text = "Downlaod JSON")
dJSON_btn.grid(row=8)

dPNG_btn = Button(root, text = "Download PNG")
dPNG_btn.grid(row=8,column=1)

 
 
root.mainloop()
 