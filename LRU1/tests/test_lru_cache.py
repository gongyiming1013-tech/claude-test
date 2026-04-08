"""Tests for LRUCache implementation."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lru_cache import LRUCache
from exceptions import CacheCapacityError, CacheKeyError


class TestLRUCacheInit:
    """Tests for cache initialization and capacity validation."""

    def test_create_with_valid_capacity(self) -> None:
        cache = LRUCache(capacity=10)
        assert cache.capacity == 10
        assert cache.size == 0

    def test_zero_capacity_raises(self) -> None:
        with pytest.raises(CacheCapacityError):
            LRUCache(capacity=0)

    def test_negative_capacity_raises(self) -> None:
        with pytest.raises(CacheCapacityError):
            LRUCache(capacity=-5)

    def test_non_integer_capacity_raises(self) -> None:
        with pytest.raises(CacheCapacityError):
            LRUCache(capacity=3.5)  # type: ignore


class TestLRUCacheGetPut:
    """Tests for basic get and put operations."""

    def test_put_and_get_single(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        assert cache.get("a") == 1

    def test_get_missing_key_returns_none(self) -> None:
        cache = LRUCache(capacity=5)
        assert cache.get("nonexistent") is None

    def test_put_updates_existing_key(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        cache.put("a", 99)
        assert cache.get("a") == 99
        assert cache.size == 1

    def test_put_multiple_keys(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.size == 3


class TestLRUCacheEviction:
    """Tests for LRU eviction behavior."""

    def test_evict_least_recently_used(self) -> None:
        """When full, putting a new key should evict the LRU item."""
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # Cache is full: [c, b, a] (c is most recent)
        cache.put("d", 4)
        # 'a' should be evicted as the least recently used
        assert cache.get("a") is None
        assert cache.get("d") == 4
        assert cache.size == 3

    def test_get_updates_access_order(self) -> None:
        """Accessing a key via get() should prevent it from being evicted."""
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # Access 'a' so it becomes most recently used
        cache.get("a")
        # Now add 'd' — 'b' should be evicted (it's the LRU now)
        cache.put("d", 4)
        assert cache.get("b") is None
        assert cache.get("a") == 1

    def test_put_update_refreshes_access_order(self) -> None:
        """Updating an existing key via put() should refresh its position."""
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        # Update 'a' — it becomes most recently used
        cache.put("a", 100)
        # Add 'd' — 'b' should be evicted
        cache.put("d", 4)
        assert cache.get("b") is None
        assert cache.get("a") == 100

    def test_capacity_one(self) -> None:
        """Cache with capacity=1 should evict on every new put."""
        cache = LRUCache(capacity=1)
        cache.put("a", 1)
        assert cache.get("a") == 1
        cache.put("b", 2)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.size == 1

    def test_eviction_sequence(self) -> None:
        """Verify correct eviction order over multiple insertions."""
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        # Evicts 'a'
        cache.put("c", 3)
        assert cache.get("a") is None
        # Evicts 'b'
        cache.put("d", 4)
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4


class TestLRUCacheDelete:
    """Tests for the delete operation."""

    def test_delete_existing_key(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        cache.delete("a")
        assert cache.get("a") is None
        assert cache.size == 0

    def test_delete_missing_key_raises(self) -> None:
        cache = LRUCache(capacity=5)
        with pytest.raises(CacheKeyError):
            cache.delete("nonexistent")

    def test_delete_frees_capacity(self) -> None:
        """After deleting, a new item should not trigger eviction."""
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.delete("a")
        cache.put("c", 3)
        # 'b' should still be present since we freed a slot
        assert cache.get("b") == 2
        assert cache.get("c") == 3


class TestLRUCacheClear:
    """Tests for the clear operation."""

    def test_clear_empties_cache(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.clear()
        assert cache.size == 0
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.get("c") is None

    def test_clear_then_reuse(self) -> None:
        """Cache should work normally after clear."""
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.clear()
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.size == 2
        assert cache.get("b") == 2
        assert cache.get("c") == 3


class TestLRUCacheDunderMethods:
    """Tests for __contains__, __len__, and __repr__."""

    def test_contains(self) -> None:
        cache = LRUCache(capacity=5)
        cache.put("a", 1)
        assert "a" in cache
        assert "b" not in cache

    def test_len(self) -> None:
        cache = LRUCache(capacity=5)
        assert len(cache) == 0
        cache.put("a", 1)
        cache.put("b", 2)
        assert len(cache) == 2

    def test_repr(self) -> None:
        cache = LRUCache(capacity=10)
        cache.put("a", 1)
        result = repr(cache)
        assert "LRUCache" in result
        assert "10" in result
