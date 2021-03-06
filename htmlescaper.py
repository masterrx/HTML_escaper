import os
import webapp2
import jinja2
import cgi
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter 

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))  
        
class Main(Handler):
    def get(self):
        self.render('test.html')
        
    def post(self):
        params = {}
        params['input'] = self.request.get("input")
        params['output'] = cgi.escape(self.request.get("input"))
        params['formatted'] = highlight(self.request.get("input"), PythonLexer(), HtmlFormatter())
        self.render('test.html',**params)
                    
app = webapp2.WSGIApplication([('/',Main)])
