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
        self.tk = tk
        self.geometry = self.tk.geometry('600x400')
        self.tk.resizable(width = True, height = True)
        self.title = self.tk.title('Bit Rate Analyzer')
        self.frame = Frame(self.tk)
        self.frame.pack(pady=10)

        self.historyPath = StringVar()
        self.userPath = StringVar()
        self.calc_var = 0
        self.file_size_label = Label(self.tk)
        self.duration_label = Label(self.tk)

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

    def createHistory(self):
        def CurSelet(evt):
            if self.histbox.size() != 0:
                value = str(self.histbox.get(ACTIVE))
                os.chdir(self.historyPath.get())
                image_path = os.path.abspath(value)
                print(image_path)
                
                image = mpimg.imread(image_path)
                plt.imshow(image)
                plt.show()
            else:
                print("Histbox is empty.")

        #self.histlabel = Label(self.tk, text="History", font=('calibre',10, 'bold'))
        #self.histlabel.grid(column=0, row=4)
        self.histbox = Listbox(
            self.frame,
            #width=25,
            #height=8,

        )
        self.histbox.pack(side=LEFT, fill=BOTH)

        self.sb = Scrollbar(self.frame)
        self.sb.pack(side=RIGHT, fill=BOTH)
        self.histbox.bind('<<ListboxSelect>>', CurSelet)

        folder = os.listdir(self.historyPath.get())
        for item in folder:
            if(item.endswith(".png")):
                self.histbox.insert(END, item)

    def calculate(self):
        def getStats(evt): 
            print("clicked")
            self.calc_var+=1
            print(self.calc_var)
            # open file explorer
            
            loading_label = Label(self.tk, text = "Loading...")
            loading_label.pack(side=BOTTOM, fill=BOTH)
            filename = filedialog.askopenfilename(initialdir=self.userPath.get(), 
                                                    title="Select a File", 
                                                    filetypes=(("MP4 File", "*.mp4*"), 
                                                                ("All Files", "*.*")))
            
            vid_size = round(os.path.getsize(filename) / 1000000, 1)
            duration = round(float(get_duration(filename)))
            self.file_size_label.config(text = "Video Size: " + str(vid_size) + " MB")
            self.duration_label.config(text = "Video Duration: " + str(duration) + " seconds")

           
            '''if self.calc_var > 1:
                file_size_label.pack_forget()
                duration_label.pack_forget()'''
                
            self.file_size_label.pack(ipadx=60, ipady=10)
                #side=RIGHT, fill=BOTH
                # display the video duration
                
            self.duration_label.pack(ipadx=60, ipady=10)

            # display file size 
            '''if self.calc_var == 1:
                
                
                self.file_size_label.pack(ipadx=60, ipady=10)
                #side=RIGHT, fill=BOTH
                # display the video duration
                
                self.duration_label.pack(ipadx=60, ipady=10)
            else:
                self.file_size_label.pack_forget()
                self.duration_label.pack_forget()
                
                self.file_size_label.pack(ipadx=60, ipady=10)
                #side=RIGHT, fill=BOTH
                # display the video duration
                
                self.duration_label.pack(ipadx=60, ipady=10)'''
#side=BOTTOM, pady = 10
            # json holds the function analyze bitrate
            json = analyze_bitrate(filename)
            graph_title = Path(filename).name
            graph_filename = Path(filename).stem

            # creates the graph image file
            plot_results(json, graph_title, graph_filename, self.historyPath.get())
            loading_label.pack_forget()

            # add new plots to history.
        
        self.calcBtn = Button(self.tk, text = "Calculate")
        self.calcBtn.bind('<Button-1>',getStats)
        self.calcBtn.pack()
#side=LEFT, padx=20, pady=20

def main():
    root = Tk()
    window = Window(root)
    window.getPath()
    window.clearFolder()
    window.createHistory()
    window.calculate()
    root.mainloop()

if __name__ == "__main__":
    main()