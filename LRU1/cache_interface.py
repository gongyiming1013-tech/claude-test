"""Abstract base class defining the contract for all cache implementations."""

from abc import ABC, abstractmethod
from typing import Generic, Hashable, Optional, TypeVar

from exceptions import CacheCapacityError

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Cache(ABC, Generic[K, V]):
    """Abstract interface for a key-value cache with bounded capacity."""

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int):
            raise CacheCapacityError(f"Capacity must be an integer, got {type(capacity).__name__}.")
        if capacity <= 0:
            raise CacheCapacityError(f"Capacity must be positive, got {capacity}.")
        self._capacity = capacity

    # --- Public API (abstract) ---

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """Retrieve value by key. Returns None if key is not in the cache."""
        pass

    @abstractmethod
    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair."""
        pass

    @abstractmethod
    def delete(self, key: K) -> None:
        """Remove a key from the cache. Raises CacheKeyError if not found."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all entries from the cache."""
        pass

    @property
    def capacity(self) -> int:
        """Return the maximum capacity of the cache."""
        return self._capacity

    @property
    @abstractmethod
    def size(self) -> int:
        """Return the current number of entries in the cache."""
        pass

    # --- Dunder methods ---

    def __contains__(self, key: K) -> bool:
        """Support 'key in cache' syntax."""
        return self.get(key) is not None

    def __len__(self) -> int:
        """Support len(cache) syntax."""
        return self.size

    def __repr__(self) -> str:
        """Human-readable representation."""
        return f"{self.__class__.__name__}(capacity={self._capacity}, size={self.size})"
