# Função de exemplo de uso
from datetime import datetime
from db import DatabaseConfig
from model import PriorityLevel
from service import KanbanService


def exemplo_uso():
    """Exemplo de como usar o sistema"""
    
    # Configuração para SQLite
    sqlite_config = DatabaseConfig("sqlite", db_path="kanban_example.db")
    
    # Configuração para PostgreSQL (descomente e ajuste conforme necessário)
    # postgres_config = DatabaseConfig(
    #     "postgresql",
    #     host="localhost",
    #     port=5432,
    #     database="kanban",
    #     username="seu_usuario",
    #     password="sua_senha"
    # )
    
    # Inicializar sistema com SQLite
    kanban = KanbanService(sqlite_config)
    
    # Criar tabelas
    kanban.create_tables()
    
    # Criar um quadro
    board = kanban.create_board("Projeto de Exemplo", "Descrição do projeto")
    print(f"Quadro criado: {board}")
    
    # Adicionar uma coluna personalizada
    custom_column = kanban.create_column(board.id, "Revisão", position=2)
    print(f"Coluna criada: {custom_column}")
    
    # Buscar os dados completos do quadro para obter as colunas
    board_data = kanban.get_board_with_data(board.id)
    
    # Criar alguns cards usando os IDs das colunas do board_data
    card1 = kanban.create_card(
        board_data['columns'][0]['id'],  # Primeira coluna "A Fazer"
        "Implementar login",
        "Criar sistema de autenticação",
        "João Silva",
        datetime(2024, 12, 31),
        PriorityLevel.HIGH
    )
    
    card2 = kanban.create_card(
        board_data['columns'][0]['id'],  # Primeira coluna "A Fazer"
        "Design da interface",
        "Criar mockups das telas",
        "Maria Santos",
        priority=PriorityLevel.MEDIUM
    )
    
    print(f"Cards criados: {card1}, {card2}")
    
    # Mover card para outra coluna
    kanban.move_card(card1.id, board_data['columns'][1]['id'])  # Mover para "Em Progresso"
    
    # Buscar dados completos do quadro novamente para mostrar o resultado final
    board_data_final = kanban.get_board_with_data(board.id)
    print("\nDados completos do quadro:")
    print(f"Nome: {board_data_final['name']}")
    for column in board_data_final['columns']:
        print(f"  Coluna: {column['title']} ({len(column['cards'])} cards)")
        for card in column['cards']:
            print(f"    - {card['title']} (Prioridade: {card['priority']})")
    
    return kanban

if __name__ == "__main__":
    # Executar exemplo
    sistema = exemplo_uso()
    print("\nSistema Kanban inicializado com sucesso!")
    print("Para usar com PostgreSQL, descomente e configure as credenciais na função exemplo_uso()")