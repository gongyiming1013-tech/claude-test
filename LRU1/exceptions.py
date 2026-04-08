"""Custom exception hierarchy for cache operations."""


class CacheError(Exception):
    """Base exception for all cache operations."""

    pass


class CacheCapacityError(CacheError):
    """Raised when cache capacity is invalid (e.g., zero or negative)."""

    pass


class CacheKeyError(CacheError):
    """Raised when a cache key operation fails (e.g., key not found)."""

    pass
