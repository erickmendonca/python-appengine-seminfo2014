#!/usr/bin/env python

#import wsgiref.handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
 import template

class Shout(db.Model):
	message = db.StringProperty(
		required=True)
	when = db.DateTimeProperty(
		auto_now_add=True)
	who = db.StringProperty()

class MyHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		helloMessage = ''
		if user:
			helloMessage = 'Hello, ' + user.nickname()
		else:
			self.redirect(users.create_login_url(self.request.uri))
		shouts = db.GqlQuery('SELECT * FROM Shout ORDER BY when DESC')
		values = {
		'shouts' : shouts,
		'message' : helloMessage
		}
		self.response.out.write(
			unicode(template.render('main.html',
									values)))
	def post(self):
		shout = Shout(
			message=self.request.get(
				'message'),
			who=self.request.get('who'))
		shout.put()
		self.redirect('/')

application = webapp.WSGIApplication([
		(r'.*', MyHandler)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()