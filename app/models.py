from flaskext.babel import Babel, gettext
from sqlalchemy import Column, Integer, String, Date, Enum, Float, DateTime, ForeignKey
from database import Base

class DefaultBehaviour():

    def set_fields(self, elm_dict = None, **kwargs):
        if isinstance(elm_dict, dict):
            for key , value in elm_dict.iteritems():
                self.__dict__[key] = value
            return True
        if kwargs:
            for key , value in kwargs.iteritems():
                self.__dict__[key] = value
            return True
        else:
            return False

class User(Base, DefaultBehaviour):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True )
    username = Column(String(40), unique = True, nullable=False)
    name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    card_no = Column(String(120), nullable=False)
    card_uid = Column(String(120), nullable=False)
    balance = Column(String(120), nullable=False)

    def __init__(self,
            username = None,
            name = None,
            email = None ,
            card_no = None,
            card_uid = None,
            balance = 0):
        self.username = username
        self.name = name
        self.email = email
        self.card_no = card_no
        self.card_uid = card_uid
        self.balance = balance

    def __repr__(self):
        return '<User %r>' %(self.username)

class Card(Base, DefaultBehaviour):

    __tablename__ = 'card'

    id = Column(Integer, primary_key=True )
    tr_date = Column( DateTime, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False )
    card_no = Column(String(120), nullable=False)
    card_uid = Column(String(120), nullable=False)

class Balance(Base, DefaultBehaviour):

    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tr_date = Column(DateTime, nullable = False)
    amount = Column(Float, nullable = False)
    remain = Column(Float, nullable = False)
    txtype_id = Column(Integer) # 1 - Debit, 2 - Credit

    def __init__(self, card_state_id = None, tr_date = None, amount = None, remain = None, type_id = None ):
        self.card_state_id = card_state_id
        self.tr_date = tr_date
        self.amount = amount
        self.remain = remain
        self.type_id = type_id

class PosLog(Base):

    __tablename__ = 'pos_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tr_date = Column(DateTime, nullable = False)
    message = Column(String(512))

    def __init__(self, user_id = None, tr_date = None, message = None ):
        self.user_id = user_id
        self.tr_date = tr_date
        self.message = message
