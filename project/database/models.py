# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, INTEGER, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Project(Base):
    __tablename__ = 'projects'

    id = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    admin_id = Column(String(45), nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    userss = relationship('User', secondary='users_has_projects')


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email_id = Column(String(255), nullable=False, unique=True)
    privilege = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    userscol = Column(String(45))


class Issue(Base):
    __tablename__ = 'issues'

    id = Column(INTEGER(11), primary_key=True)
    subject = Column(String(45), nullable=False)
    description = Column(String(255))
    priority = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    projects_id = Column(ForeignKey('projects.id'), nullable=False, index=True)
    created_by_user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    assigned_to_user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    tested = Column(INTEGER(11), server_default=text("'0'"))

    assigned_to_user = relationship('User', primaryjoin='Issue.assigned_to_user_id == User.id')
    created_by_user = relationship('User', primaryjoin='Issue.created_by_user_id == User.id')
    projects = relationship('Project')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(INTEGER(11), primary_key=True)
    msg = Column(String(255), nullable=False)
    users_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    projects_id = Column(ForeignKey('projects.id'), nullable=False, index=True)

    projects = relationship('Project')
    users = relationship('User')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(String(255))
    priority = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    due_date = Column(DateTime, nullable=False)
    assigned_to_user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    assigned_by_user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    projects_id = Column(ForeignKey('projects.id'), nullable=False, index=True)
    status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    assigned_by_user = relationship('User', primaryjoin='Task.assigned_by_user_id == User.id')
    assigned_to_user = relationship('User', primaryjoin='Task.assigned_to_user_id == User.id')
    projects = relationship('Project')


t_users_has_projects = Table(
    'users_has_projects', metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True, nullable=False, index=True),
    Column('projects_id', ForeignKey('projects.id'), primary_key=True, nullable=False, index=True)
)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(INTEGER(11), primary_key=True)
    comments = Column(String(255))
    users_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    tasks_id = Column(ForeignKey('tasks.id'), nullable=False, index=True)

    tasks = relationship('Task')
    users = relationship('User')
