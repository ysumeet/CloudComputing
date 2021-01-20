# [START imports]
import os
import js
import urllib
import jinja2
import webapp2
import requests
from google.appengine.api import users
from google.appengine.ext import ndb
from gaesessions import get_current_session

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# [START form_key]
def form_key(id):
    return ndb.Key('Form', id)
# [END form_key]

# [START create_entity]
def create_entity(id, form_data):
    element = Form(fever=form_data['fever'], cough=form_data['cough'], breath=form_data['breath'], muscle=form_data['muscle'], tired=form_data['tired'],
                   nasal=form_data['nasal'], throat=form_data['throat'], nausea=form_data['nausea'], taste=form_data['taste'], chills=form_data['chills'], isolate=form_data['isolate'])
    element.put()
    return element
# [END create_entity]

# [START Form]
class Form(ndb.Model):
    fever = ndb.StringProperty(indexed=False)
    cough = ndb.StringProperty(indexed=False)
    breath = ndb.StringProperty(indexed=False)
    muscle = ndb.StringProperty(indexed=False)
    tired = ndb.StringProperty(indexed=False)
    nasal = ndb.StringProperty(indexed=False)
    throat = ndb.StringProperty(indexed=False)
    nausea = ndb.StringProperty(indexed=False)
    taste = ndb.StringProperty(indexed=False)
    chills = ndb.StringProperty(indexed=False)
    isolate = ndb.StringProperty(indexed=False)
# [END Form]

# [START FormHandler]
class FormHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
    def post(self):
        user_id = self.request.get('user_id')
        state = self.request.get('state').strip().upper()
        if self.request.get('Submit') == 'Submit':
            form_data = {
                'fever': self.request.get('fever'),
                'cough': self.request.get('cough'),
                'breath': self.request.get('breath'),
                'muscle': self.request.get('muscle'),
                'tired': self.request.get('tired'),
                'nasal': self.request.get('nasal'),
                'throat': self.request.get('throat'),
                'nausea': self.request.get('nausea'),
                'taste': self.request.get('taste'),
                'chills': self.request.get('chills'),
                'isolate': self.request.get('isolate')
            }
            if not any([True for key,value in form_data.items() if value == '-- Select --']):
                element = create_entity(user_id, form_data)
                # code to add it into bigquery
                if any([True for key,value in form_data.items() if value == 'Yes']):
                    url = 'https://bw7plu7pni.execute-api.us-east-1.amazonaws.com/lambda_request_handler'
                    myobj = {'state': state}
                    json_data = requests.post(url, data = myobj)
                else:
                    # No COVID
                    print("Hello")
# [END FormHandler]

# [START app]
app = webapp2.WSGIApplication([
    ('/', FormHandler)
], debug=True)
# [END app]
