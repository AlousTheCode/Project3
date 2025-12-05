# library_app_gui.py

import os
import matplotlib.pyplot as plt
# Module needed to embed Matplotlib plots into a Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial

# --- LIBRARY AND FILE SETTINGS ---
# Filename constant for storing book data
filename = "my_books.txt"

# ---------------------------------------------------------------------------------------
# --- 1. FILE HANDLING (Cited) ---
# Reference: Python File Handling Documentation, utilizing  for safe operation.
# ---------------------------------------------------------------------------------------

def check_if_file_exists():
    """Checks the existence of the data file."""
    return os.path.exists(filename)

def get_all_books():
    """Reads all books from the file and returns them as a list of dictionaries."""
    book_list = []
    
    if check_if_file_exists():
        try:
            # Use 'with open' for guaranteed file closure.
            with open(filename, "r") as f:
                all_lines = f.readlines()
        except IOError:
            # Error Handling: Catches file reading errors.
            messagebox.showerror("File Error", "The book data file could not be read.")
            return book_list

        for line in all_lines:
            clean_line = line.strip()
            # Split the line into title and rating, handling commas in titles.
            parts = clean_line.split(",", 1)
            
            if len(parts) == 2:
                book_name = parts[0].strip()
                rating_str = parts[1].strip()
                
                # Error Handling: Ensures rating is a digit before conversion.
                if rating_str.isdigit():
                    book = {"title": book_name, "rating": int(rating_str)}
                    book_list.append(book)
                # Lines with non-digit ratings are silently skipped.
    return book_list

def rewrite_all_books(books):
    """Rewrites the entire book list back to the file (used after deletion/update)."""
    try:
        # 'w' mode (write) overwrites the entire file content.
        with open(filename, "w") as f:
            for book in books:
                line = book["title"] + "," + str(book["rating"]) + "\n"
                f.write(line)
    except IOError:
        # Error Handling: Catches file writing errors.
        messagebox.showerror("File Error", "Failed to write data to the file.")


def save_book_to_file(name, rating):
    """Appends a new book entry to the file."""
    line = name + "," + str(rating) + "\n"
    try:
        # 'a' mode (append) adds the data to the end of the file.
        with open(filename, "a") as f:
            f.write(line)
        return True
    except IOError:
        # Error Handling: Catches file writing errors.
        messagebox.showerror("File Error", "Failed to save the book to the file.")
        return False

# ---------------------------------------------------------------------------------------
# --- 2. CORE LOGIC (Search and Sort Algorithms) ---
# Reference: Linear Search implementation pattern.
# Reference: Python's built-in sorted() function for efficient sorting.
# ---------------------------------------------------------------------------------------

def linear_search_book(title_to_find, books):
    """
    Linear Search: Searches for the specified title in the book list (case-insensitive).
    """
    for book in books:
        if book['title'].lower() == title_to_find.lower(): # lower() method for case-insensitive search
            return book
    return None # Returns None if the book is not found

def check_duplicate_book(new_name):
    """Checks if a book already exists using the linear search algorithm."""
    current_books = get_all_books()
    return linear_search_book(new_name, current_books) is not None

def sort_books(books, sort_by='rating', ascending=False):
    """
    Sorts the books based on a specified criterion ('rating' or 'title').
    """
    if sort_by == 'title':
        # Sort by title, converting to lowercase for accurate alphabetical order.
        return sorted(books, key=lambda book: book['title'].lower(), reverse=not ascending)
    else:
        # Sort by rating.
        return sorted(books, key=lambda book: book['rating'], reverse=not ascending)

# ---------------------------------------------------------------------------------------
# --- 3. TKINTER GUI (User Interface) ---
# Reference: Tkinter and Matplotlib Integration (FigureCanvasTkAgg)
# ---------------------------------------------------------------------------------------

