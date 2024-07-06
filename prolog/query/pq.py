from collections import deque 
from bisect import insort

class SearchQueue():
    def __init__(self):
        self._container = deque()  ## deque() not list [] 
                                   ## the idea is to pop from the left side
    @property
    def empty(self):
        return not self._container
    def push(self, expr):
        self._container.append(expr)
    def pop(self):
        return self._container.popleft() # FIFO popping from the left is O(1) in deque() unlike in list
    def __repr__(self):
        return repr(self._container)
        
class FactHeap():
    def __init__(self):
        self._container = []

    def push(self, item):
        insort(self._container, item) # in by sort
        
    def __getitem__(self, item):
         return self._container[item]
    
    def __len__(self):
         return len(self._container)
    
    def __repr__(self):
        return repr(self._container)