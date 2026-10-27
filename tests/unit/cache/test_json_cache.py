# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Tests for the JSON cache."""

import pytest
from graphrag_cache.json_cache import JsonCache
from graphrag_storage.memory_storage import MemoryStorage


@pytest.mark.asyncio
async def test_json_cache_round_trip():
    cache = JsonCache(MemoryStorage())

    await cache.set("key", {"text": "héllo", "items": [1, 2, 3]})

    assert await cache.get("key") == {"text": "héllo", "items": [1, 2, 3]}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        "[1, 2, 3]",
        '"a string"',
        "42",
        "true",
        '{"other": 1}',
    ],
)
async def test_json_cache_purges_payloads_that_are_not_envelopes(payload):
    """Valid JSON that is not a result envelope must not crash get()."""
    storage = MemoryStorage()
    cache = JsonCache(storage)
    await storage.set("key", payload)

    assert await cache.get("key") is None
    assert not await cache.has("key")


@pytest.mark.asyncio
async def test_json_cache_purges_invalid_json():
    storage = MemoryStorage()
    cache = JsonCache(storage)
    await storage.set("key", "{not json")

    assert await cache.get("key") is None
    assert not await cache.has("key")
