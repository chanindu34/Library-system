import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

class BookStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    LOST = "Lost"

class Book:
    def __init__(self,title: str,author: str, isbn: str):
        self.id: str = str(uuid.uuid4())[:8]
        self.title: str  = title
        self.author: str = author
        self.isbn : str  = isbn
        self._status: BookStatus =BookStatus.AVAILABLE
        self.history: List[str] = []

    def __repr__(self):
        return f"<Book: {self.title} | ID: {self.id} | Status: {self._status.value}>"
    
    @property
    def is_available(self) -> bool:
        return self._status == BookStatus.AVAILABLE
    
    def mark_borrowed(self):
        if not self.is_available:
            raise ValueError(f"Error: Book '{self.title}' is currently {self._status.value}")

        self._status = BookStatus.BORROWED

        self.history.append(f"Borrowed on {datetime.now().strftime('%y-%m-%d %H:%M:%S')}")
        print(f"Success: '{self.title}' has been borrowed.")

    def mark_returned(self):
        self._status = BookStatus.AVAILABLE

        self.history.append(f"Returned on {datetime.now().strftime('%y-%m-%d %H:%M:%S')}")    
        print(f"Success. '{self.title}' has been returned.")

class Member:
    def __init__(self, name: str):
        self.member_id: str = str(uuid.uuid4())[:8]
        self.name: str = name
        self._borrowed_books: List[Book] = []  
        self.max_limit: int = 3  

    def __repr__(self):
        return f"<Member: {self.name} | ID: {self.member_id} | Books: {len(self._borrowed_books)}/{self.max_limit}>"

  
    
    def borrow_book(self, book: Book):
        if len(self._borrowed_books) >= self.max_limit:
            raise ValueError(f"Error: Member {self.name} has reached the limit of {self.max_limit} books.")
    
        self._borrowed_books.append(book)
        print(f"Success: {self.name} has taken '{book.title}'")

    def return_book(self, book: Book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            print(f"Success: {self.name} returned '{book.title}'")
        else:
            print(f"Error: {self.name} does not have '{book.title}'")

    def list_books(self):
        if not self._borrowed_books:
            print(f"{self.name} has no books.")
        else:
            print(f"--- {self.name}'s Books ---")
            for book in self._borrowed_books:
                print(book)

class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}

    def add_book(self, book: Book):
        self.books[book.id] = book
        print(f"System: Added '{book.title}' to library.")

    def register_member(self, member: Member):
        self.members[member.member_id] = member
        print(f"System: Registered member '{member.name}'.")

    
    def issue_book(self, member_id: str, book_id: str):
        
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            print("Error: Member or Book not found.")
            return

        if not book.is_available:
            print(f"Error: Book '{book.title}' is already borrowed.")
            return
        
        try:
            book.mark_borrowed()       
            member.borrow_book(book)  
            print(f"Transaction Complete: '{book.title}' issued to {member.name}.")
        except ValueError as e:
            print(e) 

    def return_book(self, member_id: str, book_id: str):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if member and book:
            member.return_book(book)
            book.mark_returned()
            print(f"Transaction Complete: '{book.title}' returned.")




if __name__ == "__main__":

    uoc_library = Library()
    
    b1 = Book("Clean Code", "Robert Martin", "978-01")
    b2 = Book("The Pragmatic Programmer", "Andy Hunt", "978-02")
    b3 = Book("Introduction to Algorithms", "Cormen", "978-03")
    
    m1 = Member("Dahanayake")
    m2 = Member("Perera")

    print("--- 1. SYSTEM SETUP ---")
    uoc_library.add_book(b1)
    uoc_library.add_book(b2)
    uoc_library.add_book(b3)
    uoc_library.register_member(m1)
    uoc_library.register_member(m2)

    
    print("\n--- 2. ISSUING BOOKS ---")
    
    uoc_library.issue_book(m1.member_id, b1.id)
      
    uoc_library.issue_book(m2.member_id, b1.id)

    uoc_library.issue_book(m1.member_id, b2.id)

    
    print("\n--- 3. VERIFICATION ---")
    print(f"Book 1 Status: {b1._status.value}") 
    m1.list_books() 

    
    print("\n--- 4. RETURNING BOOKS ---")
    uoc_library.return_book(m1.member_id, b1.id)
    
    print(f"Book 1 Status After Return: {b1._status.value}") 