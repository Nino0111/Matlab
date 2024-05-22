import customtkinter
import sqlite3
import bcrypt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
#APP WINDOW 
app = customtkinter.CTk()
app.title('Artwork Inventory and Exhibition Management System')
app.geometry('600x480')
app.config(bg='#FFFFFF')
app.resizable(FALSE, FALSE)

 #FONTS USED
font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold', 'underline')
font5 = ('Arial', 10, 'bold')

#CONNECTING WITH THE DATA BASE
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# TABLES FOR DATA BASE
cursor.execute('''CREATE TABLE IF NOT EXISTS Users(username TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS ArtworkInventory(first TEXT, last TEXT, type TEXT, name TEXT, date TEXT)''')

# THE FUNCTION FOR VALUES OF VARIABLES
def artwork_inventory():

    first = First_entry.get()
    last = Last_entry.get()
    type = type_option.get()
    date = date_entry.get()
    name = name_entry.get()
    
    if first and last and type and date and name:
        
        cursor.execute('SELECT name FROM ArtworkInventory WHERE name=?', (name,))
        
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'The Artwork is already Listed ')
       
        else:
            cursor.execute('INSERT INTO ArtworkInventory (first, last, type, date, name) VALUES (?, ?, ?, ?, ?)',
                           (first, last, type, date, name))
            conn.commit()
            messagebox.showinfo('Success', 'Info Inputted in the System.')
            First_entry.delete(0, END)
            Last_entry.delete(0, END)
            date_entry.delete(0, END)
            name_entry.delete(0, END)
            add_to_treeview()
    else:
        messagebox.showerror('Error', 'ENTER VALID DATA!')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'IT IS ALREADY EXISTED')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            messagebox.showinfo('The account has been created.')
            show_login()
    else:
        messagebox.showerror('Error', 'ENTER VALID DATA')


def login_account():
    
    username = username_entry2.get()
    password = password_entry2.get()
   
    if username and password:
        
        cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        
        result = cursor.fetchone()
        
        if result:
            
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('WELCOME', 'YOU HAVE BEEN LOG IN')
                Adoption_frame()
            
            else:
                messagebox.showerror('Error', 'Invalid password')
        
        else:
            messagebox.showerror('Error', 'Invalid Username')
    
    else:
        messagebox.showerror('Error', 'ENTER VALID DATA!')


def show_signup():
    frame2.destroy()
    show_signup_frame()


def show_login():
    frame1.destroy()
    show_login_frame()


def Adoption_page():
    frame2.destroy()
    Adoption_frame()


def add_to_treeview():
    cursor.execute('SELECT * FROM ArtworkInventory')
    infos = cursor.fetchall()
    tree.delete(*tree.get_children())
    for info in infos:
        tree.insert('', END, values=info)


def delete():
    
    selected_item = tree.focus()
   
    if not selected_item:
        messagebox.showerror('ERROR', 'CHOOSE INFORMATION')
   
    else:
       
        name = tree.item(selected_item)['values'][3]
        
        try:
            cursor.execute('DELETE FROM ArtworkInventory WHERE name = ?', (name,))
            conn.commit()
            add_to_treeview()
            messagebox.showinfo('DELETED DATA!')
       
        except Exception as e:
            messagebox.showerror('ERROR', f'Failed to delete data: {e}')


def update():
    
    selected_item = tree.focus()
    
    if not selected_item:
        messagebox.showerror('Error', 'SELECT TO UPDATE')

    else:
        
        first = First_entry.get()
        last = Last_entry.get()
        type = type_option.get()
        date = date_entry.get()
        name = name_entry.get()

        
        if not (first and last and type and date and name):
            messagebox.showerror('Error', 'Enter all data!')
            return

        
        original_info = tree.item(selected_item)['values'][3]

        
        cursor.execute('''
            UPDATE ArtworkInventory
            SET first = ?, last = ?, type = ?, date = ?, name = ?
            WHERE name = ?
        ''', (first, last, type, date, name, original_info))
        
        conn.commit()

         
        add_to_treeview()
        messagebox.showinfo('Data has been updated')

        
        First_entry.delete(0, END)
        Last_entry.delete(0, END)
        date_entry.delete(0, END)
        name_entry.delete(0, END)



