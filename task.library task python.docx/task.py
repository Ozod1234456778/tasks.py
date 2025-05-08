from datetime import datetime

class Book:
    def __init__(self, title, author, year, isbn, genre):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.genre = genre
        self.is_borrowed = False
        self.borrowed_by = None
        self.borrow_date = None
        self.borrow_count = 0

    def get_summary(self):
        return f"{self.title} by {self.author} ({self.year}) - Genre: {self.genre}"

    def mark_borrowed(self, user_id):
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrowed_by = user_id
            self.borrow_date = datetime.now()
            self.borrow_count += 1
        else:
            print(" Kitob allaqachon olingan.")

    def mark_returned(self):
        self.is_borrowed = False
        self.borrowed_by = None
        self.borrow_date = None
 user.py – User sinfi

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.borrowed_books = []
        self.history = []

    def borrow_book(self, book):
        if not book.is_borrowed:
            book.mark_borrowed(self.user_id)
            self.borrowed_books.append(book)
            self.history.append((book, "Borrowed"))
        else:
            print(" Bu kitob allaqachon olingan.")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.mark_returned()
            self.borrowed_books.remove(book)
            self.history.append((book, "Returned"))
        else:
            print(" Siz bu kitobni olmagansiz.")

    def get_current_borrowed(self):
        return [book.title for book in self.borrowed_books]

    def get_history(self):
        return [(b.title, status) for b, status in self.history]
 library.py – Library sinfi

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]

    def search_books(self, keyword):
        result = []
        for book in self.books:
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword.lower() in book.genre.lower()):
                result.append(book)
        return result

    def list_available_books(self):
        return [book for book in self.books if not book.is_borrowed]

    def register_user(self, user):
        self.users.append(user)

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def borrow_book(self, user_id, isbn):
        user = self.get_user_by_id(user_id)
        book = next((b for b in self.books if b.isbn == isbn), None)
        if user and book:
            user.borrow_book(book)
        else:
            print(" Foydalanuvchi yoki kitob topilmadi.")

    def return_book(self, user_id, isbn):
        user = self.get_user_by_id(user_id)
        book = next((b for b in user.borrowed_books if b.isbn == isbn), None)
        if user and book:
            user.return_book(book)
        else:
            print(" Qaytarilayotgan kitob topilmadi.")

    def generate_statistics(self):
        total_books = len(self.books)
        total_users = len(self.users)
        borrowed_books = len([b for b in self.books if b.is_borrowed])
        print(f" Jami kitoblar: {total_books}")
        print(f" Jami foydalanuvchilar: {total_users}")
        print(f" Ijaradagi kitoblar: {borrowed_books}")
Namuna ishlatish (main.py)

from book import Book
from user import User
from library import Library

lib = Library()

# Kitoblar qo‘shamiz
book1 = Book("Ufqdagi Yulduz", "T. Malik", 1990, "111", "Drama")
book2 = Book("Python Asoslari", "Ali Qodirov", 2020, "222", "Texnologiya")
lib.add_book(book1)
lib.add_book(book2)

# Foydalanuvchi ro'yxatdan o'tadi
user1 = User(1, "Azizbek")
lib.register_user(user1)

# Kitob ijarasi
lib.borrow_book(1, "111")
lib.borrow_book(1, "222")

# Statistikani chiqarish
lib.generate_statistics()

# Qaytarish
lib.return_book(1, "111")

# Foydalanuvchi tarixini ko‘rish
print(user1.get_history())
