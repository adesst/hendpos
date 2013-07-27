from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///hendpos.db', convert_unicode=True)
engine = create_engine('mysql+mysqldb://root@localhost/hendpos', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    group_query = db_session.query(models.UserGroup)
    group = group_query.count()
    if group == 0:
        groups = [{'group_id' : 10, 'group_name' : 'Manager'},
            {'group_id' : 80, 'group_name' : 'Staff'},
            {'group_id' : 90, 'group_name' : 'Registered'},
        ]
        db_session.execute(UserGroup.__table__.insert(), groups)

