from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Tuple
from utils import compute_all_prefixes
from service_enums.category import EntityNameType

class searchTextAlgo(ABC):
    @abstractmethod
    def add(self, value: str, obj: Tuple[str, EntityNameType]):
        NotImplementedError()

    @abstractmethod
    def search_index(self, prefix: str, limit: Optional[int]=0):
        NotImplementedError()
        
class FullTextSearchIndex(searchTextAlgo):
    def __init__(self):
        self.__index = defaultdict(set)
    
    def add(self, value: str, obj: Tuple[str, EntityNameType]):
        value = value.lower()
        # print('FTS, rece', value, obj)
        prefixes = compute_all_prefixes(value)
        for each_prefix in prefixes:
            self.__index[each_prefix].add(obj)
        # print(value, self.__index)
    
    def search_index(self, prefix: str, limit: Optional[int]=0):
        # print(self.__index.get(prefix.lower()))
        possible_values = list(reversed(sorted(self.__index.get(prefix.lower(), set()))))
        limit = limit or len(possible_values)
        return possible_values[:limit]

class TrieNode:
    def __init__(self):
        self.children = {}
        self.words = set()

class TrieSearchIndex(searchTextAlgo):
    def __init__(self):
        self.root = TrieNode()

    def add(self, word: str, obj: Tuple[str, EntityNameType]):
        node = self.root
        # print(word, type(word))
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.words.add(obj)

    def search_index(self, prefix: str, limit=0):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return list(node.words)[:limit or len(node.words)]