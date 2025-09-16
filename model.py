
from datetime import datetime
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Text, 
    DateTime, 
    ForeignKey,
    Enum as SQLEnum,
    Boolean
)

from sqlalchemy.orm import relationship
import uuid
import enum

from db import Base

# Enums
class PriorityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Modelos de Dados
class Board(Base):
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    kcolumns = relationship("Kcolumn", back_populates="board", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Board(id={self.id}, name='{self.name}')>"

class Kcolumn(Base):
    __tablename__ = "kcolumns"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    position = Column(Integer, default=0)  # Para ordenação das colunas
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    board = relationship("Board", back_populates="kcolumns")
    cards = relationship("Card", back_populates="kcolumn", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Kcolumn(id={self.id}, title='{self.title}', board_id={self.board_id})>"

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee = Column(String(255), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(SQLEnum(PriorityLevel), default=PriorityLevel.MEDIUM)
    position = Column(Integer, default=0)  # Para ordenação dos cards
    kcolumn_id = Column(Integer, ForeignKey("kcolumns.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    kcolumn = relationship("Kcolumn", back_populates="cards")
    
    def __repr__(self):
        return f"<Card(id={self.id}, title='{self.title}', kcolumn_id={self.kcolumn_id})>"
