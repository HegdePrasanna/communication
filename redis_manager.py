import asyncio
import redis.asyncio as aioredis
import json
from fastapi import WebSocket
import os

class RedisPubSubManager:
    """
        Initializes the RedisPubSubManager.
        For my ref: https://medium.com/@nandagopal05/scaling-websockets-with-pub-sub-using-python-redis-fastapi-b16392ffe291

    Args:
        host (str): Redis server host.
        port (int): Redis server port.
    """

    # def __init__(self, host='localhost', port=6379):
    def __init__(self, host='192.168.0.102', port=6379):
        # Get the Redis host from the environment variable
        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        self.redis_host = redis_host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        """
        Establishes a connection to Redis.

        Returns:
            aioredis.Redis: Redis connection object.
        """
        return aioredis.Redis(host=self.redis_host,
                            port=self.redis_port,
                            auto_close_connection_pool=False)

    async def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub client.
        """
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, room_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            room_id (str): Channel or room ID.
            message (str): Message to be published.
        """
        await self.redis_connection.publish(room_id, message)

    async def subscribe(self, room_id: str) -> aioredis.Redis:
        """
        Subscribes to a Redis channel.

        Args:
            room_id (str): Channel or room ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            room_id (str): Channel or room ID to unsubscribe from.
        """
        await self.pubsub.unsubscribe(room_id)