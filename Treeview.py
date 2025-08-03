import tkinter as tk
from tkinter import ttk, messagebox

# Function to handle item selection
def on_item_select(event):
    selected_item = tree.focus()  # Get the selected item
    item_values = tree.item(selected_item, "values")  # Retrieve values
    if item_values:
        messagebox.showinfo("Selection", f"You selected: {item_values}")

# Create the main window
root = tk.Tk()
root.title("Treeview Event Binding")
root.geometry("400x300")

# Create a Treeview widget
tree = ttk.Treeview(root)

# Define columns
tree["columns"] = ("Name", "Age", "City")

# Format columns
tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
tree.column("Name", anchor=tk.W, width=120)
tree.column("Age", anchor=tk.CENTER, width=50)
tree.column("City", anchor=tk.W, width=120)

# Create headings
tree.heading("Name", text="Name", anchor=tk.W)
tree.heading("Age", text="Age", anchor=tk.CENTER)
tree.heading("City", text="City", anchor=tk.W)

# Add sample data
tree.insert("", "end", values=("Alice", 25, "New York"))
tree.insert("", "end", values=("Bob", 30, "London"))
tree.insert("", "end", values=("Charlie", 22, "Paris"))

# Bind event to detect selection
tree.bind("<<TreeviewSelect>>", on_item_select)

# Pack the Treeview widget
tree.pack(pady=20, fill="both", expand=True)

# Run the application
root.mainloop()