# Classe Principal do Sistema Kanban
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db import Base, DatabaseConfig
from model import Board, Card, Kcolumn, PriorityLevel

class KanbanService:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = create_engine(
            config.connection_string,
            echo=False,  # Mude para True para ver as queries SQL
            pool_pre_ping=True if config.database_type == "postgresql" else False
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Cria todas as tabelas no banco de dados"""
        Base.metadata.create_all(bind=self.engine)
        print(f"Tabelas criadas no banco {self.config.database_type}")
        
    def get_session(self) -> Session:
        """Retorna uma sessão do banco de dados"""
        return self.SessionLocal()
    
    def drop_tables(self):
        """Remove todas as tabelas (USE COM CUIDADO!)"""
        Base.metadata.drop_all(bind=self.engine)
        print("Todas as tabelas foram removidas")
    
    # CRUD Operations para Board
    def create_board(self, name: str, description: str = None) -> Board:
        """Cria um novo quadro com colunas padrão"""
        with self.get_session() as session:
            board = Board(name=name, description=description)
            session.add(board)
            session.flush()  # Para obter o ID
            
            # Criar colunas padrão
            default_columns = [
                Kcolumn(title="A Fazer", position=0, board_id=board.id),
                Kcolumn(title="Em Progresso", position=1, board_id=board.id),
                Kcolumn(title="Concluído", position=2, board_id=board.id)
            ]
            
            for col in default_columns:
                session.add(col)
            
            session.commit()
            
            # Fazer um refresh para carregar os relacionamentos
            session.refresh(board)
            # Acessar explicitamente as colunas para carregá-las na sessão
            _ = board.kcolumns
            
            # Fazer expunge/merge para garantir que o objeto possa ser usado fora da sessão
            session.expunge(board)
            
            # Reattach o objeto em uma nova sessão para retornar com os dados carregados
            with self.get_session() as new_session:
                board_with_columns = new_session.merge(board)
                # Carregar explicitamente as colunas
                board_with_columns.kcolumns
                new_session.expunge(board_with_columns)
                return board_with_columns
    
    def get_board(self, board_id: int) -> Optional[Board]:
        """Busca um quadro por ID"""
        with self.get_session() as session:
            return session.query(Board).filter(Board.id == board_id, Board.is_active == True).first()
    
    def get_all_boards(self) -> List[Board]:
        """Lista todos os quadros ativos"""
        with self.get_session() as session:
            return session.query(Board).filter(Board.is_active == True).all()
    
    def update_board(self, board_id: int, name: str = None, description: str = None) -> Optional[Board]:
        """Atualiza um quadro"""
        with self.get_session() as session:
            board = session.query(Board).filter(Board.id == board_id).first()
            if board:
                if name:
                    board.name = name
                if description is not None:
                    board.description = description
                board.updated_at = datetime.now()
                session.commit()
                session.refresh(board)
            return board
    
    def delete_board(self, board_id: int) -> bool:
        """Soft delete de um quadro"""
        with self.get_session() as session:
            board = session.query(Board).filter(Board.id == board_id).first()
            if board:
                board.is_active = False
                board.updated_at = datetime.now()
                session.commit()
                return True
            return False
    
    # CRUD Operations para Kcolumn
    def create_column(self, board_id: int, title: str, position: int = None) -> Optional[Kcolumn]:
        """Cria uma nova coluna"""
        with self.get_session() as session:
            # Verificar se o board existe
            board = session.query(Board).filter(Board.id == board_id).first()
            if not board:
                return None
            
            if position is None:
                # Obter a próxima posição
                max_position = session.query(Kcolumn).filter(Kcolumn.board_id == board_id).count()
                position = max_position
            
            column = Kcolumn(title=title, position=position, board_id=board_id)
            session.add(column)
            session.commit()
            session.refresh(column)
            return column
    
    def update_column(self, column_id: int, title: str = None, position: int = None) -> Optional[Kcolumn]:
        """Atualiza uma coluna"""
        with self.get_session() as session:
            column = session.query(Kcolumn).filter(Kcolumn.id == column_id).first()
            if column:
                if title:
                    column.title = title
                if position is not None:
                    column.position = position
                column.updated_at = datetime.now()
                session.commit()
                session.refresh(column)
            return column
    
    def delete_column(self, column_id: int) -> bool:
        """Deleta uma coluna (apenas se não for a última do quadro)"""
        with self.get_session() as session:
            column = session.query(Kcolumn).filter(Kcolumn.id == column_id).first()
            if not column:
                return False
            
            # Verificar se não é a última coluna do quadro
            columns_count = session.query(Kcolumn).filter(Kcolumn.board_id == column.board_id).count()
            if columns_count <= 1:
                return False
            
            session.delete(column)
            session.commit()
            return True
    
    # CRUD Operations para Card
    def create_card(self, kcolumn_id: int, title: str, description: str = None, 
                   assignee: str = None, due_date: datetime = None, 
                   priority: PriorityLevel = PriorityLevel.MEDIUM) -> Optional[Card]:
        """Cria um novo card"""
        with self.get_session() as session:
            # Verificar se a coluna existe
            column = session.query(Kcolumn).filter(Kcolumn.id == kcolumn_id).first()
            if not column:
                return None
            
            # Obter a próxima posição
            max_position = session.query(Card).filter(Card.kcolumn_id == kcolumn_id).count()
            
            card = Card(
                title=title,
                description=description,
                assignee=assignee,
                due_date=due_date,
                priority=priority,
                position=max_position,
                kcolumn_id=kcolumn_id
            )
            session.add(card)
            session.commit()
            session.refresh(card)
            return card
    
    def update_card(self, card_id: int, **kwargs) -> Optional[Card]:
        """Atualiza um card"""
        with self.get_session() as session:
            card = session.query(Card).filter(Card.id == card_id).first()
            if card:
                for key, value in kwargs.items():
                    if hasattr(card, key) and value is not None:
                        setattr(card, key, value)
                card.updated_at = datetime.now()
                session.commit()
                session.refresh(card)
            return card
    
    def move_card(self, card_id: int, target_kcolumn_id: int, position: int = None) -> Optional[Card]:
        """Move um card para outra coluna"""
        with self.get_session() as session:
            card = session.query(Card).filter(Card.id == card_id).first()
            target_column = session.query(Kcolumn).filter(Kcolumn.id == target_kcolumn_id).first()
            
            if not card or not target_column:
                return None
            
            if position is None:
                # Colocar no final da coluna de destino
                position = session.query(Card).filter(Card.kcolumn_id == target_kcolumn_id).count()
            
            card.column_id = target_kcolumn_id
            card.position = position
            card.updated_at = datetime.now()
            session.commit()
            session.refresh(card)
            return card
    
    def delete_card(self, card_id: int) -> bool:
        """Deleta um card"""
        with self.get_session() as session:
            card = session.query(Card).filter(Card.id == card_id).first()
            if card:
                session.delete(card)
                session.commit()
                return True
            return False
    
    def get_board_with_data(self, board_id: int) -> Optional[dict]:
        """Retorna um quadro completo com colunas e cards"""
        with self.get_session() as session:
            board = session.query(Board).filter(
                Board.id == board_id, 
                Board.is_active == True
            ).first()
            
            if not board:
                return None
            
            # Buscar colunas ordenadas por posição
            kcolumns = session.query(Kcolumn).filter(
                Kcolumn.board_id == board_id
            ).order_by(Kcolumn.position).all()
            
            board_data = {
                "id": board.id,
                "uuid": board.uuid,
                "name": board.name,
                "description": board.description,
                "created_at": board.created_at,
                "columns": []
            }
            
            for kcolumn in kcolumns:
                # Buscar cards da coluna ordenados por posição
                cards = session.query(Card).filter(
                    Card.kcolumn_id == kcolumn.id
                ).order_by(Card.position).all()
                
                kcolumn_data = {
                    "id": kcolumn.id,
                    "uuid": kcolumn.uuid,
                    "title": kcolumn.title,
                    "position": kcolumn.position,
                    "cards": []
                }
                
                for card in cards:
                    card_data = {
                        "id": card.id,
                        "uuid": card.uuid,
                        "title": card.title,
                        "description": card.description,
                        "assignee": card.assignee,
                        "due_date": card.due_date,
                        "priority": card.priority.value,
                        "position": card.position,
                        "created_at": card.created_at
                    }
                    kcolumn_data["cards"].append(card_data)
                
                board_data["columns"].append(kcolumn_data)
            
            return board_data