def Adoption_frame():
   
    global frame3, First_entry, Last_entry, type_option, date_entry, name_entry, tree

    
    frame3 = customtkinter.CTkFrame(app, bg_color='#FFFDD0', fg_color='#FFFDD0', width=600, height=480)
    frame3.pack(fill='both', expand=True)

    
    frameT = customtkinter.CTkFrame(frame3, bg_color='#FFFDD0', fg_color='#FFFDD0', width=600, height=180)
    frameT.grid(row=0, column=0, sticky='n')

    
    options = ['1', '2', '3', '4','5']
    variable1 = StringVar()

    
    type_label = customtkinter.CTkLabel(frameT, font=font2, text='Quantity:', text_color='#00CFB6', bg_color='#FFFDD0')
    type_label.grid(row=0, column=2, padx=10)

    
    type_option = customtkinter.CTkComboBox(frameT, font=font2, text_color='#fff', fg_color='#111111',
                                             dropdown_hover_color='#00B29D', button_color='#00CFB6',
                                             button_hover_color='#00B29D', border_color='#00CFB6', dropdown_fg_color='#00CFB6',
                                             width=165, variable=variable1, values=options, state='readonly')
    
    type_option.set('1')
    type_option.grid(row=1, column=2, padx=10)

    
    First_label = customtkinter.CTkLabel(frameT, font=font2, text='Artist Name:', text_color='#00CFB6', bg_color='#FFFDD0')
    First_label.grid(row=0, column=0, padx=10)

    
    First_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#fff', fg_color='#111111', placeholder_text='Artist Name',
                                         border_color='#00CFB6', border_width=2, width=165)
    First_entry.grid(row=1, column=0, padx=10)

   
    Last_label = customtkinter.CTkLabel(frameT, font=font2, text='Title :', text_color='#00CFB6', bg_color='#FFFDD0')
    Last_label.grid(row=0, column=1, padx=10)
    
    
    Last_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#fff', fg_color='#000', placeholder_text='Title',
                                        border_color='#00CFB6', border_width=2, width=165)
    Last_entry.grid(row=1, column=1, padx=10)
    
    
    date_label = customtkinter.CTkLabel(frameT, font=font2, text='Date of exhibition', text_color='#00CFB6', bg_color='#FFFDD0')
    date_label.grid(row=2, column=0, padx=10)

    
    date_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#fff', fg_color='#111111', placeholder_text='Date (YYYY-MM-DD)',
                                        border_color='#00CFB6', border_width=2, width=165)
    date_entry.grid(row=3, column=0, padx=10)

    
    name_label = customtkinter.CTkLabel(frameT, font=font2, text='Year Made:', text_color='#00CFB6', bg_color='#FFFDD0')
    name_label.grid(row=2, column=1, padx=10)

    
    name_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#fff', fg_color='#111111', placeholder_text='Year Made',
                                        border_color='#00CFB6', border_width=2, width=165)
    name_entry.grid(row=3, column=1, padx=10)

    
    insert_button = customtkinter.CTkButton(frameT, command= artwork_inventory, font=font2, text_color='#fff', text='Insert Info',
                                            fg_color='#00CFB6', hover_color='#00B29D', bg_color='#FFFDD0', cursor='hand2',
                                            corner_radius=5, width=165)
    insert_button.grid(row=4, column=1, padx=10, pady=5)


    frameM = customtkinter.CTkFrame(frame3, bg_color='#FFFDD0', fg_color='#FFFDD0', width=1000, height=350)
    frameM.grid(row=1, column=0, sticky='nsew', padx=70, pady=10)

    
    style = ttk.Style(frameM)
    style.theme_use('clam')
    
    style.configure('Treeview', font=font3, foreground='#000', background='#00B29D', fieldbackground='#000')
    
    style.configure('Treeview.Heading', font=font3, foreground='#fff', background='#008978', relief='flat')
    
    style.map('Treeview', background=[('selected', '#00A994')])
    style.map('Treeview.Heading', background=[('active', '#008978')])

   
    tree = ttk.Treeview(frameM, height=6)
    tree['columns'] = ('Artist Name', 'Title', 'Quantity', 'Pet name', 'Date adopted')

    
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Artist Name', anchor=tk.CENTER, width=110)
    tree.column('Title', anchor=tk.CENTER, width=110)
    tree.column('Quantity', anchor=tk.CENTER, width=110)
    tree.column('Pet name', anchor=tk.CENTER, width=110)
    tree.column('Date adopted', anchor=tk.CENTER, width=110)

   
    tree.heading('Artist Name', text='Artist Name')
    tree.heading('Title', text='Title')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Pet name', text='Year Made')
    tree.heading('Date adopted', text='Date of Exhibition')

    tree.grid(row=0, column=0, padx=60, pady=20, sticky='nsew')

    
    frameB = customtkinter.CTkFrame(frame3, bg_color='#FFFDD0', fg_color='#FFFDD0', width=600, height=100)
    frameB.grid(row=2, column=0, sticky='n')

    
    edit_button = customtkinter.CTkButton(frameB, command=update, font=font2, text_color='#fff', text='Edit Info',
                                            fg_color='#00CFB6', hover_color='#00B29D', bg_color='#FFFDD0', cursor='hand2',
                                            corner_radius=5, width=165)
    edit_button.grid(row=0, column=0, padx=10, pady=5)

    
    delete_button = customtkinter.CTkButton(frameB, command=delete, font=font2, text_color='#fff', text='Delete Info',
                                            fg_color='#00CFB6', hover_color='#00B29D', bg_color='#FFFDD0', cursor='hand2',
                                            corner_radius=5, width=165)
    delete_button.grid(row=0, column=1, padx=10, pady=5)

    
    add_to_treeview()



