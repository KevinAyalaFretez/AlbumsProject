import tkinter as tk
from tkinter import messagebox
from tkinter import *
from Database_Connection import get_db_connection
import Database_Connection
from PIL import Image,ImageTk
from tkinter import ttk


def open_firstpage():
    #Create the new window
    tree_window = tk.Toplevel(root)
    tree_window.title("2023")
    tree_window.geometry("800x500")

    #Create Treeview
    tree = ttk.Treeview(tree_window, columns=("Artist", "Album"), show='headings')
    tree.heading("Artist", text="Artist")
    tree.heading("Album", text="Album")
    tree.pack(expand=True, fill="both", padx=20, pady=20)

    # Connect to DB and fetch data
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Artist, Album FROM [2023]")
            rows = cursor.fetchall()

            # Insert rows into Treeview
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Connection Error", "Could not connect to the database")

    # Creating labels and entry fields
    Label(tree_window, text="Artist").pack(pady=5)
    artist_entry = tk.Entry(tree_window, width=25)
    artist_entry.pack(pady=5)

    Label(tree_window, text="Album").pack(pady=5)
    album_entry = tk.Entry(tree_window, width=25)
    album_entry.pack(pady=5)

    def register_album():
        artist = artist_entry.get()
        album = album_entry.get()
    
    # conditions
        if not artist or not album:
            messagebox.showerror("Error","Please fill in all fields")
        else:
            #Inserting the database
            conn = Database_Connection.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insert into 2023 table
                    query = "INSERT INTO [2023] (Artist, Album) VALUES (?, ?)"
                    cursor.execute(query, (artist, album))
                    conn.commit()
                    messagebox.showinfo("Success", "Done")
                    tree_window.destroy()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to register: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showinfo("Success","Done")
                tree_window.destroy()

    #Button
    button_frame = Frame(tree_window)
    button_frame.pack(pady=15)

    Button(button_frame, text="Register", command=register_album, bg=("green")).pack(side=LEFT,padx=5)

     # Optional: Close button
    tk.Button(tree_window, text="Close", command=tree_window.destroy).pack(pady=10)


## Create the Welcome Screen window
root = tk.Tk()
root.title("Albums")
root.geometry("800x500")

#Create a frame
frame = tk.Frame(root, padx=100, pady=100)
frame.pack(pady=100)

Button1 = tk.Button(root, text="2023", font=("",20),command=open_firstpage)
Button1.pack(pady=5)

root.mainloop()