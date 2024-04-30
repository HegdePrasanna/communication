from sqlalchemy import (create_engine, Column, Integer, String, DateTime, ForeignKey, 
                        TEXT, text, func,TIMESTAMP,BOOLEAN)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50),index=True,nullable=False)
    email = Column(String(50),nullable=False)

class Group(Base):
    __tablename__ = "comm_group"
    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100),index=True,nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))


class UserGroups(Base):
    __tablename__ = "comm_user_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))


class Messages(Base):
    __tablename__ = "comm_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_grp_id = Column(Integer)
    user_id = Column(Integer)
    group_id = Column(Integer)
    message = Column(TEXT,nullable=False)
    is_reply = Column(BOOLEAN,default=True)
    to_message = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=text('UTC_TIMESTAMP()'),default=text('UTC_TIMESTAMP()'))
    created_by = Column(Integer)
    updated_by = Column(Integer)
    is_active = Column(BOOLEAN,default=True)
