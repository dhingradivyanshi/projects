from typing import List, SupportsInt, LiteralString, SupportsFloat
from abc import ABC, abstractmethod
from enum import Enum
import heapq
from collections import defaultdict
from service_enums.category import BookCategory, BookAttributes, EntityNameType
from search_algo.search_index_manager import IndexManager
from find_top.index_factory import BookFactory



class BookBuilder():
    def __init__(self):
        self._name = None
        self._author = None
        self._publisher = None
        self._publish_year = None
        self._category = None
        self._price = 0.0
        self._sold_count = 0

    def add_name(self, book_name: LiteralString):
        self._name = book_name
        return self
    
    def add_author(self, author_name: LiteralString):
        self._author = author_name
        return self
    
    def add_publisher(self, publisher_name: LiteralString):
        self._publisher = publisher_name
        return self
    
    def add_publish_year(self, publisher_year: SupportsInt):
        self._publish_year = publisher_year
        return self
    
    def add_category(self, book_category: BookCategory):
        self._category = book_category
        return self
    
    def add_price(self, book_price: SupportsFloat):
        self._price = book_price
        return self

    def add_count(self, sold_count: SupportsInt):
        self._sold_count = sold_count
        return self

    def build(self):
        if not self._name or not self._author:
            raise ValueError("Name and Author of book are mandate.") 
        return Book._create(
            self._name,
            self._author,
            self._publisher,
            self._publish_year,
            self._category,
            self._price,
            self._sold_count
        )

class Book(EntityNameType):
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Book should be created with BookBuilder only.")

    @property
    def entity_name(self):
        return self.name
    
    @classmethod
    def _create(cls, name, author, publisher, publish_year, category, price, count_sold):
        self = object.__new__(cls)
        self.name = name
        self.author = author
        self.publisher = publisher
        self.publish_year = publish_year
        self.category = category
        self.price = price
        self.count_sold = count_sold
        return self

    def __repr__(self):
        return f"<Book {self.name} by {self.author} - Sold: {self.count_sold}>"
        

class Catalog(ABC):
    @abstractmethod
    def add(self, data): 
        NotImplementedError() 
    
    @abstractmethod
    def getAll(self): 
        NotImplementedError() 

class BookCatalog(Catalog):
    __books = None
    def __init__(self):
        self.__books = []

    def add(self, book: Book):
        self.__books.append(book)
    
    def getAll(self):
        return self.__books[:]



class BookCatalogManager():
    _catalog_manager = None

    def __init__(self):
        self._catalog_manager = BookCatalog()
        self._index_manager = IndexManager(BookFactory.get_all())
        self._author_top_sold_heap = defaultdict(list)
        self._category_top_sold_heap = defaultdict(list)

    def add_books(self, books: List[Book]) -> None:
        if len(books) == 0:
            raise ValueError("No Books Shared")

        for book in books:
            self._catalog_manager.add(book)
            self._index_manager.update_index(BookAttributes.author_name, book)
            self._index_manager.update_index(BookAttributes.book_name, book)
            heapq.heappush(self._author_top_sold_heap[book.author], (book.count_sold, book.entity_name, book))
            heapq.heappush(self._category_top_sold_heap[book.category], (book.count_sold, book.entity_name, book))

    def search_by_author(self, author_name) -> List[Book]:
        return self._index_manager.search_by_attr(BookAttributes.author_name, author_name)
    
    def search_by_name(self, book_name) -> List[Book]:
        return self._index_manager.search_by_attr(BookAttributes.book_name, book_name)
    
    def get_top_sold_by_author(self, author_name, limit=1) -> List[Book]:
        if limit < 1:
            raise ValueError("Limit should be >= 1")
        
        author_max_heap = self._author_top_sold_heap.get(author_name)
        return [book for _, _, book in heapq.nlargest(limit, author_max_heap)] if author_max_heap else []

    def get_top_sold_by_category(self, category, limit=1) -> List[Book]:
        if limit < 1:
            raise ValueError("Limit should be >= 1")
        
        category_max_heap = self._category_top_sold_heap.get(category)
        return [book for _, _, book in heapq.nlargest(limit, category_max_heap)] if category_max_heap else []


if __name__ == "__main__":
    catalog = BookCatalogManager()
    b1 = (
        BookBuilder()
        .add_name("ABCD")
        .add_author("B")
        .build()
    )
    b2 = BookBuilder().add_name("AB").add_author("B").add_count(5).build()
    b3 = BookBuilder().add_name("Bcd").add_author("B").build()

    catalog.add_books([b1, b2, b3])
    print(catalog.get_top_sold_by_author("B"))
    print(catalog.get_top_sold_by_author("B", 2))
    print(catalog.get_top_sold_by_author("B", 3))

    print(catalog.search_by_author("B"))
    print(catalog.search_by_name("AB"))
    # print(catalog, b1)
