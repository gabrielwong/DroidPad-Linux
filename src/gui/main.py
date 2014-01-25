'''
Created on Jan 24, 2014

@author: gabriel
'''
import Tkinter as tk

TITLE = "DroidPad"

# Our frame
class DroidFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.parent.title(TITLE)
        self.pack(fill=tk.BOTH, expand=1)

def main():
    root = tk.Tk()
    root.geometry("500x500+200+100")
    app = DroidFrame(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()