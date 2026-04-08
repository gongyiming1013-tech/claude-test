"""Cache wrapper that tracks hit/miss statistics."""

from typing import Hashable, Optional, TypeVar

from cache_interface import Cache

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class MonitoredCache(Cache[K, V]):
    """
    Wrapper that adds hit/miss monitoring to any Cache implementation.

    Intercepts get() calls to count cache hits and misses.
    All other operations are delegated directly to the inner cache.
    """

    def __init__(self, inner: Cache[K, V]) -> None:
        super().__init__(inner.capacity)
        self._inner = inner
        self._hits = 0
        self._misses = 0

    # --- Public API ---

    def get(self, key: K) -> Optional[V]:
        """Retrieve value by key and record hit or miss."""
        result = self._inner.get(key)
        if result is not None:
            self._hits += 1
        else:
            self._misses += 1
        return result

    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair."""
        self._inner.put(key, value)

    def delete(self, key: K) -> None:
        """Remove a key from the cache."""
        self._inner.delete(key)

    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._inner.clear()

    @property
    def size(self) -> int:
        """Return current number of entries."""
        return self._inner.size

    @property
    def hits(self) -> int:
        """Return total number of cache hits."""
        return self._hits

    @property
    def misses(self) -> int:
        """Return total number of cache misses."""
        return self._misses

    @property
    def hit_rate(self) -> float:
        """Return cache hit rate as a float between 0.0 and 1.0."""
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return self._hits / total

    @property
    def stats(self) -> dict[str, object]:
        """Return a summary dict of cache statistics."""
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self.hit_rate,
            "total_requests": self._hits + self._misses,
        }

    def reset_stats(self) -> None:
        """Reset hit/miss counters without clearing the cache data."""
        self._hits = 0
        self._misses = 0
