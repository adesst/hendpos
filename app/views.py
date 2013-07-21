from flask import render_template, request, session, flash, redirect
from app import *
from flask.ext.babel import lazy_gettext
import datetime
import traceback, logging

POST_FORM_LABEL = 0
POST_FORM_VALUE = 1

def pop_up_link(link_url, link_string):
    ret_str = '''<a href="%s" >%s</a>''' %( link_url, link_string)
    return ret_str

def log_create_user(kwargs):
    auth_user_id = kwargs['auth_user_id']
    message = kwargs['message']
    tr_date = datetime.datetime.now()
    pos_log = PosLog(auth_user_id, tr_date, message)
    db_session.add(pos_log)
    return True

@app.route('/')
@app.route('/index')
@login_required('/')
def index():
    return render_template('default/index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.form:
        form_data = dict(request.form)
        next_url = 'index'
        url_query = dict(request.args)
        user = form_data['username']
        flash(lazy_gettext('Hello %s' %str(user[0])))
        if url_query.has_key('next'):
            next_url = url_query['next']
        return redirect(u'%s' %next_url)
    else:
        session['AuthUser'] = {'id' : 1}
        return render_template('default/login.html')

@app.route('/user/new', methods=['POST','GET'])
@login_required()
def user_new():
    db_session.rollback()
    error_message = []
    form = FieldSet(User)
    form_data = None
    if request.form :
        form_data = dict(request.form.items())
        for key, value in form_data.iteritems() :
            if value == '':
                error_message.append( lazy_gettext(' %s is NULL' %( key )) )
        if len( error_message ) == 0:
            user = User()
            user.set_fields(form_data)
            db_session.add(user)
            try:
                message = "New user %s has been added " %pop_up_link(('/user/view/%s') %user.email, user.username)
                params = {'auth_user_id' : session['AuthUser']['id'], \
                    'message' : message,
                }
                if not log_create_user(params):
                    raise ValueError
                else:
                    db_session.commit()
                    return str(message)
            except Exception, e:
                db_session.rollback()
                if isinstance(e, IntegrityError ):
                    message = lazy_gettext('Error: Email has been taken')
                else:
                    message = "Error: %s %s" %(e, type(e))
                logging.error('%s %s' %(traceback.print_exc(), message))
                error_message.append( message )
        else:
            pass
    return render_template('default/user_new.html', error_message = error_message, form = form_data or None)


@app.route('/user/edit/<id>')
@app.route('/user/edit/', methods=['POST'])
@login_required()
def user_edit(id=None):
    if request.form :
        return 'Form is not empty'
        # redirect to user_view
    else:
        # read the DB
        message = ''
        obj = User.query.filter_by(id=id).first()
        # set the form
        return render_template('default/user_edit.html', message = message, form=obj)

@app.route('/user/view/<email>')
@login_required()
def user_view(email=None):
    if email == None:
        return redirect(url_for('user_list'))
    else:
        obj = User.query.filter_by(email=email).first()
        print form
        return 'Hello'

@app.route('/user/renew_card/<id>')
@app.route('/user/renew_card/<id>/<card_id>')
def user_renew_card(id, card_id = None):
    print id, ' ', card_id
    if card_id :
        # renew card ID
        # throw ok
        return 'Renew Card Ok'
    return 'Renew Card menu'

@app.route('/user/delete/<id>')
def user_delete(id):
    pass

@app.route('/user/list')
def user_list():
    pass

#@app.route('/transaction/add/id')
#@app.route('/transaction/edit/id')
#@app.route('/transaction/delete/id')
#@app.route('/transaction/view/id')
#@app.route('/transaction/list')
