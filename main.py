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

class Window:
    def __init__(self, tk):
        self.geometry = tk.geometry('600x400')
        self.title = tk.title('Bit Rate Analyzer')
        self.historyPath = StringVar()
        self.userPath = StringVar()
        self.getPath()
        self.clearFolder()
        self.createHistory(tk)
        self.calculate(tk)

    def clearFolder(self):
        for item in os.listdir(os.getcwd()):
            if (item.endswith(".png") or item.endswith(".json")):
                os.remove(os.path.abspath(item))
                print("removing..")

    def getPath(self):
        cwd = os.getcwd()
        if(cwd[0] == "C"):
            file_no_upath = cwd[9:-1]
            inst_1 = file_no_upath.find("/")
            user = file_no_upath[0:inst_1]
        else:
            file_no_upath = cwd[13:-1]
            inst_1 = file_no_upath.find("/")
            user = file_no_upath[0:inst_1]

        self.userPath.set("/mnt/c/Users/" + user + "/")
        self.historyPath.set(self.userPath.get() + "Documents/History")
        
        if not os.path.exists(self.historyPath.get()):
            os.mkdir(self.historyPath.get())

    def createHistory(self, tk):
        def CurSelet(evt):
            if self.histbox.size() != 0:
                value = str(self.histbox.get(ACTIVE))
                image_path = os.path.abspath(value)

                
                image = mpimg.imread(image_path)
                plt.imshow(image)
                plt.show()
            else:
                print("Histbox is empty.")

        self.histlabel = Label(tk, text="History", font=('calibre',10, 'bold'))
        self.histlabel.grid(column=0, row=4)
        self.histbox = Listbox(tk)
        self.histbox.grid(column=0, row = 6)
        self.histbox.bind('<<ListboxSelect>>', CurSelet)

        folder = os.listdir(self.historyPath.get())
        for item in folder:
            if(item.endswith(".png")):
                self.histbox.insert(END, item)

    def calculate(self, tk):
        def getFileStats(tk):
            loading_label = Label(tk, text = "Loading...")
            loading_label.grid(column = 3, row = 4)
            # open file explorer
            filename = filedialog.askopenfilename(initialdir=self.historyPath.get(), 
                                                    title="Select a File", 
                                                    filetypes=(("MP4 File", "*.mp4*"), 
                                                                ("All Files", "*.*")))
            vid_size = round(os.path.getsize(filename) / 1000000, 1)
            duration = round(float(get_duration(filename)))
 
            # display file size 
            file_size_label = Label(tk, text = "Video Size: " + str(vid_size) + " MB")
            file_size_label.grid(column=5, row=3)

            # display the video duration
            duration_label = Label(tk, text = "Video Duration: " + str(duration) + " seconds")
            duration_label.grid(column=5, row=4)

            # json holds the function analyze bitrate
            json = analyze_bitrate(filename)
            graph_title = Path(filename).name
            graph_filename = Path(filename).stem

            # creates the graph image file
            plot_results(json, graph_title, graph_filename, self.historyPath.get())    
            loading_label.grid_forget()

            # add new plots to history.

        self.calcBtn = Button(tk, text = "Calculate", command = getFileStats(tk))
        self.calcBtn.grid(row=2,column=4)
    


def main():
    root = Tk()
    window = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()