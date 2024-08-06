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
        self.title = tk.title('Bit Rate Analyzer')
        self.geometry = tk.geometry('600x400')
        self.clearFolder()
        self.createHistory(tk)

    def clearFolder():
        for item in os.listdir(os.getcwd()):
            if (item.endswith(".png") or item.endswith(".json")):
                os.remove(os.path.abspath(item))
                print("removing..")

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
    
    def getPath():
        self.historyPath = StringVar()
        self.userPath = StringVar()


def main():
    root = Tk()
    window = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()