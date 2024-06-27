#!/usr/bin/python3
"""

"""
from models.base import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """
    
    """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """
        
        """
        password = getenv('HBNB_MYSQL_PWD')
        username = getenv('HBNB_MYSQL_USER')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, db_name)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop(self.__engine)
    
    def all(self, cls=None):
        """
        
        """
        list_obj = []
        if cls:
            try:
                if isinstance(cls, str):
                    cls = globals()[cls]
            except KeyError:
                pass
            if issubclass(cls, Base):
                list_obj = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                list_obj.extend(self.__session.query(subclass),all())
            obj_dict = {}
            for obj in list_obj:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
            return obj_dict

    def new(self, obj):
        """ """
        self.__session.add(obj) 

    def save(self):
        """ """
        self.__session.commit()
    
    def delete(self, obj=None):
        """"""
        self.__session.delete(obj)

    def reload(self):
        """ """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = session()
