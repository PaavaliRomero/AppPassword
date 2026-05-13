
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from random import *
import json
from data_manager import Generate_random_password

FILE_LOGO = 'Class_29_GUI_appPass/Image/logo.png'
EMAIL_DEFAULT = 'romero.paavali@gmail.com'

# ---------------------------- UI SETUP ------------------------------- #
class myWindowAppPass:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.config(padx=20, pady=20)

        #Images
        self.canvas = Canvas(self.root, width=200, height=200)
        self.imgLock = PhotoImage(file=FILE_LOGO)
        self.canvas.create_image(100, 100, image=self.imgLock, anchor="center")
        self.canvas.grid(column=1, row=0)

        #Labels
        self.Lb_Website = tk.Label(text="Website:")
        self.Lb_Website.grid(column=0, row=1)
        self.Lb_EmailUser = tk.Label(text="Email/Username:")
        self.Lb_EmailUser.grid(column=0,row=2)
        self.Lb_Password = tk.Label(text="Password:")
        self.Lb_Password.grid(column=0, row=3)

        #Entries
        self.Et_Website_In = tk.Entry(width=21)
        self.Et_Website_In.grid(column=1,row=1)
        self.Et_Website_In.focus()

        self.Et_EmailUse_In = tk.Entry(width=39)
        self.Et_EmailUse_In.grid(column=1,row=2, columnspan=2)
        self.Et_EmailUse_In.insert(0, EMAIL_DEFAULT)

        self.Et_Password_In = tk.Entry(width=21)
        self.Et_Password_In.grid(column=1,row=3)

        #Butons
        self.Bt_GeneratePass = tk.Button(text="Generate Password", command=self.GeneratePassword_Func_BT, width=14)
        self.Bt_GeneratePass.grid(column=2, row=3)

        self.Bt_AddEmail = tk.Button(text="Add", command=self.SaveData_Func_BT, width=36)
        self.Bt_AddEmail.grid(column=1, row=4, columnspan=2)

        self.Bt_Search = tk.Button(text="Search", command=self.find_password_Func_BT, width=14)
        self.Bt_Search.grid(column=2, row=1)
        

    def GeneratePassword_Func_BT(self):
        password_list = Generate_random_password()
        password = "".join(password_list)

        self.Et_Password_In.delete(0,END)
        self.Et_Password_In.insert(0, password)

    # ---------------------------- SEARCH ----------------------------------------- #
    def find_password_Func_BT(self):
        try:
            with open('Class_29_GUI_appPass/data/data.json','r') as FileData:
                read = json.load(FileData)
        except FileNotFoundError:
            messagebox.showinfo(title="Error",message=f"No file data found.")
        else:
            website = self.Et_Website_In.get()        
            if website in read:
                email = read[website]['email']
                password = read[website]['password']
                messagebox.showinfo(message=f"Email:{email} \nPassword:{password}")
            else:        
                messagebox.showinfo(title="Error",message=f"no details for {website} exists.")

        # ---------------------------- SAVE PASSWORD ------------------------------- #
    def SaveData_Func_BT(self):
        password = str(self.Et_Password_In.get())
        website = str(self.Et_Website_In.get())
        emailUser = str(self.Et_EmailUse_In.get())
            
        new_data ={
            website: {
                "email": emailUser,
                "password": password,
            }
        }

        if not (password and website):
            messagebox.showinfo(message="Empty entries. Please try again.")
            return
        else:
            try:
                with open('Class_29_GUI_appPass/data/data.json','r') as FileData:
                    data = json.load(FileData)
            except FileNotFoundError:
                with open('Class_29_GUI_appPass/data/data.json','w') as FileData:
                    json.dump(new_data, FileData, indent=4)
            else:
                data.update(new_data)

                with open('Class_29_GUI_appPass/data/data.json','w') as FileData:
                    json.dump(data, FileData, indent=4)
                
            self.Et_Password_In.delete(0,END)
            self.Et_Website_In.delete(0,END)