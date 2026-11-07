import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

#load books
def load_books():
    books = {}

    try:
        with open(os.path.join(os.path.dirname(__file__),"books.csv"), "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                book_id = int(row["book_id"])
                books[book_id] = {
                    "title": row["title"],
                    "author": row["author"],
                    "status": row.get("status", "Available")
                }

    except FileNotFoundError:
        print("books.csv was not found.")

    return books

#save books
def save_books(books):
    filename = os.path.join(os.path.dirname(__file__), "books.csv")

    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["book_id", "title", "author", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for book_id, info in books.items():
            writer.writerow({
                "book_id": book_id,
                "title": info["title"],
                "author": info["author"],
                "status": info["status"]
            })


def get_book_id(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

#add a new book
def add_book(books):
    book_id = get_book_id("Enter Book ID: ")

    if book_id in books:
        print("Book ID already exists.")
        return

    title = input("Enter Book Title: ").strip()
    author = input("Enter Author's name: ").strip()

    if not title or not author:
        print("Title and author cannot be empty.")
        return

    books[book_id] = {
        "title": title,
        "author": author,
        "status": "Available"
    }
    save_books(books)
    print("Book added successfully.")

#view books
def view_books(books):
    if not books:
        print("No books found.")
        return

    print("\n--- Library Books ---")
    for book_id, info in books.items():
        print(
            f"ID: {book_id} | Title: {info['title']} | "
            f"Author: {info['author']} | Status: {info['status']}"
        )

#search any book
def search_books(books):
    query = input("Search by title or author: ").strip().lower()

    matches = [
        (book_id, info)
        for book_id, info in books.items()
        if query in info["title"].lower()
        or query in info["author"].lower()
    ]

    if not matches:
        print("No matching books found.")
        return

    for book_id, info in matches:
        print(
            f"ID: {book_id} | Title: {info['title']} | "
            f"Author: {info['author']} | Status: {info['status']}"
        )

#issue a book
def issue_book(books):
    book_id = get_book_id("Enter Book ID to issue: ")

    if book_id not in books:
        print("Book ID not found.")
    elif books[book_id]["status"] == "Issued":
        print("Book is already issued.")
    else:
        books[book_id]["status"] = "Issued"
        save_books(books)
        print("Book issued.")

#return a book
def return_book(books):
    book_id = get_book_id("Enter Book ID to return: ")

    if book_id not in books:
        print("Book ID not found.")
    elif books[book_id]["status"] == "Available":
        print("Book is not currently issued.")
    else:
        books[book_id]["status"] = "Available"
        save_books(books)
        print("Book returned successfully.")

#gui
def main():
    books = load_books()
 
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("1000x600")
    root.minsize(800, 450)
    root.configure(bg="#FFF5F8")
 
    style = ttk.Style()
    style.theme_use("clam")
 
    # ---------- Colors ----------
    pink = "#D95D8F"
    dark_pink = "#BD4778"
    pale_pink = "#FFF5F8"
    soft_pink = "#F3DCE6"
    white = "#FFFFFF"
    black = "#241B22"
    muted = "#705C66"
    green, green_dark = "#16A34A", "#15803D"
    orange, orange_dark = "#EA580C", "#C2410C"
 
    # ---------- Frame & label styles ----------
    style.configure("Sidebar.TFrame", background=black)
    style.configure("Content.TFrame", background=pale_pink)
    style.configure("Card.TFrame", background=white, relief="solid", borderwidth=1)
 
    style.configure("SidebarTitle.TLabel", background=black, foreground=white,
                    font=("Segoe UI", 15, "bold"))
    style.configure("PageTitle.TLabel", background=pale_pink, foreground=black,
                    font=("Segoe UI", 24, "bold"))
    style.configure("Subtitle.TLabel", background=pale_pink, foreground=muted,
                    font=("Segoe UI", 11))
    style.configure("CardLabel.TLabel", background=white, foreground=black,
                    font=("Segoe UI", 22, "bold"))
    style.configure("CardCaption.TLabel", background=white, foreground=muted,
                    font=("Segoe UI", 10))
 
    # ---------- Sidebar buttons ----------
    # focusthickness=0 removes the outline clam draws around the last-clicked button
    style.configure("Nav.TButton", background=black, foreground=white,
                    font=("Segoe UI Symbol", 11), padding=(14, 10), anchor="w",
                    borderwidth=0, focusthickness=0, focuscolor=black)
    style.map("Nav.TButton",
              background=[("active", pink)],
              foreground=[("active", white)])
 
    # Same look, but pink: used for the page you're currently on
    style.configure("NavActive.TButton", background=pink, foreground=white,
                    font=("Segoe UI Symbol", 11), padding=(14, 10), anchor="w",
                    borderwidth=0, focusthickness=0, focuscolor=pink)
    style.map("NavActive.TButton", background=[("active", pink)])
 
    # ---------- Action buttons (flat, no grey border) ----------
    def action_button_style(name, bg, hover):
        style.configure(name, background=bg, foreground=white,
                        font=("Segoe UI", 10, "bold"), padding=(14, 9),
                        borderwidth=0, focusthickness=0, focuscolor=bg)
        style.map(name, background=[("active", hover)])
 
    action_button_style("Accent.TButton", pink, dark_pink)
    action_button_style("Green.TButton", green, green_dark)
    action_button_style("Orange.TButton", orange, orange_dark)
 
    # ---------- Table & scrollbar ----------
    style.configure("Treeview", background=white, fieldbackground=white,
                    foreground=black, rowheight=30, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", background=soft_pink, foreground=black,
                    font=("Segoe UI", 10, "bold"), padding=8)
    style.map("Treeview",
              background=[("selected", soft_pink)],
              foreground=[("selected", black)])
 
    style.configure("Vertical.TScrollbar", background=soft_pink,
                    troughcolor=pale_pink, bordercolor=pale_pink,
                    arrowcolor=pink, relief="flat")
    style.map("Vertical.TScrollbar", background=[("active", pink)])
 
    # ---------- Main layout ----------
    sidebar = ttk.Frame(root, width=210, style="Sidebar.TFrame")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
 
    content = ttk.Frame(root, style="Content.TFrame")
    content.pack(side="left", fill="both", expand=True)
 
    home_frame = ttk.Frame(content, style="Content.TFrame")
    books_frame = ttk.Frame(content, style="Content.TFrame")
 
    ttk.Label(sidebar, text="  📚  MY LIBRARY", style="SidebarTitle.TLabel").pack(
        anchor="w", padx=12, pady=(25, 30))
 
    # ---------- Home page ----------
    ttk.Label(home_frame, text="Library Management System",
              style="PageTitle.TLabel").pack(pady=(55, 10))
    ttk.Label(home_frame, text="Manage your books in one place",
              style="Subtitle.TLabel").pack(pady=(0, 25))
 
    # Three stat cards side by side
    cards_row = ttk.Frame(home_frame, style="Content.TFrame")
    cards_row.pack(pady=10)
 
    stat_labels = {}
    for key, caption in (("total", "Total Books"),
                         ("available", "Available"),
                         ("issued", "Issued")):
        card = ttk.Frame(cards_row, style="Card.TFrame", padding=25)
        card.pack(side="left", padx=10)
        number = ttk.Label(card, text="0", style="CardLabel.TLabel")
        number.pack()
        ttk.Label(card, text=caption, style="CardCaption.TLabel").pack()
        stat_labels[key] = number
 
    ttk.Button(home_frame, text="View Books", style="Accent.TButton",
               command=lambda: show_page(books_frame)).pack(pady=25)
 
    # ---------- Books page ----------
    columns = ("id", "title", "author", "status")
    table = ttk.Treeview(books_frame, columns=columns, show="headings")
 
    table.heading("id", text="ID")
    table.heading("title", text="Title")
    table.heading("author", text="Author")
    table.heading("status", text="Status")
 
    table.column("id", width=70, anchor="center", stretch=False)
    table.column("title", width=280, anchor="w", stretch=True)
    table.column("author", width=230, anchor="w", stretch=True)
    table.column("status", width=120, anchor="center", stretch=False)
 
    # Row text color by status (each row gets a tag matching its status)
    table.tag_configure("Available", foreground=green)
    table.tag_configure("Issued", foreground=orange)
 
    scrollbar = ttk.Scrollbar(books_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
 
    # Packing order matters: bottom buttons and the title are packed
    # BEFORE the table, otherwise the expanding table takes all the space.
    buttons = ttk.Frame(books_frame, style="Content.TFrame")
    buttons.pack(side="bottom", pady=15)
 
    header = ttk.Frame(books_frame, style="Content.TFrame")
    header.pack(side="top", fill="x")

    ttk.Label(header, text="Books", style="PageTitle.TLabel").pack(side="left")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(header, textvariable=search_var, width=28,
                             font=("Segoe UI", 10))
    search_entry.pack(side="right", ipady=4)
    ttk.Label(header, text="Search:", style="Subtitle.TLabel").pack(side="right", padx=8)
 
    scrollbar.pack(side="right", fill="y", pady=(10, 0))
    table.pack(side="top", fill="both", expand=True, pady=(10, 0))
 
    # ---------- Logic ----------
    def refresh_table():
        query = search_var.get().strip().lower()
        for item in table.get_children():
            table.delete(item)
 
        for book_id, info in books.items():
            if query and query not in info["title"].lower()\
                     and query not in info["author"].lower():
                continue

            table.insert("", "end", tags=(info["status"],),
                         values=(book_id, info["title"], info["author"], info["status"]))
 
        issued = sum(1 for b in books.values() if b["status"] == "Issued")
        stat_labels["total"].config(text=str(len(books)))
        stat_labels["available"].config(text=str(len(books) - issued))
        stat_labels["issued"].config(text=str(issued))
        
    search_var.trace_add("write", lambda *args: refresh_table())
 
    def add_book_gui():
        book_id = simpledialog.askinteger("Add book", "Enter book ID:", parent=root)
        if book_id is None:
            return
 
        if book_id in books:
            messagebox.showerror("Error", "That book ID already exists.")
            return
 
        title = simpledialog.askstring("Add book", "Enter title:", parent=root)
        if not title or not title.strip():
            return
 
        author = simpledialog.askstring("Add book", "Enter author:", parent=root)
        if not author or not author.strip():
            return
 
        books[book_id] = {
            "title": title.strip(),
            "author": author.strip(),
            "status": "Available"
        }
        save_books(books)
        refresh_table()
 
    def change_status(new_status):
        selected = table.selection()
        if not selected:
            messagebox.showinfo("Select a book", "Select a book from the table first.")
            return
 
        book_id = int(table.item(selected[0], "values")[0])
 
        if books[book_id]["status"] == new_status:
            messagebox.showinfo("Book status",
                                f"This book is already {new_status.lower()}.")
            return
 
        books[book_id]["status"] = new_status
        save_books(books)
        refresh_table()
 
    ttk.Button(buttons, text="＋  Add Book", style="Accent.TButton",
               command=add_book_gui).pack(side="left", padx=5)
    ttk.Button(buttons, text="Issue Book", style="Orange.TButton",
               command=lambda: change_status("Issued")).pack(side="left", padx=5)
    ttk.Button(buttons, text="Return Book", style="Green.TButton",
               command=lambda: change_status("Available")).pack(side="left", padx=5)
 
    # ---------- Sidebar navigation ----------
    home_btn = ttk.Button(sidebar, text="⌂   Home", style="Nav.TButton",
                          command=lambda: show_page(home_frame))
    home_btn.pack(fill="x", padx=10, pady=4)
 
    books_btn = ttk.Button(sidebar, text="▤   View Books", style="Nav.TButton",
                           command=lambda: show_page(books_frame))
    books_btn.pack(fill="x", padx=10, pady=4)
 
    def show_page(frame):
        home_frame.pack_forget()
        books_frame.pack_forget()
        frame.pack(fill="both", expand=True, padx=30, pady=25)
 
        # Highlight the sidebar button of the page that is showing
        home_btn.config(style="NavActive.TButton" if frame is home_frame else "Nav.TButton")
        books_btn.config(style="NavActive.TButton" if frame is books_frame else "Nav.TButton")
 
        refresh_table()
 
    show_page(home_frame)
    root.mainloop()

if __name__ == "__main__":
    main()
    