from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Conversation Model
class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    messages = relationship("Message", back_populates="conversation")

# Message Model
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    role = Column(String(50), nullable=False)  # 'user' or 'bot'
    content = Column(Text, nullable=False)
    conversation = relationship("Conversation", back_populates="messages")

# Embedding Model
class Embedding(Base):
    __tablename__ = 'embeddings'
    id = Column(Integer, primary_key=True)
    document = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)  # Store as JSON string
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship("Conversation")
