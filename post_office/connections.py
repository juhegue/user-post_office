from threading import local

from django.core.mail import get_connection

from .settings import get_backend


# Copied from Django 1.8's django.core.cache.CacheHandler
class ConnectionHandler:
    """
    A Cache Handler to manage access to Cache instances.

    Ensures only one instance of each alias exists per thread.
    """
    def __init__(self):
        self._connections = local()

    def __getitem__(self, alias):
        alias, user_id = alias
        name = f'{alias}_{user_id}'
        try:
            return self._connections.connections[name]
        except AttributeError:
            self._connections.connections = {}
        except KeyError:
            pass

        try:
            backend = get_backend(alias)
        except KeyError:
            raise KeyError('%s is not a valid backend alias' % alias)

        connection = get_connection(backend, user_id=user_id)
        connection.open()
        self._connections.connections[name] = connection
        return connection

    def all(self):
        return getattr(self._connections, 'connections', {}).values()

    def close(self):
        for connection in self.all():
            connection.close()


connections = ConnectionHandler()
