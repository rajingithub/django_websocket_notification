in main project folders, create a new ```asgi.py``` file and add the below code

```
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from websocket_connection.middleware import WebsocketAuthMiddleware
from websocket_connection.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings') # replace myproject with our actual project name

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        WebsocketAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})
```


in projects settings.py file

```
INSTALLED_APPS = (
    'daphne',
    ...
    ...
    ...
    'channels'

)

    },
]

# WSGI_APPLICATION = 'myproject.wsgi.application'
ASGI_APPLICATION = 'myproject.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],#redis_host-> 127.0.0.1 in local
        },
    },
}

```
requires latest redis around version7
url : ws://0.0.0.0:8000/websocket

