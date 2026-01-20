
from typing import Dict
from search_algo.algorithms import searchTextAlgo
from service_enums.category import EntityNameType
from enum import Enum

class IndexManager():
    _attr_index = None

    def __init__(self, attr_index_map: Dict[Enum, searchTextAlgo] = None):
        self._attr_index = {}
        for attr, cls in attr_index_map.items():
            self._attr_index[attr] = cls()
        # print(self._attr_index)

    def update_index(self, attr: Enum, obj: EntityNameType):
        if attr not in self._attr_index:
            raise ValueError("Index on this attribute doesn't exist.")
        attr_value = getattr(obj, attr.value)
        self._attr_index[attr].add(attr_value, (obj.entity_name, obj))

    def search_by_attr(self, attr: Enum, value: str, limit=0):
        # print(attr)
        if attr not in self._attr_index:
            return []
        return [ book for _, book in self._attr_index[attr].search_index(value, limit)]