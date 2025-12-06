GitHub Repository
The source code for this project is available on GitHub: [BURAYA GITHUB LINKINI YAPIŞTIR]

Identification
Name: [ADIN SOYADIN]

P-number: [ÖĞRENCİ NUMARAN]

Course code: [DERS KODU]

Declaration of Own Work
I confirm that this assignment is my own work. Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

Introduction
This code represents a comprehensive implementation of a Library Management System using the Tkinter library for the Graphical User Interface (GUI) and Matplotlib for data visualization.

The application is designed to help users manage their personal book collection. It allows users to add books with ratings, delete entries, and organize the list. Additionally, it features advanced data analysis tools, such as dynamic bar charts and pie charts, to visualize reading habits.

Installation
To run the application, ensure you have Python 3.x installed. The project requires the matplotlib library for data visualization.

You can install the required dependencies using the following command in your terminal:

Bash

pip install matplotlib
Note: Tkinter is usually included with standard Python installations.

How to Use
The application provides a user-friendly menu with the following options:

Add New Book: Enter the book title and a rating (1-10). The system includes error handling to prevent negative numbers or empty inputs.

List & Sort Books: View your collection and sort it by Rating (High/Low) or Title (A-Z).

Search Book: Use the Linear Search algorithm to quickly find if a specific book exists in your library.

Delete Book: Remove a book from the list permanently.

Visualizations: Click the buttons to generate a Bar Chart (with dynamic coloring) or a Pie Chart.

Running the Application
To start the program, navigate to the project folder in your terminal and run:


Key Features
Graphical User Interface (GUI): A clean and responsive interface built with Tkinter.

Data Persistence: All data is saved automatically to my_books.txt, so records are not lost when the app closes.

Advanced Visualization:

Bar Chart: Shows book ratings with dynamic colors (Green for high, Red for low) and an average line.

Pie Chart: Displays the distribution of books across rating categories.

Algorithms: Implements Linear Search for finding items and efficient sorting methods for organization.

Robust Error Handling: Prevents crashes by handling invalid inputs (e.g., non-numeric ratings).

Libraries Used
The following libraries are used in this project:

Tkinter: For creating the main window and UI elements.

Matplotlib: For plotting statistical graphs (Bar and Pie charts).

OS: For file existence checks and path management.

Project Structure
library_app_gui.py: The main source code containing the GUI, logic, and algorithms.

my_books.txt: The text file used as a database to store book titles and ratings.

README.md: Documentation of the project.