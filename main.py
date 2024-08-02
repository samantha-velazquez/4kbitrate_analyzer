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
    image_path = history_path.get() +'/' + value
    
    image = mpimg.imread(image_path)
    plt.axis('off')
    plt.grid(False)
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.show()


histlabel = Label(root, text="History", font=('calibre',10, 'bold'))
histlabel.grid(column=0, row=4)
histbox = Listbox(root)
histbox.grid(column=0, row = 6)
histbox.bind('<<ListboxSelect>>', CurSelet)

history_path = StringVar()
user_path = StringVar()

def calcFiles():
    for item in os.listdir(os.getcwd()):
        if(item.endswith(".png") or item.endswith(".json")):
            os.remove(os.path.abspath(item))
            print("removing..")

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

    uPath = "/mnt/c/Users/" + user + "/"
    user_path.set(uPath)

    # open file explorer
    filename = filedialog.askopenfilename(initialdir=uPath, title="Select a File", filetypes=(("MP4 File", "*.mp4*"), ("All Files", "*.*")))


    vid_size = round(os.path.getsize(filename) / 1000000, 1)

    duration = round(float(get_duration(filename)))

    
    json = analyze_bitrate(filename)

    # save json to history
    graph_title = Path(filename).name
    graph_filename = Path(filename).stem


    hist_path = uPath + "Documents/History"
    history_path.set(hist_path)
    if not os.path.exists(hist_path):
        os.mkdir(hist_path)

    plot_results(json, graph_title, graph_filename, hist_path)
    btn_pressed = 3
    
    loading_label.grid_forget()
    fps = get_framerate_float(filename)
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
    folder = os.listdir(os.getcwd())
    for item in folder:
        if(item.endswith(".json")):
            path = os.path.abspath(item)
            name = Path(path).name
            new_path = user_path.get() + "Downloads/" + name
            print("new path: " + new_path)
            os.replace(path, new_path)

def downloadPNG():
    history = history_path.get()
    folder = os.listdir(history)
    l = len(folder)
    file = folder[l-1]
    cwd = os.getcwd()
    os.chdir(history)
    path = os.path.abspath(file)
    new_path = path.replace("Documents/History", "Downloads")
    os.chdir(cwd)
    shutil.copyfile(path, new_path)

def close():
    path = history_path.get()
    folder = os.listdir(path)
    cwd = os.getcwd()
    os.chdir(history_path.get())
    for file in folder:
        os.remove(os.path.abspath(file))
    os.rmdir(path)
    os.chdir(cwd)
    root.destroy()

calc_btn = Button(root, text = "Calculate", command = calcFiles)
calc_btn.grid(row=2,column=4)

dJSON_btn = Button(root, text = "Download JSON", command=downloadJSON)
dJSON_btn.grid(row=7, column=0)

dPNG_btn = Button(root, text = "Download PNG", command=downloadPNG)
dPNG_btn.grid(row=7, column=1)

quit_btn = Button(root, text = "Exit", background = "red",command = close)
quit_btn.grid(row=7, column=4)


root.mainloop()