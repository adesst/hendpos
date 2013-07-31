from flask import render_template, request, session, flash, redirect
from app import *
from flask.ext.babel import lazy_gettext
import datetime
from dateutil import parser
import traceback, logging
import copy

POST_FORM_LABEL = 0
POST_FORM_VALUE = 1
REGISTERED_USER = 90
TOP_UP = '1'
SELL = '11'
ATTENDANCE = '11'

def pop_up_link(link_url, link_string):
    ret_str = '''<a href="%s" >%s</a>''' %( link_url, link_string)
    return ret_str

def pos_log(kwargs):
    user_auth_id = kwargs['auth_user_id']
    user_id = kwargs['user_id']
    message = kwargs['message']
    tr_date = datetime.datetime.now()
    pos_log = PosLog(user_auth_id, user_id, tr_date, message)
    db_session.add(pos_log)
    return True

@app.route('/')
@app.route('/index')
#@login_required('/')
def index():
    session['AuthUser'] = {'id' : 1}
    return render_template('default/index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.form:
        form_data = dict(request.form)
        next_url = 'index'
        url_query = dict(request.args)
        user = form_data['username']
        flash(lazy_gettext('Hello %s' %str(user[0])))
        session['AuthUser'] = {'id' : 1}
        if url_query.has_key('next'):
            next_url = url_query['next']
        return redirect(u'%s' %next_url)
    else:
        session['AuthUser'] = {'id' : 1}
        return render_template('default/login.html')

@app.route('/user/new', methods=['POST','GET'])
#@login_required()
def user_new():
    session['AuthUser'] = {'id' : 1}
    error_message = []
    form_data = None
    if request.form :
        form_data = dict(request.form.items())
        for key, value in form_data.iteritems() :
            if value == '':
                error_message.append( lazy_gettext(' %s is NULL' %( key )) )
        if len( error_message ) == 0:
            try:
                user = User()
                form_data['username'] = form_data['card_uid']
                form_data['card_no'] = form_data['card_uid']
                form_data['group_id'] = REGISTERED_USER
                user.set_fields(form_data)
                user.date_create = datetime.datetime.now()
                db_session.add(user)
                db_session.commit()
                message = "New user %s has been added " % pop_up_link(('/user/view/%s') %user.id, user.username)
                params = {'auth_user_id' : session['AuthUser']['id'], \
                    'user_id' : user.id, \
                    'message' : message, \
                }
                if not pos_log(params):
                    raise ValueError
                else:
                    flash(message)
                    db_session.commit()
                    form_data = None
            except Exception, e:
                db_session.rollback()
                message = "Error: %s %s" %(e, type(e))
                logging.error('%s %s' %(traceback.print_exc(), message))
                error_message.append( message )
        else:
            pass
    return render_template('default/user_new.html', error_message = error_message, form = form_data or None)


@app.route('/user/edit/<id>', methods=['GET','POST'])
@app.route('/user/edit/', methods=['POST','GET'])
#@login_required()
def user_edit(id=None):
    session['AuthUser'] = {'id' : 1}
    error_message = []
    if request.form :
        form_data = dict(request.form.items())
        for key, value in form_data.iteritems() :
            if value == '':
                error_message.append( lazy_gettext(' %s is NULL' %( key )) )
        if len( error_message ) == 0:
            try:
                id = copy.copy(u'%s' % form_data['id'])
                del form_data['id']
                form_data['date_create'] = parser.parse(form_data['date_create'])
                user_query = db_session.query(User).filter(User.id==id)
                user_query.update(form_data)
                user = user_query.one()
                userlog = UserLog()
                poslog = PosLog()
                userlog.set_fields(form_data)
                userlog.user_id = id
                userlog.date_log = datetime.datetime.now()
                db_session.add(userlog)
                message = lazy_gettext("User %s has been updated " %pop_up_link(('/user/view/%s') %user.id, user.username))
                params = {'auth_user_id' : session['AuthUser']['id'], \
                    'user_id' : user.id, \
                    'message' : message, \
                }
                if not pos_log(params):
                    raise ValueError
                else:
                    flash(message)
                    db_session.flush()
                    db_session.commit()
            except Exception, e:
                db_session.rollback()
                message = "Error: %s %s" %(e, type(e))
                flash(message)
                logging.error('%s %s' %(traceback.print_exc(), message))
                error_message.append( message )
                return redirect(url_for('user_edit', id=id))
            return redirect(url_for('user_list'))
        else:
            pass
    else:
        message = ''
        obj = None
        try:
            obj = User.query.filter_by(id=id).first()
            return render_template('default/user_edit.html', message = message, form=obj)
        except Exception, e:
            message = "Error: %s %s" %(e, type(e))
            flash(message)
            logging.error('%s %s' %(traceback.print_exc(), message))
            return redirect(url_for('user_edit', id=id))

@app.route('/user/view/<id>')
#@login_required()
def user_view(id=None):
    if id == None:
        flash(lazy_gettext('Error: No user ID specified, redirecting to list'))
        return redirect(url_for('user_list'))
    else:
        try:
            user = User.query.filter_by(id=id).first()
            if user is None:
                raise ValueError(lazy_gettext('Error: User ID is not exists'))
            mutations = Balance.query.filter_by(user_id=id)
            return render_template('default/user_view.html', user=user, mutations=mutations)
        except Exception, e:
            message = "Error: %s %s" %(e, type(e))
            flash(message)
            logging.error('%s %s' %(traceback.print_exc(), message))
            return redirect(url_for('user_list'))

@app.route('/user/renew_card/<id>')
def user_renew_card(id=None):
    if id == None :
        flash(lazy_gettext('Error: No user ID specified, redirecting to list'))
        return redirect(url_for('user_list'))
    elif request.form :
        pass
    else:
        pass
    user = User.query.filter_by(id=id).first()
    return render_template('default/user_renew_card.html', user=user)

@app.route('/user/delete/<id>')
def user_delete(id):
    session['AuthUser'] = {'id' : 1}
    error_message = []
    if id == None:
        flash(lazy_gettext('Error: No user ID specified, redirecting to list'))
    else:
        try:
            user_query = User.query.filter_by(id=id)
            user = user_query.one()
            form_data = copy.copy(user.__dict__)
            form_data = {key: value for key, value in form_data.iteritems() if not key.startswith("_") }
            form_data['status'] = 1
            user_query.update(form_data)
            del form_data['id'], form_data['status']
            userlog = UserLog()
            userlog.set_fields(form_data)
            userlog.date_log = datetime.datetime.now()
            userlog.user_id = user.id
            db_session.add(userlog)
            message = "User %s has been deleted " % (user.username)
            params = {'auth_user_id' : session['AuthUser']['id'], \
                'user_id' : user.id, \
                'message' : message, \
            }
            if not pos_log(params):
                raise ValueError
            else:
                db_session.flush()
                db_session.commit()
                return str(message)
        except Exception, e:
            db_session.rollback()
            message = "Error: %s %s" %(e, type(e))
            flash(message)
            logging.error('%s %s' %(traceback.print_exc(), message))
            error_message.append( message )
    return redirect(url_for('user_list'))

@app.route('/user/list')
@app.route('/user')
def user_list():
    users = db_session.query(User).filter(or_(User.status==None, User.status==0)).all()
    return render_template('default/user_list.html', users=users)

@app.route('/transaction_pre_add/<txtype>')
def transaction_pre_add(txtype = None):
    if txtype == None:
        flash(lazy_gettext('Error: No user ID specified, redirecting to frontpage'))
        return redirect(url_for('index'))
    else:
        pass
    if txtype == '1':
        str_txtype = lazy_gettext('TopUp')
    elif txtype == '11':
        str_txtype = lazy_gettext('Sell')
    elif txtype == '2':
        str_txtype = lazy_gettext('Attendance')
    else:
        str_txtype = lazy_gettext('Unknown')
    return render_template('default/transaction_pre_add.html', txtype=txtype, str_txtype=str_txtype)

@app.route('/transaction_add', methods=['POST'])
def transaction_add():
    session['AuthUser'] = {'id' : 1}
    form_data = None
    txtype_id = None
    error_message = []
    if request.form :
        try:
            form_data = dict(request.form.items())
            txtype_id = form_data['txtype_id']
            user_query = db_session.query(User).filter(User.card_uid==form_data['card_uid'])
            user = user_query.one()
            if 'amount' in form_data:
                balance = Balance()
                if float(form_data['amount']) <= 0:
                   flash(lazy_gettext('Error: Amount must be >= 0'))
                   return redirect(url_for('transaction_pre_add', txtype=txtype_id))
                if form_data['txtype_id'] == TOP_UP:
                    form_data['user_id'] = user.id
                    form_data['remain'] = float(form_data['amount']) + float(user.balance)
                    form_data['tr_date'] = datetime.datetime.now()
                    balance.set_fields(form_data)
                    db_session.add(balance)
                    user_data = {key: value for key, value in user.__dict__.iteritems() if not key.startswith("_")}
                    user_data['balance'] = form_data['remain']
                    user_query.update(user_data)
                    db_session.flush()
                    db_session.commit()
                    message = "Transaction %s of TOP-UP %s has been added " % \
                        (
                            pop_up_link(url_for('transaction_view', id=balance.id), form_data['amount']) ,
                            pop_up_link(url_for('user_view', id=user.id), user.username)
                        )
                    params = {'auth_user_id' : session['AuthUser']['id'], \
                        'user_id' : user.id, \
                        'message' : message, \
                    }
                    if not pos_log(params):
                        raise ValueError
                    flash(lazy_gettext(message))
                    db_session.flush()
                    db_session.commit()
                elif form_data['txtype_id'] == SELL:
                    form_data['user_id'] = user.id
                    form_data['remain'] = float(user.balance) - float(form_data['amount'])
                    if form_data['remain'] < 0 :
                       flash(lazy_gettext('Error: Amount of Sales exists balance'))
                       return redirect(url_for('transaction_pre_add', txtype=txtype_id))
                    form_data['tr_date'] = datetime.datetime.now()
                    balance.set_fields(form_data)
                    db_session.add(balance)
                    user_data = {key: value for key, value in user.__dict__.iteritems() if not key.startswith("_")}
                    user_data['balance'] = form_data['remain']
                    user_query.update(user_data)
                    db_session.flush()
                    db_session.commit()
                    message = "Transaction %s of SELL %s has been added " % \
                        (
                            pop_up_link(url_for('transaction_view', id=balance.id), form_data['amount']) ,
                            pop_up_link(url_for('user_view', id=user.id), user.username)
                        )
                    params = {'auth_user_id' : session['AuthUser']['id'], \
                        'user_id' : user.id, \
                        'message' : message, \
                    }
                    if not pos_log(params):
                        raise ValueError
                    flash(lazy_gettext(message))
                    db_session.flush()
                    db_session.commit()
                else:
                    flash(lazy_gettext('Error: Unknown txtype_id of Transaction'))
                return redirect(url_for('transaction_pre_add', txtype=txtype_id))
            elif 'card_uid' in form_data:
                form_data = {key : value for key, value in user.__dict__.iteritems() if not key.startswith("_") }
            else:
                flash(lazy_gettext('Error: Form forgery detected'))
                return redirect(url_for('index'))
        except Exception, e:
            db_session.rollback()
            message = "Error: %s %s" %(e, type(e))
            logging.error('%s %s' %(traceback.print_exc(), message))
            error_message.append( message )
    return render_template('default/transaction_add.html', form=form_data or None, txtype_id=txtype_id)

@app.route('/transaction_edit/<id>')
def transaction_edit(id):
    return lazy_gettext('Error: Currently unavailable')

@app.route('/transaction_delete/<id>', methods=['GET','POST'])
def transaction_delete(id=None):
    if id == None:
        flash(lazy_gettext('Error: No user ID specified, redirecting to Transaction List'))
    else:
        try:
            balance_query = Balance.query.filter_by(id=id)
            balance = balance.one()
        except Exception as e:
            db_session.rollback()
            message = "Error: %s %s" %(e, type(e))
            flash(message)
            logging.error('%s %s' %(traceback.print_exc(), message))
    return redirect(url_for('transaction_list'))

@app.route('/transaction_view/<id>')
def transaction_view(id=None):
    if id == None:
        flash(lazy_gettext('Error: No user ID specified, redirecting to Transaction List'))
        return redirect(url_for('transaction_list'))
    else:
        form = db_session.query(Balance, User).filter(Balance.user_id==User.id, Balance.id == id).first()
        if form:
            return render_template('default/transaction_view.html', form=form)
        else:
            flash(lazy_gettext('Error: Transaction %s is not exists' % id))
            return redirect(url_for('transaction_list'))

@app.route('/transaction_list')
@app.route('/transaction_list/')
def transaction_list():
    mutations = db_session.query(Balance, User).filter(Balance.user_id==User.id)
    return render_template('default/transaction_list.html', mutations=mutations)

@app.route('/poslog/list/<limit>', methods=['GET','POST'])
@app.route('/poslog/list', methods=['GET','POST'])
def poslog_list(limit=None):
    if limit == None:
        limit = 100
    mutations = db_session.query(PosLog).order_by(desc(PosLog.tr_date)).limit(limit)
    return render_template('default/poslog_list.html', mutations=mutations)
