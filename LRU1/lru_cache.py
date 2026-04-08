"""LRU Cache implementation using a hash map and doubly linked list."""

from typing import Hashable, Optional, TypeVar

from cache_interface import Cache
from exceptions import CacheKeyError
from linked_list import _DoublyLinkedList, _Node

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

DEFAULT_CAPACITY: int = 128


class LRUCache(Cache[K, V]):
    """
    Least Recently Used cache with O(1) get and put operations.

    Uses a hash map (dict) for O(1) key lookup and a doubly linked list
    for O(1) access-order tracking. When capacity is exceeded, the least
    recently used item is automatically evicted.
    """

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        super().__init__(capacity)
        self._map: dict[K, _Node[K, V]] = {}
        self._list: _DoublyLinkedList[K, V] = _DoublyLinkedList()

    # --- Public API ---

    def get(self, key: K) -> Optional[V]:
        """Retrieve value by key. Moves key to most-recently-used position."""
        if key not in self._map:
            return None
        node = self._map[key]
        self._list.move_to_front(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair. Evicts LRU item if at capacity."""
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._list.move_to_front(node)
            return
        if self.size >= self._capacity:
            self._evict()
        new_node = _Node(key, value)
        self._list.add_to_front(new_node)
        self._map[key] = new_node

    def delete(self, key: K) -> None:
        """Remove a key from the cache. Raises CacheKeyError if not found."""
        if key not in self._map:
            raise CacheKeyError(f"Key '{key}' not found.")
        node = self._map.pop(key)
        self._list.remove(node)

    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._map.clear()
        self._list.clear()

    @property
    def size(self) -> int:
        """Return current number of cached items."""
        return len(self._map)

    # --- Private Helpers ---

    def _evict(self) -> None:
        """Remove the least recently used item (tail of list)."""
        node = self._list.remove_last()
        del self._map[node.key]
