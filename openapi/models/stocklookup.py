
from .dbconnect import connection,db_session,init_db, Base
from sqlalchemy import Column, Integer, String, DateTime


class LookUp(Base):
    __tablename__ = "tb_reference"
    id = Column(String(10), primary_key=True)
    version = Column(Integer)
    country_code = Column(String(2))
    factor_type = Column(String(20))
    factor1 = Column(String(20))
    factor2 = Column(String(20))
    factor3 = Column(String(20))
    factor4= Column(String(20))
    factor5 = Column(String(20))
    result = Column(String(100))
    def __init__(self,id=None,version=None,country_code=None, factor_type=None, factor1=None, factor2=None, factor3=None, factor4=None, factor5=None, result=None):
        self.id = id
        self.version = version
        self.country_code = country_code
        self.factor_type = factor_type
        self.factor1 = factor1
        self.factor2 = factor2
        self.factor3 = factor3
        self.factor4 = factor4
        self.factor5 = factor5
        self.result = result

    def __repr__(self):
        return "<lookup %s>" % self.id
    def save(self):
        db_session.add(self)
        db_session.commit()
        return self
    def update(self):
        db_session.commit()
        return self
