#!/usr/bin/env python

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os.path
import webapp2

class Shout(db.Model):
	message = db.StringProperty(
		required=True)
	when = db.DateTimeProperty(
		auto_now_add=True)
	who = db.StringProperty()

class MyHandler(webapp2.RequestHandler):
	def render_template(self, view_filename, params={}):
		path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
		self.response.out.write(template.render(path, params))

	def get(self):
		user = users.get_current_user()
		helloMessage = ''
		if user:
			helloMessage = 'Hello, ' + user.nickname()
		else:
			self.redirect(users.create_login_url(self.request.uri))
		shouts = db.GqlQuery('SELECT * FROM Shout ORDER BY when DESC')
		values = {
		'user' : user,
		'shouts' : shouts,
		'message' : helloMessage
		}
		self.render_template('shouts.html',values)
		
	def post(self):
		shout = Shout(
			message=self.request.get(
				'message'),
			who=self.request.get('who'))
		shout.put()
		self.redirect('/')

application = webapp2.WSGIApplication([
		(r'.*', MyHandler)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()