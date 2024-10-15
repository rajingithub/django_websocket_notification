

from rest_framework.exceptions import AuthenticationFailed


class WebsocketAuthMiddleware:
    def __init__(self,app):
        self.app = app
    
    def __call__(self,scope,receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            authorization = headers[b'authorization']
            # TODO : send token or cookies in the connection and authorize the user accordingly
            user_id = authorization.decode('utf-8').split()[-1]
            print("authorization present in headers",authorization)
            scope['user_id'] = user_id
        else:
            print("authorization not present in headers")
            raise AuthenticationFailed(detail = "Authentication Failed")
        return self.app(scope, receive, send)