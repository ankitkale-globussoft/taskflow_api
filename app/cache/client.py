import msgpack
import redis.asyncio as aioredis
from typing import Any
from app.config import settings

class CacheClient:
    prefix = "taskflow"

    def __init__(self):
        self._redis: aioredis.Redis | None = None

    async def connect(self):
        self._redis = await aioredis.from_url(
            url=settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=False
        )

    async def disconnect(self):
        if self._redis:
            await self._redis.aclose()

    def _make_key(self, key: str) -> str:
        return f"{self.prefix}:{key}"
    
    async def get(self, key: str) -> Any | None:
        try:
            raw = await self._redis.get(self._make_key(key))
            if not raw:
                return None
            return msgpack.unpackb(raw, raw=False)
        except Exception:
            return None
        
    async def set(self, key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS) -> Any:
        try:
            packed = msgpack.packb(value, use_bin_type=True)
            await self._redis.set(self._make_key(key), packed, ex=ttl)
        except Exception:
            pass

    async def delete(self, key: str) -> None:
        try:
            await self._redis.delete(self._make_key(key))
        except Exception:
            pass

    async def delete_pattern(self, pattern: str) -> None:
        try:
            full_pattern = self._make_key(pattern)
            keys = await self._redis.keys(full_pattern)
            if keys:
                await self._redis.delete(*keys)
        except Exception:
            pass

cache = CacheClient()