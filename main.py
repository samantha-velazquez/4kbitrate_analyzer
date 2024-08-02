from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from _utils import get_duration, get_framerate_float
from tkinter import PhotoImage
from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results
from pathlib import Path

from tqdm import tqdm
from math import trunc
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

root = Tk()
root.title("Bit Rate Calculator")
root.geometry('600x400')
button_pressed = 0


# create an entry and variable for the username.
# user_label = Label(root, text = 'Username', font=('calibre',10, 'bold'))
# user_label.grid()
# user_entry = Entry(root, textvariable=username, font=('calibre',10,'normal'))
# user_entry.grid(row=0, column=1)



def CurSelet(evt):
    value = str(histbox.get(ACTIVE))
    # just a test to see if click functionality works
    # print(value + "hi")
    print(os.path.abspath(value))
    image_path = os.path.abspath(value)

    
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.show()
     
    '''file1 = open(os.path.abspath(value))
    print(file1.read())
    file1.close()'''

    

    '''filedialog.askopenfilename(  
      title = "Select a file of any type",  
      filetypes = [("All files", "*.*")]  
      )  '''
    
    

histlabel = Label(root, text="History", font=('calibre',10, 'bold'))
histlabel.grid(column=0, row=4)
histbox = Listbox(root)
histbox.grid(column=0, row = 6)
histbox.bind('<<ListboxSelect>>', CurSelet)

def calcFiles():
    
    btn_pressed = 0

    loading_label = Label(root, text = "Loading...")
    loading_label.grid(column = 3, row = 4)
    progressbar = ttk.Progressbar(orient=HORIZONTAL, length=160)
    progressbar.grid(column = 5, row = 8)

    # progressbar.step()

    # open file explorer
    filename = filedialog.askopenfilename(initialdir="/Users", title="Select a File", filetypes=(("MP4 File", "*.mp4*"), ("All Files", "*.*")))
    
    

    if(filename[0] == "C"):
        file_no_upath = filename[9:-1]
        inst_1 = file_no_upath.find("/")
        user = file_no_upath[0:inst_1]
    else:
        file_no_upath = filename[13:-1]
        inst_1 = file_no_upath.find("/")
        user = file_no_upath[0:inst_1]
        print(user)
    
    

    btn_pressed = 1
    # set a path for the history
    uPath = "/mnt/c/Users/" + user
    fPath = uPath + "/BitRateHistory"
    if not os.path.exists(fPath):
        os.mkdir(fPath)

    
    

    vid_path = os.path.abspath(filename)
    vid_size = round(os.path.getsize(filename) / 1000000, 1)

    duration = round(float(get_duration(vid_path)))
    folder_contents = os.listdir(fPath)

    

    

    json = analyze_bitrate(filename)
    btn_pressed = 2

    # save json to history
    graph_filename = Path(filename).stem
    print("graph_filename: " + graph_filename)
    plot_results(json, filename, graph_filename, user)
    btn_pressed = 3
    
    print(graph_filename)
    print(os.path.basename(filename))

    print(os.path.abspath(graph_filename + ".png"))
    print(os.path.abspath(graph_filename + ".json"))

    os.chdir(uPath + "/BitRateHistory/")

    print(os.path.abspath(graph_filename + ".png"))
    print(os.path.abspath(graph_filename + ".json"))

    
    loading_label.grid_forget()
    fps = get_framerate_float(vid_path)
    total_frames = trunc(int(duration) * fps) + 1
    
    
       

    
    # get the file size from os
    
    # display file size 
    file_size_label = Label(root, text = "Video Size: " + str(vid_size) + " MB")
    file_size_label.grid(column=5, row=3)
    # get the video duration
    
    # display video duration 
    duration_label = Label(root, text = "Video Duration: " + str(duration) + " seconds")
    duration_label.grid(column=5, row=4)
    # create the history list
    

    for item in folder_contents:
        if(item.endswith(".png")):
            histbox.insert(END, item)
    

    """""
    print("image path: " + img_path)
    image =  PhotoImage(file=img_path)
    image_lbl = Label(root, image=image)
    image_lbl.grid(row=3, column=3)
    """""
   
calc_btn = Button(root, text = "Calculate", command = calcFiles)
calc_btn.grid(row=2,column=4)

 
root.mainloop()
