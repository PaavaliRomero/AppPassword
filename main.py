from gui_interface import myWindowAppPass
import tkinter as tk

def main():
    root = tk.Tk()
    app = myWindowAppPass(root)
    root.mainloop()

if __name__ == "__main__":
    main()