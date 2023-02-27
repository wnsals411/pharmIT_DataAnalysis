from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship

from app.database.conn import Base, db

class BaseMixin:
    # id = Column(Integer, primary_key=True, index=True)
    # created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def getfirst(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """

        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        print(kwargs.items())
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        # print(query.count())
        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        print(result)
        if not session:
            sess.close()
        return result

    @classmethod
    def getallsort(cls, session: Session = None):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """

        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        # print(kwargs.items())
        
        # for key, val in kwargs.items():
        #     col = getattr(cls, key)
        #     query = query.filter(col == val)

        # print(query.count())
        result = query.all()
        print(result)
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1: cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        get_id = self.id
        ret = None

        self._session.flush()
        if qs > 0 :
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        print(self.served)
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


class User(Base, BaseMixin):
    __tablename__ = "pharm_AnalEmp"
    UserId = Column(String(length=200), nullable=False, primary_key=True)
    EmpName = Column(String(length=200), nullable=False)
    LoginPwd = Column(String(length=400), nullable=False)
    DeptSeq = Column(Integer, nullable=True)
    DeptName = Column(String(length=200), nullable=True)    
    UMPgName = Column(String(length=400), nullable=True)
    # keys = relationship("ApiKeys", back_populates="user")

class AnalMenu(Base, BaseMixin):
    __tablename__ = "pharm_AnalMenu"
    MenuId = Column(Integer, nullable=False, primary_key=True)
    MenuParent = Column(Integer, nullable=False)    
    MenuName = Column(String(length=300), nullable=False)
    MenuUrl = Column(String(length=300), nullable=False)
    Sort = Column(Integer, nullable=True)
    UseYN = Column(String(length=1), nullable=False)
    LastDateTime = Column(DateTime, nullable=False, default=func.utc_timestamp())

class ApiKeys(Base, BaseMixin):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())    
    access_key = Column(String(length=64), nullable=False, index=True)
    secret_key = Column(String(length=64), nullable=False)
    user_memo = Column(String(length=40), nullable=True)
    status = Column(Enum("active", "stopped", "deleted"), default="active")
    is_whitelisted = Column(Boolean, default=False)
    UserId = Column(Integer, ForeignKey("user.UserId"), nullable=False)
    # whitelist = relationship("ApiWhiteLists", backref="api_keys")
    # user = relationship("User", back_populates="keys")

class ApiWhiteLists(Base, BaseMixin):
    __tablename__ = "api_whitelists"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())        
    ip_addr = Column(String(length=64), nullable=False)
    # api_key_id = Column(Integer, ForeignKey("api_keys.UserId"), nullable=False)


# class Users(Base, BaseMixin):
#     __tablename__ = "users"
#     status = Column(Enum("active", "deleted", "blocked"), default="active")
#     email = Column(String(length=255), nullable=True)
#     pw = Column(String(length=2000), nullable=True)
#     name = Column(String(length=255), nullable=True)
#     phone_number = Column(String(length=20), nullable=True, unique=True)
#     profile_img = Column(String(length=1000), nullable=True)
#     sns_type = Column(Enum("FB", "G", "K"), nullable=True)
#     marketing_agree = Column(Boolean, nullable=True, default=True)
#     keys = relationship("ApiKeys", back_populates="users")


# class ApiKeys(Base, BaseMixin):
#     __tablename__ = "api_keys"
#     access_key = Column(String(length=64), nullable=False, index=True)
#     secret_key = Column(String(length=64), nullable=False)
#     user_memo = Column(String(length=40), nullable=True)
#     status = Column(Enum("active", "stopped", "deleted"), default="active")
#     is_whitelisted = Column(Boolean, default=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     whitelist = relationship("ApiWhiteLists", backref="api_keys")
#     users = relationship("Users", back_populates="keys")


# class ApiWhiteLists(Base, BaseMixin):
#     __tablename__ = "api_whitelists"
#     ip_addr = Column(String(length=64), nullable=False)
#     api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=False)