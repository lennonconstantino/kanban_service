# Classe Principal do Sistema Kanban
from datetime import datetime
from typing import List, Optional
from repository import KanbanRepository
from model import Board, Card, Kcolumn, PriorityLevel

class KanbanService:
    def __init__(self, repository: KanbanRepository):
        self.repository = repository
            
    def create_board(self, name: str, description: str = None) -> Board:
        return self.repository.create_board(name=name, description=description)
    
    def get_board(self, board_id: int) -> Optional[Board]:
        return self.repository.get_board(board_id=board_id)
    
    def get_all_boards(self) -> List[Board]:
        return self.repository.get_all_boards()
    
    def update_board(self, board_id: int, name: str = None, description: str = None) -> Optional[Board]:
        return self.repository.update_board(board_id=board_id, name=name, description=description)
    
    def delete_board(self, board_id: int) -> bool:
        return self.repository.delete_board(board_id=board_id)
    
    # CRUD Operations para Kcolumn
    def create_column(self, board_id: int, title: str, position: int = None) -> Optional[Kcolumn]:
        return self.repository.create_column(board_id=board_id, title=title, position=position)
    
    def update_column(self, column_id: int, title: str = None, position: int = None) -> Optional[Kcolumn]:
        return self.repository.update_column(column_id=column_id, title=title, position=position)
    
    def delete_column(self, column_id: int) -> bool:
        return self.repository.delete_column(column_id=column_id)
    
    # CRUD Operations para Card
    def create_card(self, kcolumn_id: int, title: str, description: str = None, 
                    assignee: str = None, due_date: datetime = None, 
                    priority: PriorityLevel = PriorityLevel.MEDIUM) -> Optional[Card]:
        return self.repository.create_card(kcolumn_id=kcolumn_id, title=title, description=description, 
                    assignee=assignee, due_date=due_date, 
                    priority=priority)
    
    def update_card(self, card_id: int, **kwargs) -> Optional[Card]:
        return self.repository.update_card(card_id=card_id, kwargs=kwargs)
    
    def move_card(self, card_id: int, target_kcolumn_id: int, position: int = None) -> Optional[Card]:
        return self.repository.move_card(card_id=card_id, target_kcolumn_id=target_kcolumn_id, position=position)
    
    def delete_card(self, card_id: int) -> bool:
        return self.repository.delete_card(card_id=card_id)
    
    def get_board_with_data(self, board_id: int) -> Optional[dict]:
        return self.repository.get_board_with_data(board_id=board_id)
