#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")

    def post(self):
        f = {'km': lambda x: str(float(x) * 0.621371192),
             'milje': lambda x: str(float(x) / 0.621371192)
        }
        enota = self.request.get('vnos')
        pretvorba = self.request.get('pretvornik')
        rezultat = ''
        try:
            rezultat = f[pretvorba](enota)
            params = {"message": rezultat}
            return self.render_template("pretvornik.html", params=params)
        except ValueError:
            rezultat = "Error: Incorrect Number"
            params = {"message": rezultat}
            return self.render_template("pretvornik.html", params=params)
        except KeyError:
            pass
        self.write(rezultat)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
