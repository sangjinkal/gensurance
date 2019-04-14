# coding=utf-8
from .dbconnect import connection,db_session,init_db, Base
from sqlalchemy import Column, Integer, String, DateTime


class StockList(Base):
    __tablename__ = "tb_stock_lists"
    id = Column(String(10), primary_key=True)
    trdDd = Column(String(8))
    isuCd = Column(String(12))
    isuSrtCd = Column(String(9))
    isuKorNm = Column(String(80))
    isuKorAbbrv = Column(String(9))
    valid = Column(String(1))
    def __init__(self,id=None,trdDd=None,isuCd=None,isuStrCd=None, isuKorNm =None, isuKorAbbrv= None, valid=None):
        self.id = id
        self.trdDd = trdDd
        self.isuCd = isuCd
        self.isuKorAbbrv = isuKorAbbrv
        self.isuSrtCd = isuStrCd
        self.isuKorNm = isuKorNm
        self.valid = valid
    def __repr__(self):
        return "<stockList %s>" % self.id
    def save(self):
        db_session.add(self)
        db_session.commit()
        return self
    def update(self):
        db_session.commit()
        return self
