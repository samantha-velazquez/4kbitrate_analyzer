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
        self.historyPath = self.title = tk.title('Bit Rate Analyzer')
        self.historyPath = StringVar()
        self.userPath = StringVar()
        self.getPath()
        self.clearFolder()
        self.createHistory(tk)

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

        

def main():
    root = Tk()
    window = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()