def show_signup_frame():
   
    global frame1, username_entry, password_entry
    
    
    frame1 = customtkinter.CTkFrame(app, fg_color='#FFFDD0', width=600, height=480)
    frame1.place(x=0, y=0)
    
    frameR = customtkinter.CTkFrame(frame1, fg_color='#FFFDD0', width=300, height=480)
    frameR.pack(expand=True, side=RIGHT)

    
    image1 = Image.open("2.jpeg")
    side_img = customtkinter.CTkImage(dark_image=image1, light_image=image1, size=(300, 480))
    customtkinter.CTkLabel(master=frame1, text="", image=side_img).pack(expand=True, side=LEFT)

   
    signup_label = customtkinter.CTkLabel(frameR, font=font1, text='Sign Up', text_color='#00CFB6', bg_color='#FFFDD0')
    signup_label.place(x=30, y=20)

   
    user_label = customtkinter.CTkLabel(frameR, font=font3, text='Username:', text_color='#00CFB6', bg_color='#FFFDD0')
    user_label.place(x=30, y=105)
    
    
    username_entry = customtkinter.CTkEntry(frameR, font=font2, text_color='#000', fg_color='#FFFDD0',
                                            bg_color='#FFFDD0', border_color='#00CFB6', border_width=3,
                                            width=245, height=50)
    username_entry.place(x=30, y=130)

    
    pass_label = customtkinter.CTkLabel(frameR, font=font3, text='Password:', text_color='#00CFB6', bg_color='#FFFDD0')
    pass_label.place(x=30, y=195)

    
    password_entry = customtkinter.CTkEntry(frameR, font=font2, show='*', text_color='#000',
                                            fg_color='#FFFDD0', bg_color='#FFFDD0', border_color='#00CFB6',
                                            border_width=3, width=245, height=50)
    password_entry.place(x=30, y=220)

    
    signup_button = customtkinter.CTkButton(frameR, command=signup, font=font2, text_color='#fff',
                                            text='Sign up', fg_color='#00CFB6', hover_color='#00B29D',
                                            bg_color='#FFFDD0', cursor='hand2', corner_radius=5, width=245)
    signup_button.place(x=30, y=320)

   
    login_button = customtkinter.CTkButton(frameR, command=show_login, font=font2, text_color='#fff',
                                           text='Log in', fg_color='#000', hover_color='#232323',
                                           bg_color='#FFFDD0', border_color='#00CFB6', border_width=2,
                                           cursor='hand2', corner_radius=5, width=245)
    login_button.place(x=30, y=370)


def show_login_frame():
    global frame2, username_entry2, password_entry2
    frame2 = customtkinter.CTkFrame(app, width=600, height=480)
    frame2.place(x=0, y=0)
    frameR = customtkinter.CTkFrame(frame2, fg_color='#FFFDD0', width=300, height=480)
    frameR.pack(expand=True, side=RIGHT)

    image1 = Image.open("2.jpeg")
    side_img = customtkinter.CTkImage(dark_image=image1, light_image=image1, size=(300, 480))
    customtkinter.CTkLabel(master=frame2, text="", image=side_img).pack(expand=True, side=LEFT)

    
    login_label2 = customtkinter.CTkLabel(frameR, font=font1, text='Log in', text_color='#6495ed', bg_color='#FFFDD0')
    login_label2.place(x=30, y=20)

    
    user_label = customtkinter.CTkLabel(frameR, font=font3, text='Username:', text_color='#6495ed', bg_color='#FFFDD0')
    user_label.place(x=30, y=105)

    
    username_entry2 = customtkinter.CTkEntry(frameR, font=font2, text_color='#6495ed', fg_color='#FFFDD0',
                                             bg_color='#FFFDD0', border_color='#6495ed', border_width=3,
                                             width=245, height=50)
    username_entry2.place(x=30, y=130)

    
    pass_label = customtkinter.CTkLabel(frameR, font=font3, text='Password:', text_color='#6495ed', bg_color='#FFFDD0')
    pass_label.place(x=30, y=195)

    
    password_entry2 = customtkinter.CTkEntry(frameR, font=font2, show='*', text_color='#6495ed',
                                             fg_color='#FFFDD0', bg_color='#FFFDD0', border_color='#6495ed',
                                             border_width=3, width=245, height=50)
    password_entry2.place(x=30, y=220)

    
    login_button2 = customtkinter.CTkButton(frameR, command=login_account, font=font2, text_color='#fff',
                                            text='Log in', fg_color='#6495ed', hover_color='#00B29D',
                                            bg_color='#FFFDD0', cursor='hand2', corner_radius=5, width=245)
    login_button2.place(x=30, y=320)

    
    signup_button2 = customtkinter.CTkButton(frameR, command=show_signup, font=font2, text_color='#fff',
                                             text='Sign up', fg_color='#6495ed', hover_color='#232323',
                                             bg_color='#FFFDD0', border_color='#00CFB6', border_width=2,
                                             cursor='hand2', corner_radius=5, width=245)
    signup_button2.place(x=30, y=370)


show_login_frame()


def on_closing():
    conn.close()
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)


app.mainloop()