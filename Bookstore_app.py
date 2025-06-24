#Bookstore_app.py

'''
Specification:
For this project, you are required to create a program for a bookstore. The program
should allow the clerk to enter data about new books into the database, update
book information, delete books from the database, and search to find the
availability of books in the database.
'''

import sqlite3

# ---------- SETUP ----------

# Connect to the database (it creates it if it doesn't exist)
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the book table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INTEGER NOT NULL
    )
''')

# Populate with initial data if not already populated
initial_books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

# Check if data already exists before inserting
cursor.execute("SELECT COUNT(*) FROM book")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO book VALUES (?, ?, ?, ?)", initial_books)
    conn.commit()

# ---------- FUNCTIONS ----------

def enter_book():
    try:
        id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter author: ")
        qty = int(input("Enter quantity: "))
        cursor.execute("INSERT INTO book VALUES (?, ?, ?, ?)", (id, title, author, qty))
        conn.commit()
        print("Book added successfully.")
    except sqlite3.IntegrityError:
        print("Book ID already exists. Please try with a different ID.")
    except ValueError:
        print("Invalid input. Please enter numeric values for ID and quantity.")

def update_book():
    try:
        id = int(input("Enter the ID of the book to update: "))
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        book = cursor.fetchone()
        if book:
            print("Book found:", book)
            title = input("Enter new title (press enter to keep current): ") or book[1]
            author = input("Enter new author (press enter to keep current): ") or book[2]
            qty = input("Enter new quantity (press enter to keep current): ")
            qty = int(qty) if qty else book[3]
            cursor.execute("UPDATE book SET title=?, author=?, qty=? WHERE id=?", (title, author, qty, id))
            conn.commit()
            print("Book updated successfully.")
        else:
            print("Book not found.")
    except ValueError:
        print("Invalid input.")

def delete_book():
    try:
        id = int(input("Enter the ID of the book to delete: "))
        cursor.execute("DELETE FROM book WHERE id=?", (id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Book deleted successfully.")
        else:
            print("Book not found.")
    except ValueError:
        print("Invalid input.")

def search_books():
    term = input("Enter book ID, title, or author to search: ").strip()
    try:
        id = int(term)
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
    except ValueError:
        cursor.execute("SELECT * FROM book WHERE title LIKE ? OR author LIKE ?", (f'%{term}%', f'%{term}%'))

    results = cursor.fetchall()
    if results:
        print("Books found:")
        for book in results:
            print(book)
    else:
        print("No books found.")

# ---------- MENU ----------

def menu():
    while True:
        print("\n===== Bookstore Menu =====")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '0':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# ---------- MAIN ----------

if __name__ == "__main__":
    menu()
    conn.close()
