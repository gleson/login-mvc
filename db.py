from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base


def conn():
    CONN = 'sqlite:///projeto_login.db'
    return CONN


def return_engine():
    CONN = conn()
    engine = create_engine(CONN, echo=False)
    return engine


def return_session():
    engine = return_engine()
    Session = sessionmaker(bind=engine)
    return Session()


class DbUser:

    @classmethod
    def create(cls, name, email, password, level, status, sign_up_date):
        x = User(name=name, email=email, password=password, level=level, status=status, sign_up_date=sign_up_date)
        session = return_session()
        session.add(x)
        session.commit()
        return True

    @classmethod
    def read(cls):
        session = return_session()
        return session.query(User).all()

    @classmethod
    def read_one(cls, id=None, name=None, email=None, level=None):
        session = return_session()
        try:
            if id:
                return session.query(User).filter_by(id=id).one()
            elif name:
                return session.query(User).filter_by(name=name).one()
            elif email:
                return session.query(User).filter_by(email=email).one()
            elif level:
                return session.query(User).filter_by(level=level)[0]
            else:
                return False
        except:
            return False


    @classmethod
    def update(cls, id, field, value):
        session = return_session()
        x = session.query(User).filter(User.id==id).one()
        if field=='name': x.name = value
        elif field=='email': x.email = value
        elif field=='password': x.password = value
        elif field=='level': x.level = value
        elif field=='status': x.status = value

        if any([x.name, x.email, x.password, x.level, x.status]):
            try:
                session.commit()
                return True
            except:
                return False
        return False

    @classmethod
    def delete(cls, id):
        session = return_session()
        x = session.query(User).filter(User.id==id).delete()
        session.commit()
        return x


Base.metadata.create_all(return_engine())

