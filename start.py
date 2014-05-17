import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from core.app import web

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    web.wsgi_app = SharedDataMiddleware(web.wsgi_app, {
        '/static':  os.path.join(os.path.dirname(__file__), 'static')
    })

    run_simple('127.0.0.1', 5000, web, use_debugger=True, use_reloader=True)
