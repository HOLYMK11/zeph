from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from config import SQLITE_PATH
import datetime, os
engine = create_engine(f"sqlite:///{SQLITE_PATH}", connect_args={'check_same_thread': False}, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    credits = Column(Integer, default=0)
    premium_until = Column(DateTime, nullable=True)
    daily_ai = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    meta = Column(JSON, default={})
class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, index=True)
    credits = Column(Integer)
    uses = Column(Integer, default=1)
Base.metadata.create_all(bind=engine)
class Storage:
    def __init__(self):
        self.Session = SessionLocal
    def ensure_user(self, tg_id:int, username:str=None):
        db = self.Session()
        try:
            u = db.query(User).filter(User.tg_id==tg_id).one_or_none()
            if not u:
                u = User(tg_id=tg_id, username=username)
                db.add(u); db.commit(); db.refresh(u)
            return u
        finally:
            db.close()
    def add_credits(self, tg_id:int, amount:int):
        db = self.Session()
        try:
            u = db.query(User).filter(User.tg_id==tg_id).one_or_none()
            if not u:
                return False
            u.credits += amount
            db.commit()
            return True
        finally:
            db.close()
    def set_premium(self, tg_id:int, days:int):
        db = self.Session()
        try:
            u = db.query(User).filter(User.tg_id==tg_id).one_or_none()
            if not u:
                return False
            if u.premium_until and u.premium_until > datetime.datetime.utcnow():
                u.premium_until = u.premium_until + datetime.timedelta(days=days)
            else:
                u.premium_until = datetime.datetime.utcnow() + datetime.timedelta(days=days)
            db.commit()
            return True
        finally:
            db.close()
    def redeem_coupon(self, code:str):
        db = self.Session()
        try:
            c = db.query(Coupon).filter(Coupon.code==code).one_or_none()
            if not c:
                return None
            credits = c.credits
            c.uses -= 1
            if c.uses <= 0:
                db.delete(c)
            db.commit()
            return credits
        finally:
            db.close()