class LibraryApp:
    """Main class for the Library Management System GUI application."""
    def __init__(self, master):
        self.master = master
        master.title("Advanced Library Management System")
        master.geometry("1000x700")

        # Main container frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        """Initializes and arranges all main UI components."""
        # Left Menu Bar (Buttons)
        menu_frame = tk.Frame(self.main_frame, width=220, relief=tk.RAISED, borderwidth=2)
        menu_frame.pack(side="left", fill="y", padx=5)

        tk.Label(menu_frame, text="📖 MENU", font=('Arial', 16, 'bold')).pack(pady=15)
        
        # Main CRUD buttons
        ttk.Button(menu_frame, text="1. Add New Book", command=self.show_add_book_view).pack(fill='x', pady=5, padx=10)
        ttk.Button(menu_frame, text="2. List & Sort Books", command=self.show_list_books_view).pack(fill='x', pady=5, padx=10)
        ttk.Button(menu_frame, text="3. Search Book", command=self.show_search_view).pack(fill='x', pady=5, padx=10)
        ttk.Button(menu_frame, text="4. Delete Book", command=self.show_delete_view).pack(fill='x', pady=5, padx=10)
        
        tk.Label(menu_frame, text="📊 VISUALIZATIONS", font=('Arial', 12, 'bold')).pack(pady=15)
        # Data Visualization buttons
        ttk.Button(menu_frame, text="5. Rating Distribution (Bar Chart)", command=self.show_bar_chart).pack(fill='x', pady=5, padx=10)
        ttk.Button(menu_frame, text="6. Category Distribution (Pie Chart)", command=self.show_pie_chart).pack(fill='x', pady=5, padx=10)
        
        ttk.Button(menu_frame, text="EXIT", command=self.master.quit).pack(fill='x', pady=30, padx=10)

        # Right Content Area (where views are displayed)
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        self.show_welcome_view()

    def clear_content_frame(self):
        """Destroys all widgets in the content frame to switch views."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- VIEWS (Screen definitions) ---

    def show_welcome_view(self):
        """Displays the initial welcome message."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="📚 Welcome to the Advanced Library Application! 📊", font=('Arial', 18)).pack(pady=50)
        tk.Label(self.content_frame, text="Please select an operation from the menu on the left.", font=('Arial', 12)).pack(pady=10)

    def show_add_book_view(self):
        """Displays the form to add a new book."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="--- Add New Book ---", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Input fields
        tk.Label(self.content_frame, text="Book Title:").pack(pady=5)
        self.book_title_entry = tk.Entry(self.content_frame, width=50)
        self.book_title_entry.pack(pady=5)
        
        tk.Label(self.content_frame, text="Rating (1-10):").pack(pady=5)
        self.book_rating_entry = tk.Entry(self.content_frame, width=10)
        self.book_rating_entry.pack(pady=5)
        
        ttk.Button(self.content_frame, text="Save Book", command=self.handle_add_book).pack(pady=20)

    def handle_add_book(self):
        """Handles the book addition process with comprehensive error checking."""
        name = self.book_title_entry.get().strip()
        rating_input = self.book_rating_entry.get().strip()

        if len(name) == 0:
            messagebox.showerror("Error", "Book title cannot be empty.")
            return

        if check_duplicate_book(name):
            messagebox.showerror("Error", f"'{name}' already exists in the library.")
            return

        try:
            # Error Handling: Check if the rating is a valid integer.
            rating = int(rating_input)
            if 1 <= rating <= 10:
                if save_book_to_file(name, rating):
                    self.book_title_entry.delete(0, tk.END)
                    self.book_rating_entry.delete(0, tk.END)
                    messagebox.showinfo("Success", f"'{name}' successfully saved.")
            else:
                messagebox.showerror("Error", "Rating must be between 1 and 10.")
        except ValueError:
            # bi tek burda sıkıntı olariblir tekrar baks
            messagebox.showerror("Error", "Please enter a valid number for the rating.")

    def show_list_books_view(self):
        """Displays books in a sortable Treeview widget."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="--- List & Sort Books ---", font=('Arial', 14, 'bold')).pack(pady=10)
        
        books = get_all_books()
        if not books:
            tk.Label(self.content_frame, text="Library is empty.").pack(pady=20)
            return

        # Sorting Options Frame
        sort_frame = tk.Frame(self.content_frame)
        sort_frame.pack(pady=10)
        
        tk.Label(sort_frame, text="Sort By:").pack(side='left', padx=5)
        
        sort_variable = tk.StringVar(self.content_frame, "1") # Default: Rating Descending
        
        def update_list(val):
            """Updates the Treeview content based on the selected sorting method."""
            choice = sort_variable.get()
            if choice == "1":
                sorted_books = sort_books(books, 'rating', ascending=False)
            elif choice == "2":
                sorted_books = sort_books(books, 'rating', ascending=True)
            elif choice == "3":
                sorted_books = sort_books(books, 'title', ascending=True)
            
            # Clear and repopulate the Treeview
            self.book_tree.delete(*self.book_tree.get_children())
            for i, book in enumerate(sorted_books):
                self.book_tree.insert("", tk.END, values=(i + 1, book['title'], book['rating']))

        
        # Radio Buttons for Sorting Criteria
        tk.Radiobutton(sort_frame, text="Rating Descending", variable=sort_variable, value="1", command=lambda: update_list(None)).pack(side='left')
        tk.Radiobutton(sort_frame, text="Rating Ascending", variable=sort_variable, value="2", command=lambda: update_list(None)).pack(side='left')
        tk.Radiobutton(sort_frame, text="Title (A-Z)", variable=sort_variable, value="3", command=lambda: update_list(None)).pack(side='left')

        # Treeview (Table) setup
        self.book_tree = ttk.Treeview(self.content_frame, columns=("No", "Title", "Rating"), show='headings')
        self.book_tree.heading("No", text="No.", anchor='center')
        self.book_tree.heading("Title", text="Book Title", anchor='w')
        self.book_tree.heading("Rating", text="Rating", anchor='center')
        
        self.book_tree.column("No", width=50, anchor='center')
        self.book_tree.column("Title", width=450, anchor='w')
        self.book_tree.column("Rating", width=100, anchor='center')
        
        self.book_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial list population
        update_list(None)


    def show_search_view(self):
        """Displays the book search interface (Linear Search)."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="--- Search Book (Linear Search) ---", font=('Arial', 14, 'bold')).pack(pady=20)
        
        tk.Label(self.content_frame, text="Enter Book Title to Find:").pack(pady=5)
        self.search_entry = tk.Entry(self.content_frame, width=50)
        self.search_entry.pack(pady=5)
        
        ttk.Button(self.content_frame, text="Search", command=self.handle_search).pack(pady=10)
        
        self.search_result_label = tk.Label(self.content_frame, text="", font=('Arial', 12))
        self.search_result_label.pack(pady=20)
        
    def handle_search(self):
        """Executes the search operation."""
        title_to_find = self.search_entry.get().strip()
        books = get_all_books()
        
        if not books:
            self.search_result_label.config(text="Library is empty, cannot search.")
            return

        if len(title_to_find) == 0:
            self.search_result_label.config(text="Please enter a title.")
            return
            
        found_book = linear_search_book(title_to_find, books) # Calls the Linear Search Algorithm
        
        if found_book:
            self.search_result_label.config(text=f"✅ Success: '{found_book['title']}' found! Rating: {found_book['rating']}/10")
        else:
            self.search_result_label.config(text=f"❌ Result: '{title_to_find}' not found in the library.")


    def show_delete_view(self):
        """Displays the interface for deleting a book."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="--- Delete Book ---", font=('Arial', 14, 'bold')).pack(pady=10)
        
        books = get_all_books()
        if not books:
            tk.Label(self.content_frame, text="Library is empty, no books to delete.").pack(pady=20)
            return

        # Combobox (Dropdown) to select the book to delete
        tk.Label(self.content_frame, text="Select Book to Delete:").pack(pady=5)
        
        book_options = [f"{i+1}. {book['title']} ({book['rating']}/10)" for i, book in enumerate(books)]
        self.book_to_delete_var = tk.StringVar(self.content_frame)
        self.book_to_delete_var.set(book_options[0] if book_options else "")
        
        self.book_combobox = ttk.Combobox(self.content_frame, textvariable=self.book_to_delete_var, values=book_options, width=70)
        self.book_combobox.pack(pady=5)
        
        # Use partial to pass the current list of books to the handler function
        ttk.Button(self.content_frame, text="Delete Selected Book", 
                   command=partial(self.handle_delete_book, books)).pack(pady=20)


    def handle_delete_book(self, books):
        """Handles the deletion process and updates the file."""
        selected_option = self.book_to_delete_var.get()
        if not selected_option:
            messagebox.showerror("Error", "Please select a book to delete.")
            return

        # Extract the index from the selected string (e.g., "1. Book Title" -> index 0)
        try:
            index_to_delete = int(selected_option.split('.')[0]) - 1
        except ValueError:
            messagebox.showerror("Error", "Invalid selection format.")
            return
            
        if 0 <= index_to_delete < len(books):
            # Confirmation dialogue before deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete: {books[index_to_delete]['title']}?")
            if confirm:
                deleted_book = books.pop(index_to_delete)
                rewrite_all_books(books) # Rewrite the file with the modified list
                
                messagebox.showinfo("Success", f"'{deleted_book['title']}' successfully deleted.")
                self.show_delete_view() # Refresh the view
        else:
            messagebox.showerror("Error", "Invalid book number.")


    # --- MATPLOTLIB VISUALIZATION (Data Visualization) ---

    def plot_graph(self, plot_func):
        """
        Generic helper function to embed a Matplotlib figure into the Tkinter window.
        Reference: Matplotlib's Tkinter integration using FigureCanvasTkAgg.
        """
        self.clear_content_frame()
        
        books = get_all_books()
        if not books:
            messagebox.showinfo("Info", "Not enough data to draw a graph.")
            return

        # Create a Matplotlib figure
        fig = plt.Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Call the specific plotting function (plot_bar or plot_pie)
        plot_func(books, ax) 

        # Embed the Matplotlib figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add the Matplotlib toolbar (for zooming, panning, etc.)
        toolbar = NavigationToolbar2Tk(canvas, self.content_frame)
        toolbar.update()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.draw()


    def show_bar_chart(self):
        """Generates and displays the Bar Chart of rating distribution."""
        
        def plot_bar(books, ax):
            x_scores = list(range(1, 11))
            # Calculate book counts per score using List Comprehension
            y_counts = [sum(1 for book in books if book["rating"] == score) for score in x_scores]
            
            # Draw bars
            bars = ax.bar(x_scores, y_counts, color='#3498db', alpha=0.8)
            
            # Add value labels on top of the bars
            for bar in bars:
                yval = bar.get_height()
                if yval > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)
            
            ax.set_title('Book Rating Distribution (Bar Chart)')
            ax.set_xlabel('Rating (1-10)') # 1 den 10 a kadar gidiyor burası 9.5 olabilir 
            ax.set_ylabel('Number of Books')
            ax.set_xticks(x_scores)
            ax.grid(axis='y', linestyle='--', alpha=0.6)

        self.plot_graph(plot_bar)
        
    def show_pie_chart(self):
        """Generates and displays the Pie Chart of rating categories."""
        
        def plot_pie(books, ax):
            # Categorize the ratings
            low_rated = sum(1 for book in books if book["rating"] <= 5)
            mid_rated = sum(1 for book in books if 6 <= book["rating"] <= 8)
            high_rated = sum(1 for book in books if book["rating"] >= 9)

            sizes = [low_rated, mid_rated, high_rated]
            labels = ['Low Rated (1-5)', 'Mid Rated (6-8)', 'Highly Rated (9-10)']
            colors = ['#e74c3c', '#f39c12', '#2ecc71']
            
            # Filter out zero values (Pie charts fail or look bad with zero slices)
            filtered_data = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
            if not filtered_data:
                 ax.text(0.5, 0.5, "Insufficient data for category chart.", ha='center')
                 return

            filtered_sizes, filtered_labels, filtered_colors = zip(*filtered_data)

            # Draw the Pie chart
            ax.pie(filtered_sizes, 
                    labels=filtered_labels, 
                    colors=filtered_colors,
                    autopct='%1.1f%%',  # Show percentage
                    startangle=90,
                    wedgeprops={'edgecolor': 'black', 'linewidth': 1})
            
            ax.set_title('Distribution by Rating Category (Pie Chart)')
            ax.axis('equal') # Ensures the pie chart is circular
            
        self.plot_graph(plot_pie)


if __name__ == "__main__":
    # Initialize the main Tkinter window
    root = tk.Tk()
    
    # Initialize the Library Application
    app = LibraryApp(root)
    
    # Start the Tkinter main event loop
    root.mainloop()