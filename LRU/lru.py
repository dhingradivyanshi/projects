class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
from collections import OrderedDict
x = OrderedDict
x.pop
x.popitem

class LRUCache:

    def __init__(self, cacheSize: int):
        self.capacity = cacheSize
        self.cache = {}
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.__join(self.head, self.tail)
    
    def __join(self, node1: Node, node2: Node) -> None:
        node1.next = node2
        node2.prev = node1
    
    def __str__(self):
        start = self.head.next
        values = []
        while(start!=self.tail):
            values.append(str((start.key, start.value)))
            start = start.next
        return " -> ".join(values)

    def get(self, key: int) -> int:
        existingNode = self.cache.get(key)
        if existingNode:
            self.__remove_by_node(existingNode)
            self.__insert_at_head_with_node(existingNode)
            return existingNode.value
        return -1
    
    def __insert_at_head_with_node(self, node: Node) -> None:
        self.__join(node, self.head.next)
        self.__join(self.head, node)

    
    def __remove_by_node(self, node: Node) -> Node:
        node.next.prev, node.prev.next = node.prev, node.next
        node.next = node.prev = None # Avoid dangling pointers
        return node

    def put(self, key: int, value: int) -> None:
        existingNode = self.cache.get(key)
        if existingNode is not None:
            self.__remove_by_node(existingNode)
        else:
            if len(self.cache) == self.capacity:
                last_node = self.__remove_by_node(self.tail.prev)
                del self.cache[last_node.key]
        
        newNode = Node(key, value)
        self.__insert_at_head_with_node(newNode)
        self.cache[key] = newNode
            

# if __name__ == "__path__":
    # Your LRUCache object will be instantiated and called as such:
obj = LRUCache(2)
obj.put(1,1)
print(obj)
obj.put(2,2)
print(obj)
print(obj.get(1))
obj.put(3,3)
print(obj)
print(obj.get(2))
obj.put(4,4)
print(obj)
print(obj.get(1))
print(obj.get(3))
print(obj.get(4))




    # param_1 = obj.get(key)
    # obj.put(key,value)

# class DoublyNode:
#     key = None
#     value = None
#     prevNode = None
#     nextNode = None

#     def __init__(self, search: int, assignedVal: int):
#         self.key = search
#         self.value = assignedVal
    
#     def setNext(self, node ) -> None:
#         self.nextNode = node
    
#     def setPrev(self, node) -> None:
#         self.prevNode = node
    
#     def updateValue(self, newValue) -> None:
#         self.value = newValue

# class LRUCache:
#     doublyLLHead: DoublyNode = None
#     capacity: int = None
#     tail: DoublyNode = None
#     keyMapper: dict = None
#     cacheCounter: int = None
    
#     def __init__(self, cacheSize: int):
#         self.capacity = cacheSize
#         self.keyMapper = {}
#         self.cacheCounter = 0
#         self.doublyLLHead = self.tail = DoublyNode(-1, -1)

#     def get(self, key: int) -> int:
#         existingNode = self.keyMapper.get(key)
#         if existingNode is not None:
#             self.__removeByNode(existingNode)
#             self.__insertAtHeadWithNode(existingNode)
#             return existingNode.value
#         return -1
    
#     def __insertAtHeadWithNode(self, node: DoublyNode) -> None:
#         node.setNext(self.doublyLLHead.nextNode) # Set existing top node to next Node, even if null
#         if node.nextNode:
#             node.nextNode.setPrev(node)  # update old top node's prev
#         self.doublyLLHead.setNext(node) # update Head's next
#         node.setPrev(self.doublyLLHead) # update newNode's prev
#         if self.doublyLLHead == self.tail:
#             self.tail = node
    
#     def __insertAtHead(self, key: int, value: int) -> None:
#         newNode = DoublyNode(key, value)
#         self.__insertAtHeadWithNode(newNode)
#         self.keyMapper[key] = newNode
#         self.cacheCounter += 1

#     def __removeByKey(self, key: int) -> None:
#         existingNode = self.keyMapper[key]
#         if existingNode:
#             self.__removeByNode(existingNode)
#             del self.keyMapper[key]
#             del existingNode
#             self.cacheCounter -= 1 
    
#     def __removeByNode(self, node: DoublyNode) -> None:
#         if node.nextNode:
#             node.nextNode.prevNode = node.prevNode
#         if node.prevNode:
#             node.prevNode.nextNode = node.nextNode
        
#         if self.doublyLLHead == node: # 1 Element Only or Head
#             self.doublyLLHead = node.nextNode
        
#         if self.tail == node: #LastElement
#             self.tail = node.prevNode
    
#     def __evict(self):
#         lruNode = self.tail
#         self.tail = lruNode.prevNode
#         lruNode.prevNode = None
#         self.tail.nextNode = None
#         del self.keyMapper[lruNode.key]
#         del lruNode
#         self.cacheCounter -= 1 

#     def put(self, key: int, value: int) -> None:
#         existingNode = self.keyMapper.get(key)
#         if existingNode:
#             existingNode.updateValue(value)
#             self.__removeByNode(existingNode)
#             self.__insertAtHeadWithNode(existingNode)
#         else:
#             if self.cacheCounter == self.capacity:
#                 self.__evict()
#             self.__insertAtHead(key, value)            

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)