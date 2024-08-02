from tkinter import *
from tkinter import filedialog
import os, shutil
from _utils import get_duration, get_framerate_float
from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results
from pathlib import Path
from math import trunc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

root = Tk()
root.title("Bit Rate Calculator")
root.geometry('600x400')
button_pressed = 0



def CurSelet(evt):
    value = str(histbox.get(ACTIVE))
    image_path = os.path.abspath(value)

    
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.show()


histlabel = Label(root, text="History", font=('calibre',10, 'bold'))
histlabel.grid(column=0, row=4)
histbox = Listbox(root)
histbox.grid(column=0, row = 6)
histbox.bind('<<ListboxSelect>>', CurSelet)


def calcFiles():
    for item in os.listdir(os.getcwd()):
        if(item.endswith(".png") or item.endswith(".json")):
            os.remove(os.path.abspath(item))
            print("removing..")

    btn_pressed = 0

    loading_label = Label(root, text = "Loading...")
    loading_label.grid(column = 3, row = 4)
    
    cwd = os.getcwd()

    if(cwd[0] == "C"):
        file_no_upath = cwd[9:-1]
        inst_1 = file_no_upath.find("/")
        user = file_no_upath[0:inst_1]
    else:
        file_no_upath = cwd[13:-1]
        inst_1 = file_no_upath.find("/")
        user = file_no_upath[0:inst_1]
        print(user)

    uPath = "/mnt/c/Users/" + user + "/"
    
    # open file explorer
    filename = filedialog.askopenfilename(initialdir=uPath, title="Select a File", filetypes=(("MP4 File", "*.mp4*"), ("All Files", "*.*")))


    vid_path = os.path.abspath(filename)
    vid_size = round(os.path.getsize(filename) / 1000000, 1)

    duration = round(float(get_duration(vid_path)))

    
    json = analyze_bitrate(filename)
    btn_pressed = 2

    # save json to history
    graph_title = Path(filename).name
    graph_filename = Path(filename).stem


    hist_path = vid_path.replace(graph_title, "History")
    if not os.path.exists(hist_path):
        os.mkdir(hist_path)

    plot_results(json, graph_title, graph_filename, hist_path)
    btn_pressed = 3
    
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
    
    folder = os.listdir(hist_path)
    for item in folder:
        if(item.endswith(".png")):
            histbox.insert(END, item)
    
def downloadJSON():
    folder= os.listdir(os.getcwd())
    for item in folder:
        if(item.endswith(".json")):
            path = os.path.abspath(item)
            new_path = path.replace("Documents/New folder/bitrate-viewer", "Downloads")
            os.replace(path, new_path)

def downloadPNG():
    folder = os.listdir(os.getcwd() + '/History')
    l = len(folder)
    file = folder[l-1]
    print(file)
    cwd = os.getcwd()
    os.chdir(os.getcwd() + "/History")
    path = os.path.abspath(file)
    print("old path: " +  path)
    new_path = path.replace("Documents/New folder/bitrate-viewer/History", "Downloads")
    print("new path: " + new_path)
    os.chdir(cwd)
    shutil.copyfile(path, new_path)

calc_btn = Button(root, text = "Calculate", command = calcFiles)
calc_btn.grid(row=2,column=4)

dJSON_btn = Button(root, text="Download JSON", command=downloadJSON)
dJSON_btn.grid(row=7, column=0)

dPNG_btn = Button(root, text="Download PNG", command=downloadPNG)
dPNG_btn.grid(row=7, column=1)

root.mainloop()