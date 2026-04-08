"""Internal doubly linked list data structures for cache implementations."""

from typing import Generic, Hashable, Optional, TypeVar

from exceptions import CacheError

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node(Generic[K, V]):
    """A single node in a doubly linked list, storing a cache key-value pair."""

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node[K, V]] = None
        self.next: Optional[_Node[K, V]] = None

    def __repr__(self) -> str:
        return f"_Node(key={self.key!r}, value={self.value!r})"


class _DoublyLinkedList(Generic[K, V]):
    """
    Doubly linked list with sentinel head/tail nodes.

    Supports O(1) insertion at front, removal from any position,
    and moving an existing node to front. Used internally by LRUCache.
    """

    def __init__(self) -> None:
        # Sentinel nodes simplify boundary conditions
        self._head: _Node[K, V] = _Node(None, None)  # type: ignore[arg-type]
        self._tail: _Node[K, V] = _Node(None, None)  # type: ignore[arg-type]
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    # --- Public API ---

    def add_to_front(self, node: _Node[K, V]) -> None:
        """Insert node right after the head sentinel. O(1)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node  # type: ignore[union-attr]
        self._head.next = node
        self._size += 1

    def remove(self, node: _Node[K, V]) -> None:
        """Unlink node from its current position. O(1)."""
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]
        node.prev = None
        node.next = None
        self._size -= 1

    def move_to_front(self, node: _Node[K, V]) -> None:
        """Move an existing node to the front (most recently used). O(1)."""
        self.remove(node)
        self.add_to_front(node)

    def remove_last(self) -> _Node[K, V]:
        """Remove and return the node just before the tail sentinel (LRU item). O(1)."""
        if self._size == 0:
            raise CacheError("Cannot remove from an empty list.")
        last = self._tail.prev  # type: ignore[union-attr]
        self.remove(last)  # type: ignore[arg-type]
        return last  # type: ignore[return-value]

    def clear(self) -> None:
        """Remove all nodes, reset to empty state."""
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    @property
    def size(self) -> int:
        """Return number of real nodes (excluding sentinels)."""
        return self._size

    def __repr__(self) -> str:
        """Show the list contents from front to back for debugging."""
        nodes = []
        current = self._head.next
        while current is not self._tail:
            nodes.append(repr(current))
            current = current.next  # type: ignore[union-attr]
        return f"_DoublyLinkedList([{', '.join(nodes)}])"
