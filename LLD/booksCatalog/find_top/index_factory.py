from typing import Self, Dict
from enum import Enum
from search_algo import algorithms as search_algo
from service_enums.category import BookAttributes

class Indexfactory():
    
    def __init__(self):
        self._registry = {}

    def create(self, field: Enum, cls: search_algo.searchTextAlgo) -> Self:
        self._registry[field] = cls
        return self

    def get_index(self, field: Enum) -> search_algo.searchTextAlgo:
        cls = self._registry.get(field)
        if not cls:
            raise ValueError("No Index registered for this field")
        return cls
    def get_all(self) -> Dict[Enum, search_algo.searchTextAlgo]:
        return self._registry


BookFactory = Indexfactory(
                ).create(
                    BookAttributes.author_name, search_algo.FullTextSearchIndex
                ).create(
                    BookAttributes.book_name, search_algo.TrieSearchIndex
                )