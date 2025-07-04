# Bookstore_app.py

"""
Bookstore Inventory Management Application with Classes

This program provides a command-line interface for managing a bookstore's inventory
using a local SQLite database. It allows the clerk to:
- Add new books
- Update existing book information
- Delete books
- Search for books by ID, title, or author

Features Added:
- View all books
- Check stock below quantity

Database:
- SQLite3 database file: ebookstore.db
- Table: book(id INTEGER PRIMARY KEY, title STRING, author STRING, qty INTEGER)
"""

import sqlite3

# ---------- CLASSES ----------

class DatabaseManager:
    """Handles database connection and cursor management."""

    def __init__(self, db_file='ebookstore.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title STRING NOT NULL,
                author STRING NOT NULL,
                qty INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()


class Book:
    """Represents a book entity."""

    def __init__(self, book_id, title, author, qty):
        self.id = book_id
        self.title = title
        self.author = author
        self.qty = qty

    def __str__(self):
        return f"ID: {self.id}, Title: '{self.title}', Author: {self.author}, Quantity: {self.qty}"


class Bookstore(DatabaseManager):
    """Manages bookstore operations, inherits DB connection from DatabaseManager."""

    def __init__(self, db_file='ebookstore.db'):
        super().__init__(db_file)
        self._populate_initial_data()

    def _populate_initial_data(self):
        initial_books = [
            (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
        ]
        self.cursor.execute("SELECT COUNT(*) FROM book")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany("INSERT INTO book VALUES (?, ?, ?, ?)", initial_books)
            self.conn.commit()

    def enter_book(self):
        """Insert a new book into the database."""
        try:
            book_id = int(input("Enter book ID: "))
            title = input("Enter book title: ")
            author = input("Enter author: ")
            qty = int(input("Enter quantity: "))
            self.cursor.execute(
                "INSERT INTO book VALUES (?, ?, ?, ?)",
                (book_id, title, author, qty)
            )
            self.conn.commit()
            print("Book added successfully.")
        except sqlite3.IntegrityError:
            print("Book ID already exists. Please try with a different ID.")
        except ValueError:
            print("Invalid input. Please enter numeric values for ID and quantity.")

    def update_book(self):
        """Update an existing book's information in the database."""
        try:
            book_id = int(input("Enter the ID of the book to update: "))
            self.cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
            book = self.cursor.fetchone()

            if book:
                print(f"\nCurrent details:")
                print(f"ID: {book[0]}, Title: '{book[1]}', Author: {book[2]}, Quantity: {book[3]}")

                title = input("Enter new title (press Enter to keep current): ") or book[1]
                author = input("Enter new author (press Enter to keep current): ") or book[2]
                qty_input = input("Enter new quantity (press Enter to keep current): ")
                qty = int(qty_input) if qty_input else book[3]

                self.cursor.execute(
                    "UPDATE book SET title=?, author=?, qty=? WHERE id=?",
                    (title, author, qty, book_id)
                )
                self.conn.commit()

                self.cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
                updated_book = self.cursor.fetchone()

                print("\nBook updated successfully.")
                print("Updated details:")
                print(
                    f"ID: {updated_book[0]}, Title: '{updated_book[1]}', "
                    f"Author: {updated_book[2]}, Quantity: {updated_book[3]}"
                )
            else:
                print("Book not found.")
        except ValueError:
            print("Invalid input. Please enter valid numeric ID.")

    def delete_book(self):
        """Delete a book from the database based on ID and display its details."""
        try:
            book_id = int(input("Enter the ID of the book to delete: "))
            self.cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
            book = self.cursor.fetchone()

            if book:
                confirm = input(
                    f"Are you sure you want to delete '{book[1]}' by {book[2]}? (y/n): "
                ).lower()
                if confirm == 'y':
                    self.cursor.execute("DELETE FROM book WHERE id=?", (book_id,))
                    self.conn.commit()
                    print(
                        f"Deleted: ID {book[0]}, Title: '{book[1]}', "
                        f"Author: {book[2]}, Quantity: {book[3]}"
                    )
                else:
                    print("Deletion cancelled.")
            else:
                print("Book not found.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric ID.")

    def search_books(self):
        """Search for books by ID, title, or author."""
        print("\nSearch by:")
        print("1. Book ID")
        print("2. Title")
        print("3. Author")
        choice = input("Choose search type (1/2/3): ").strip()

        if choice == '1':
            try:
                book_id = int(input("Enter book ID: ").strip())
                self.cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                return

        elif choice == '2':
            title = input("Enter book title (or part of it): ").strip().lower()
            self.cursor.execute("SELECT * FROM book WHERE LOWER(title) LIKE ?", (f"%{title}%",))

        elif choice == '3':
            author = input("Enter author name (or part of it): ").strip().lower()
            self.cursor.execute("SELECT * FROM book WHERE LOWER(author) LIKE ?", (f"%{author}%",))

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            return

        results = self.cursor.fetchall()
        if results:
            print("\nBooks found:")
            for book in results:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
        else:
            print("No books found.")

    def view_all_books(self):
        """View all books in database."""
        self.cursor.execute("SELECT * FROM book")
        books = self.cursor.fetchall()
        if books:
            print("\nAll books in Inventory:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
        else:
            print("No books in inventory.")

    def check_stock_below_quantity(self):
        """Display books with quantity below a user-specified threshold."""
        try:
            threshold = int(input("Enter quantity threshold: "))
            self.cursor.execute("SELECT * FROM book WHERE qty < ?", (threshold,))
            results = self.cursor.fetchall()
            if results:
                print(f"\nBooks with stock below {threshold}:")
                for book in results:
                    print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
            else:
                print(f"No books found with stock below {threshold}.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for quantity.")


# ---------- MENU ----------

def menu(bookstore):
    """Main menu loop for user interaction."""
    while True:
        print("\n===== Bookstore Menu =====")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View all books")
        print("6. Check stock below quantity")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            bookstore.enter_book()
        elif choice == '2':
            bookstore.update_book()
        elif choice == '3':
            bookstore.delete_book()
        elif choice == '4':
            bookstore.search_books()
        elif choice == '5':
            bookstore.view_all_books()
        elif choice == '6':
            bookstore.check_stock_below_quantity()
        elif choice == '0':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please select a valid option.")


# ---------- MAIN ----------

if __name__ == "__main__":
    bookstore = Bookstore()
    try:
        menu(bookstore)
    finally:
        bookstore.close()
