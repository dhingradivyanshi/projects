from enum import Enum
from abc import ABC, abstractproperty

class BookCategory(Enum):
    technical = "Technical"
    fictional = "Fictional"
    non_fictional = "Non-Fictional"

class BookAttributes(Enum):
    category = "category"
    author_name = "author"
    book_name = "name"

class EntityNameType(ABC):

    @abstractproperty
    def entity_name():
        NotImplementedError()