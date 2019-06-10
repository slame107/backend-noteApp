from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)


from .meta import Base
import copy

class Notes(Base):
    """The SQLAlchemy declarative model class for a Notes object."""
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)
    title = Column(Text)
    noteContent = Column(Text)
    creationDate = Column(Integer)
    lastModified = Column(Integer)

# turns an SQLAlchemy object into a dict
    def dict(self):
        tmp_dict = copy.deepcopy(self.__dict__)
        del tmp_dict['_sa_instance_state']
        return tmp_dict

    
#creation date
#last modified
#title
#notecontent
Index('my_index', Notes.name, unique=True, mysql_length=255)
