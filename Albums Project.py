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

    #Create Treeview, in show we put headings and tree to detect both, otherwise will detect only the columns without the number
    tree = ttk.Treeview(tree_window, columns=("Artist", "Album"), show=('headings','tree'))

    #Create the column 0 for the numbers next to the artist
    tree.column("#0", width=40, anchor='center')
    tree.heading("#0", text="Num")

    #Create the columns
    tree.heading("Artist", text="Artist")
    tree.heading("Album", text="Album")
    tree.pack(expand=True, fill="both", padx=20, pady=20)

    # Connect to DB and fetch data
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Artist, Album FROM [2023] ORDER BY ID")
            rows = cursor.fetchall()

            # Fetch unique artists for the combobox
            cursor.execute("SELECT DISTINCT Artist FROM [2023] ORDER BY Artist")
            # The code after artists it's useful for extract only the name of each row
            artists = [row[0] for row in cursor.fetchall()]

            # Insert rows into Treeview
            for i, row in enumerate(rows, 1): # The '1' makes the count start from 1 instead of 0
                artist, album = row
            # The 'text' parameter of insert() populates the #0 column
                tree.insert("", "end", text=i, values=(artist, album))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Connection Error", "Could not connect to the database")

    # Creating labels and entry fields
    Label(tree_window, text="Artist").pack(pady=5)
    artist_entry = ttk.Combobox(tree_window, width=22)

    # Set the values for the dropdown list
    artist_entry['values'] = artists
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
                    # Get the next number based on the current number of children in the tree
                    new_number = len(tree.get_children()) + 1
                    tree.insert("", "end", text=new_number, values=(artist, album))
                    messagebox.showinfo("Success", "Done")
                    # Clear the entry fields after successful registration
                    artist_entry.delete(0, 'end')
                    album_entry.delete(0, 'end')
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to register: {e}")
                finally:
                    conn.close()

    def delete_album():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select an entry to delete.")
            return

    # Get the selected row values
        item = tree.item(selected_item[0])
        values = item['values']

        if len(values) < 2:
            messagebox.showerror("Error", "The selected item does not have both Artist and Album.")
            return

        artist, album = values[0], values[1]

    # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Delete '{album}' by {artist}?")
        if not confirm:
         return

    # Connect to DB and delete
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "DELETE FROM [2023] WHERE Artist = ? AND Album = ?"
                cursor.execute(query, (artist, album))
                conn.commit()

            # Remove from Treeview
                tree.delete(selected_item[0])
                messagebox.showinfo("Deleted", f"'{album}' by {artist} was deleted.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Connection Error", "Could not connect to the database.")

    #Button
    button_frame = Frame(tree_window)
    button_frame.pack(pady=15)

    Button(button_frame, text="Register", command=register_album, bg=("green")).pack(side=LEFT,padx=5)

    Button(button_frame, text="Delete", command=delete_album, bg=("red")).pack(side=LEFT,padx=5)
    
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

#Button1 = tk.Button(root, text="2024", font=("",20),command=open_secondpage)
#Button1.pack(pady=5)

# Button1 = tk.Button(root, text="2025", font=("",20),command=open_thirdpage)
# Button1.pack(pady=5)

root.mainloop()