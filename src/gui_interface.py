from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from data_manager import Generate_random_password, Encrypted_Message, Decrypted_Message

BASE_DIR = Path(__file__).parent.parent

FILE_LOGO = BASE_DIR/"Image"/"logo.png"
FILE_DATA = BASE_DIR/"data"/"data.json"
EMAIL_DEFAULT = 'email@domain.com'

# ---------------------------- UI SETUP ------------------------------- #
class myWindowAppPass:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        icono = tk.PhotoImage(file=FILE_LOGO)
        self.root.iconphoto(True, icono)
        self.root.config(padx=20, pady=20)

        #Images-------------------------------------------------------
        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.imgLock = tk.PhotoImage(file=FILE_LOGO)
        self.canvas.create_image(100, 100, image=self.imgLock, anchor="center")
        self.canvas.grid(column=1, row=0)

        #Labels-------------------------------------------------------
        self.Lb_Website = tk.Label(text="Website:")
        self.Lb_Website.grid(column=0, row=1)
        self.Lb_EmailUser = tk.Label(text="Email/Username:")
        self.Lb_EmailUser.grid(column=0,row=2)
        self.Lb_Password = tk.Label(text="Password:")
        self.Lb_Password.grid(column=0, row=3)

        #Frame PasswordEntry-ButtonShow-------------------------------
        self.Frame_Pass = tk.Frame(self.root)
        self.Frame_Pass.grid(column=1,row=3)

        #Entries------------------------------------------------------
        self.Et_Website_In = tk.Entry(width=23)
        self.Et_Website_In.grid(column=1,row=1)
        self.Et_Website_In.focus()

        self.Et_EmailUse_In = tk.Entry(width=41)
        self.Et_EmailUse_In.grid(column=1,row=2, columnspan=2)
        self.Et_EmailUse_In.insert(0, EMAIL_DEFAULT)

        self.Et_Password_In = tk.Entry(self.Frame_Pass, width=18, show='*')
        self.Et_Password_In.pack(side=tk.LEFT, fill=tk.X, expand=True)

        #Butons-------------------------------------------------------
        self.Bt_GeneratePass = tk.Button(text="Generate Password", command=self.GeneratePassword_Func_BT, width=14)
        self.Bt_GeneratePass.grid(column=2, row=3)

        self.Bt_AddEmail = tk.Button(text="Add", command=self.SaveData_Func_BT, width=14)
        self.Bt_AddEmail.grid(column=1, row=4)

        self.Bt_Search = tk.Button(text="Search", command=self.find_password_Func_BT, width=14)
        self.Bt_Search.grid(column=2, row=1)

        self.Bt_Delate = tk.Button(text="Delate", command=self.Delate_Func_BT, width=14)
        self.Bt_Delate.grid(column=2, row=4)

        self.Bt_ShowPass = tk.Button(self.Frame_Pass,text="👁", command=self.TogglePasswordShow, width=2)
        self.Bt_ShowPass.pack(side=tk.LEFT)

    def TogglePasswordShow(self):
        current = self.Et_Password_In.cget('show')
        self.Et_Password_In.config(show='' if current == '*' else '*')
        
    def Delate_Func_BT(self):
        try:
            with open(FILE_DATA, 'rb') as FileData:
                data = Decrypted_Message(FileData.read())
        except FileNotFoundError:
            messagebox.showinfo(title="Error",message=f"No file data found.")
        else:
            website = self.Et_Website_In.get()
            if website in data:
                del data[website]
                with open(FILE_DATA, 'wb') as FileData:
                    FileData.write(Encrypted_Message(data))

                self.Et_EmailUse_In.delete(0, tk.END)
                self.Et_Password_In.delete(0, tk.END)
                self.Et_Website_In.delete(0, tk.END)
            
                messagebox.showinfo(message=f"Delate: {website} in data file")
            else:
                messagebox.showinfo(title="Error", message=f"Fail delated data in data file")

    def GeneratePassword_Func_BT(self):
        #Generate Password
        password_list = Generate_random_password()
        password = "".join(password_list)

        #Copy Password
        self.root.clipboard_clear()
        self.root.clipboard_append(password)

        #Delate Password
        self.Et_Password_In.delete(0,tk.END)
        self.Et_Password_In.insert(0, password)

    # ---------------------------- SEARCH ----------------------------------------- #
    def find_password_Func_BT(self):
        try:
            with open(FILE_DATA,'rb') as FileData:
                read = Decrypted_Message(FileData.read())
        except FileNotFoundError:
            messagebox.showinfo(title="Error",message=f"No file data found.")
        else:
            website = self.Et_Website_In.get()        
            if website in read:
                email = read[website]['email']
                password = read[website]['password']
                #Paste user data
                self.Et_EmailUse_In.delete(0, tk.END)
                self.Et_Password_In.delete(0, tk.END)
                self.Et_EmailUse_In.insert(0, email)
                self.Et_Password_In.insert(0, password)
                #Copy Password
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo(message=f"Email:{email} \nPassword:{password} \n\nCopied to clipboard!")
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
                with open(FILE_DATA,'rb') as FileData:
                    data = Decrypted_Message(FileData.read())
            except FileNotFoundError:
                #if data file does't exist
                with open(FILE_DATA,'wb') as FileData:
                    FileData.write(Encrypted_Message(new_data))
                    
            else:
                #if data file exist
                data.update(new_data)
                with open(FILE_DATA,'wb') as FileData:
                    FileData.write(Encrypted_Message(data))
                
                messagebox.showinfo(message="Data saved successfully.")
            
            self.Et_Password_In.delete(0,tk.END)
            self.Et_Website_In.delete(0,tk.END)
