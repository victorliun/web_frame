
import os
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
import pdb
from test_view import *

class Web(object):

    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)
        self.url_map = Map()
        self.view_functions = []

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            self.url_map.add(Rule(rule, endpoint, **options))
            self.view_functions.append(endpoint)
            return f
        return decorator

    def register(self, rule, endpoint, **options):
        self.url_map.add(Rule(rule, endpoint=endpoint, **options))
        self.view_functions.append(endpoint)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
    
    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

web = Web()
web.register("/", on_new_url)
web.register("/<short_id>+", on_short_link_details)
web.register("/<short_id>", on_follow_short_link)