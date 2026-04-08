"""Thread-safe wrapper for any Cache implementation."""

import threading
from typing import Hashable, Optional, TypeVar

from cache_interface import Cache

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class ThreadSafeCache(Cache[K, V]):
    """
    Thread-safe wrapper around any Cache implementation.

    Uses a reentrant lock (RLock) to serialize all cache operations.
    Pass any Cache instance, and this wrapper makes it safe for
    concurrent access.
    """

    def __init__(self, inner: Cache[K, V]) -> None:
        super().__init__(inner.capacity)
        self._inner = inner
        self._lock = threading.RLock()

    # --- Public API ---

    def get(self, key: K) -> Optional[V]:
        """Thread-safe get. Acquires lock before delegating to inner cache."""
        with self._lock:
            return self._inner.get(key)

    def put(self, key: K, value: V) -> None:
        """Thread-safe put. Acquires lock before delegating to inner cache."""
        with self._lock:
            self._inner.put(key, value)

    def delete(self, key: K) -> None:
        """Thread-safe delete. Acquires lock before delegating to inner cache."""
        with self._lock:
            self._inner.delete(key)

    def clear(self) -> None:
        """Thread-safe clear. Acquires lock before delegating to inner cache."""
        with self._lock:
            self._inner.clear()

    @property
    def size(self) -> int:
        """Return current number of entries, thread-safe."""
        with self._lock:
            return self._inner.size
