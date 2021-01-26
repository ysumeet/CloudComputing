# [START imports]
import os
import urllib
import json
import jinja2
import webapp2
# from requests import requests
from google.appengine.api import users
from google.appengine.ext.webapp import template
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

# [START Cred]
class Cred(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)
    state = ndb.StringProperty(indexed=False)
# [End Cred]

# [START Form]
class Form(ndb.Model):
    cred = ndb.StructuredProperty(Cred)
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

# [START create_entity]
def create_entity(id, cred, form_data):
    element = Form(id=id, cred=cred, fever=form_data['fever'], cough=form_data['cough'], breath=form_data['breath'], muscle=form_data['muscle'], tired=form_data['tired'],
                   nasal=form_data['nasal'], throat=form_data['throat'], nausea=form_data['nausea'], taste=form_data['taste'], chills=form_data['chills'], isolate=form_data['isolate'])
    element.put()
    return element
# [END create_entity]

# [START create_user]
def create_user(id, cred):
    element = Form(id=id, cred=cred)
    element.put()
    return element
# [END create_user]

# [START Login]
class Login(webapp2.RequestHandler):
   
    LOGIN_PAGE = 'login.html'
    
    def get(self):    
        template = JINJA_ENVIRONMENT.get_template(self.LOGIN_PAGE)
        self.response.write(template.render())
    
    def post(self): 
        email = self.request.get('email').strip()
        password = self.request.get('password').strip()
        template_values = {
                'error' : 'User id or password is invalid.',
            }
        if email != '' or password != '':
            users = Form.query().filter(Form.key == form_key(email)).fetch(1)
            if len(users) > 0  and  users[0].cred.password == password:
                print(users )
                session = get_current_session()
                session['user'] = users[0]
                session['email'] = users[0].key.id()
                session['user_name'] = users[0].cred.name
                session['password'] = users[0].cred.password
                session['state'] = users[0].cred.state
                self.redirect('/main')
            else:   
                template = JINJA_ENVIRONMENT.get_template(self.LOGIN_PAGE)
                self.response.write(template.render(template_values))
        else:      
            template = JINJA_ENVIRONMENT.get_template(self.LOGIN_PAGE)
            self.response.write(template.render(template_values))
# [End Login]


# [START Register]
class Register(webapp2.RequestHandler):
    
    REGISTER_PAGE = 'register.html'
    
    def get(self):    
        template = JINJA_ENVIRONMENT.get_template(self.REGISTER_PAGE)
        self.response.write(template.render())
        
    def post(self): 
        template_values = {}
        email = self.request.get('email').strip()
        username = self.request.get('user_id').strip()
        state = self.request.get('state').strip()
        password = self.request.get('password').strip()
        if email != '':
            users = Form.query().filter(Form.key == form_key(email)).fetch(1)
            if len (users)> 0:
                template_values = {
                    'error' : 'Provided email is already used, please try with a differant email',
                }
                template = JINJA_ENVIRONMENT.get_template(self.REGISTER_PAGE)
                self.response.write(template.render(template_values))
            else:
                cred = Cred(name=username, password= password, state= state)
                element = create_user(email, cred)
                print(element)
                self.redirect('/')
# [End Register]

# [START FormHandler]
class FormHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        email = session['email']
        uname = session['name']
        password = session['password']
        state = session['state']
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
        # user_id = self.request.get('user_id')
        # state = self.request.get('state').strip().upper()
        if any([True for key,value in form_data.items() if value == '']):
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render({'message':'Please answer all the questions!'}))
        else:
            # update the users record in datastore
            cred = Cred(name=uname, password=password,state= state)
            element = create_entity(email, cred, form_data)
            print(element)
            # Data studio code
            if any([True for key,value in form_data.items() if value == 'yes']):
                # send the json data
                session['state'] = state
                self.redirect('/map')
            else:
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render({'message':'No covid!'}))
                print("No Covid")
    def get(self):
        session = get_current_session()
        if session.is_active():
            user = session['user']
            uname = user.cred.name
            template_values = {
                'uname': uname
            }            
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')
# [END FormHandler]

# [START MapHandler]
class MapHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        # receive and assign the json data
        payload = {'state': session['state']}
        template = JINJA_ENVIRONMENT.get_template('locations.html')
        self.response.write(template.render(payload))
# [END MapHandler]

# [START UpdateName]
class UpdateName(webapp2.RequestHandler):
    USERNAME_PAGE = 'name.html'
    def get(self):        
        session = get_current_session()
        if not session.is_active():
            self.redirect('/')
        else:
            template = JINJA_ENVIRONMENT.get_template(self.USERNAME_PAGE)
            self.response.write(template.render())
    
    def post(self): 
        session = get_current_session()
        if not session.is_active():
            self.redirect('/')
        else:            
            username = self.request.get('username').strip()
            if username == '':
                template_values = {
                    'error':'User name cannot be empty'
                }
                template = JINJA_ENVIRONMENT.get_template(self.USERNAME_PAGE)
                self.response.write(template.render(template_values))
            else:
                user = session['user']
                user.cred.name = username
                user.put()

                session['user'] = user
                session['user_name'] = user.cred.name
                self.redirect('/main')
# [End UpdateName]

# [START UpdatePassword]
class UpdatePassword(webapp2.RequestHandler):
   
    PASSWORD_PAGE = 'password.html'
    
    def get(self): 
        session = get_current_session()
        if session.is_active():
            template = JINJA_ENVIRONMENT.get_template(self.PASSWORD_PAGE)
            self.response.write(template.render())
        else:
            self.redirect('/')
    
    def post(self):
        session = get_current_session()

        oldpassword = self.request.get('oldpassword').strip()
        newpassword = self.request.get('newpassword').strip()  

        if oldpassword != str(session['password']):
            template_values = {
                'error': 'User password is incorrect'
            }
            template = JINJA_ENVIRONMENT.get_template(self.PASSWORD_PAGE)
            self.response.write(template.render(template_values))
        else:         
            user = session['user']
            user.cred.password = newpassword
            user.put()
            self.redirect('/logout')
# [End UpdatePassword]


# [START UpdateState]
class UpdateState(webapp2.RequestHandler):
   
    STATE_PAGE = 'state.html'
    
    def get(self): 
        session = get_current_session()
        if session.is_active():
            user = session['user']
            old_state = user.cred.state
            template_values = {
                'state': old_state
            }            
            template = JINJA_ENVIRONMENT.get_template(self.STATE_PAGE)
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')
    
    def post(self): 
        session = get_current_session()
        if not session.is_active():
            self.redirect('/')
        else:            
            state = self.request.get('state').strip()
            if state == '':
                template_values = {
                    'error':'Please Select a State'
                }
                template = JINJA_ENVIRONMENT.get_template(self.USERNAME_PAGE)
                self.response.write(template.render(template_values))
            else:
                user = session['user']
                user.cred.state = state
                user.put()

                session['user'] = user
                session['state'] = user.cred.state
                self.redirect('/main')
# [End UpdateState]

# [START Logout]
class Logout(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        session.terminate()
        self.redirect('/')
# [End Logout]

# [START app]
app = webapp2.WSGIApplication([
    ('/', Login),
    ('/register', Register),
    ('/main', FormHandler),
    ('/name', UpdateName),  
    ('/password', UpdatePassword),
    ('/state', UpdateState),
    ('/logout', Logout),
    ('/map', MapHandler),
], debug=True)
# [END app]
            