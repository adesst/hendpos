from flaskext.babel import Babel, gettext
from sqlalchemy import Column, Integer, String, Date, Enum, Float, DateTime, ForeignKey
from database import Base

REGISTERED_USER = 90
STAFF_USER = 80
MANAGER_USER = 10

class DefaultBehaviour():

    def set_fields(self, elm_dict = None, **kwargs):
        if isinstance(elm_dict, dict):
            for key , value in elm_dict.iteritems():
                if not key.startswith("_"):
                    self.__dict__[key] = value
            return True
        if kwargs:
            for key , value in kwargs.iteritems() :
                if not key.startswith("_"):
                    self.__dict__[key] = value
            return True
        else:
            return False

class UserGroup(Base, DefaultBehaviour):

    __tablename__ = 'user_group'
    __table_args__ = {'mysql_engine' : 'InnoDB'}

    id = Column(Integer, primary_key=True )
    group_id = Column(Integer, index=True )
    group_name = Column(String(40) )

    def __init__(self):
        pass

    def __repr__(self):
        return '<UserGroup %r>' %(self.group_name)

class User(Base, DefaultBehaviour):

    __tablename__ = 'user'
    __table_args__ = {'mysql_engine' : 'InnoDB'}

    id = Column(Integer, primary_key=True )
    username = Column(String(40), unique = True, nullable=False)
    name = Column(String(80), )
    email = Column(String(120), )
    password = Column(String(120), )
    card_no = Column(String(120), nullable=False)
    card_uid = Column(String(120), unique=True, nullable=False)
    balance = Column(String(120), nullable=False)
    date_create = Column(DateTime)
    group_id = Column(Integer, ForeignKey('user_group.group_id'), default=90 )

    status = Column(Integer)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' %(self.username)

class UserLog(Base, DefaultBehaviour):

    __tablename__ = 'user_log'
    __table_args__ = {'mysql_engine' : 'InnoDB'}

    id = Column(Integer, primary_key=True )
    user_id = Column(Integer, )
    username = Column(String(40), unique = True,)
    name = Column(String(80), )
    email = Column(String(120), )
    password = Column(String(120), )
    card_no = Column(String(120), nullable=False)
    card_uid = Column(String(120), nullable=False)
    balance = Column(String(120), nullable=False)
    date_create = Column(DateTime)
    group_id = Column(Integer,ForeignKey("user_group.id"))
    status = Column(Integer)

    def __init__(self):
        pass

    def __repr__(self):
        return '<UserLog %r>' %(self.username)

class Balance(Base, DefaultBehaviour):

    __tablename__ = 'balance'
    __table_args__ = {'mysql_engine' : 'InnoDB'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tr_date = Column(DateTime, nullable = False)
    amount = Column(Float, nullable = False)
    balance = Column(Float, nullable = False)
    remain = Column(Float, nullable = False)
    txtype_id = Column(Integer) # 1 - Debit, 11 - Credit,
    status = Column(Integer, default=0) # 0 - Active, 1 - NotActive

    def __init__(self):
        pass

    def __repr__(self):
        return '<Balance %r>' %(self.user_id)

class PosLog(Base):

    __tablename__ = 'pos_log'
    __table_args__ = {'mysql_engine' : 'InnoDB'}

    id = Column(Integer, primary_key=True)
    user_auth_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tr_date = Column(DateTime, nullable = False)
    message = Column(String(512))

    def __init__(self, user_auth_id=None, user_id = None, tr_date = None, message = None ):
        self.user_auth_id = user_auth_id
        self.user_id = user_id
        self.tr_date = tr_date
        self.message = message

