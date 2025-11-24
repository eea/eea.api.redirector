"""Storage utilities"""

import os
import logging
from redis import Redis
from zope.interface import implementer
from zope.component import getUtility
from eea.api.redirector.interfaces import IStorageUtility

logger = logging.getLogger("eea.api.redirector")


def patched_redirection_storage_get(self, old_path, default=None):
    """Get redirection target for old_path, checking also Redis.

    We can not register a custom utility for this as all existing aliases would be lost.
    """
    value = self._old_get(old_path, default)
    if value:
        return value

    # Check Redis storage
    rs = getUtility(IStorageUtility)
    value = rs.get(old_path)
    if value:
        logger.debug("Found redis value for %s: %s", old_path, value)
        return value.decode("utf-8")
    return default


@implementer(IStorageUtility)
class RedisStorageUtility:
    """Redis Storage Utility"""

    _timeout = None
    _db = None
    _server = None
    _port = None

    @property
    def timeout(self):
        """Get timeout from environment or default to 5 seconds."""
        if not self._timeout:
            try:
                self._timeout = int(os.environ.get("REDIS_TIMEOUT", 5))
            except ValueError:
                self._timeout = 5
        return self._timeout

    @property
    def db(self):
        """Get Redis DB index from environment or default to 0."""
        if not self._db:
            try:
                self._db = int(os.environ.get("REDIS_DB", 0))
            except ValueError:
                self._db = 0
        return self._db

    @property
    def server(self):
        """Get Redis server address from environment or default to localhost."""
        if not self._server:
            self._server = os.environ.get("REDIS_SERVER", "localhost")
        return self._server

    @property
    def port(self):
        """Get Redis server port from environment or default to 6379."""
        if not self._port:
            try:
                self._port = int(os.environ.get("REDIS_PORT", 6379))
            except Exception:
                self._port = 6379
        return self._port

    def get(self, key):
        """Get a value from Redis by key."""
        if not key:
            return None

        try:
            with Redis(
                host=self.server,
                port=self.port,
                db=self.db,
                socket_connect_timeout=self.timeout,
            ) as conn:
                return conn.get(key)
        except Exception as err:
            logger.exception(err)
            return None

    def set(self, key, value):
        """Set a value in Redis by key."""
        if not key:
            return None

        try:
            with Redis(
                host=self.server,
                port=self.port,
                db=self.db,
                socket_connect_timeout=self.timeout,
            ) as conn:
                return conn.set(key, value)
        except Exception as err:
            logger.exception(err)
            return None
