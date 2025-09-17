# Sistema Kanban Service

Um sistema completo de gerenciamento de projetos baseado na metodologia Kanban, implementado em Python com SQLAlchemy e suporte a múltiplos bancos de dados.

## 📋 Conceito

O Kanban Service é uma implementação robusta de um sistema de quadro Kanban que permite:

- **Gestão de Projetos**: Criação e organização de quadros de projeto
- **Fluxo de Trabalho**: Colunas personalizáveis para representar diferentes estágios do trabalho
- **Cards de Tarefas**: Criação, edição e movimentação de tarefas entre colunas
- **Priorização**: Sistema de níveis de prioridade (Baixa, Média, Alta)
- **Rastreamento**: Timestamps de criação e atualização para auditoria
- **Flexibilidade**: Suporte a SQLite e PostgreSQL

## 🏗️ Arquitetura

O sistema segue o padrão de arquitetura em camadas:

```
┌─────────────────┐
│   main.py       │ ← Camada de Apresentação (Exemplos de uso)
├─────────────────┤
│   service.py    │ ← Camada de Serviços (Lógica de negócio)
├─────────────────┤
│  repository.py  │ ← Camada de Repositório (Acesso a dados)
├─────────────────┤
│    model.py     │ ← Camada de Modelo (Entidades do domínio)
├─────────────────┤
│     db.py       │ ← Camada de Infraestrutura (Configuração DB)
└─────────────────┘
```

### Componentes Principais

- **Board**: Quadro principal do projeto
- **Kcolumn**: Colunas do quadro (A Fazer, Em Progresso, Concluído)
- **Card**: Tarefas individuais com atributos como prioridade, responsável e prazo
- **PriorityLevel**: Enum para níveis de prioridade (LOW, MEDIUM, HIGH)

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **SQLAlchemy**: ORM para mapeamento objeto-relacional
- **SQLite/PostgreSQL**: Bancos de dados suportados
- **UUID**: Identificadores únicos para entidades
- **Enum**: Tipos de dados estruturados para prioridades

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd kanban_service
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o exemplo:
```bash
python main.py
```

## 🚀 Como Usar

### Configuração Básica

```python
from db import DatabaseConfig
from repository import KanbanRepository
from service import KanbanService

# Configuração para SQLite
config = DatabaseConfig("sqlite", db_path="kanban_example.db")
repository = KanbanRepository(config)
kanban = KanbanService(repository)
```

### Configuração para PostgreSQL

```python
# Configuração para PostgreSQL
postgres_config = DatabaseConfig(
    "postgresql",
    host="localhost",
    port=5432,
    database="kanban",
    username="seu_usuario",
    password="sua_senha"
)
```

### Operações Principais

#### 1. Gerenciamento de Quadros

```python
# Criar um quadro
board = kanban.create_board("Projeto de Exemplo", "Descrição do projeto")

# Listar todos os quadros
boards = kanban.get_all_boards()

# Atualizar um quadro
kanban.update_board(board.id, name="Novo Nome", description="Nova descrição")

# Deletar um quadro (soft delete)
kanban.delete_board(board.id)
```

#### 2. Gerenciamento de Colunas

```python
# Criar uma coluna personalizada
column = kanban.create_column(board.id, "Revisão", position=2)

# Atualizar uma coluna
kanban.update_column(column.id, title="Em Revisão", position=1)

# Deletar uma coluna
kanban.delete_column(column.id)
```

#### 3. Gerenciamento de Cards

```python
from datetime import datetime
from model import PriorityLevel

# Criar um card
card = kanban.create_card(
    column_id=column.id,
    title="Implementar login",
    description="Criar sistema de autenticação",
    assignee="João Silva",
    due_date=datetime(2024, 12, 31),
    priority=PriorityLevel.HIGH
)

# Mover card entre colunas
kanban.move_card(card.id, target_column_id)

# Atualizar um card
kanban.update_card(card.id, title="Novo título", assignee="Maria Santos")

# Deletar um card
kanban.delete_card(card.id)
```

#### 4. Consultas Avançadas

```python
# Obter quadro completo com dados
board_data = kanban.get_board_with_data(board.id)
print(f"Quadro: {board_data['name']}")
for column in board_data['columns']:
    print(f"  {column['title']}: {len(column['cards'])} cards")
    for card in column['cards']:
        print(f"    - {card['title']} ({card['priority']})")
```

## 📊 Estrutura do Banco de Dados

### Tabela `boards`
- `id`: Chave primária
- `uuid`: Identificador único
- `name`: Nome do quadro
- `description`: Descrição do projeto
- `created_at`: Data de criação
- `updated_at`: Data de atualização
- `is_active`: Status ativo (soft delete)

### Tabela `kcolumns`
- `id`: Chave primária
- `uuid`: Identificador único
- `title`: Título da coluna
- `position`: Posição para ordenação
- `board_id`: Chave estrangeira para boards
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Tabela `cards`
- `id`: Chave primária
- `uuid`: Identificador único
- `title`: Título da tarefa
- `description`: Descrição detalhada
- `assignee`: Responsável pela tarefa
- `due_date`: Data de vencimento
- `priority`: Nível de prioridade (enum)
- `position`: Posição para ordenação
- `kcolumn_id`: Chave estrangeira para kcolumns
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## 🔧 Funcionalidades Avançadas

### Colunas Padrão
Todo quadro criado automaticamente recebe três colunas padrão:
- **A Fazer** (position: 0)
- **Em Progresso** (position: 1)
- **Concluído** (position: 2)

### Sistema de Posicionamento
- Colunas e cards possuem sistema de posicionamento para ordenação
- Movimentação de cards preserva a ordem
- Posições são automaticamente calculadas quando não especificadas

### Soft Delete
- Quadros são marcados como inativos em vez de deletados fisicamente
- Preserva histórico e integridade referencial

### Validações de Integridade
- Não é possível deletar a última coluna de um quadro
- Verificação de existência de entidades antes de operações
- Relacionamentos em cascata para manutenção da integridade

## 🧪 Exemplo Completo

Execute o arquivo `main.py` para ver um exemplo completo de uso:

```bash
python main.py
```

Este exemplo demonstra:
1. Criação de um quadro
2. Adição de coluna personalizada
3. Criação de cards com diferentes prioridades
4. Movimentação de cards entre colunas
5. Consulta de dados completos do quadro

## 🔄 Extensibilidade

O sistema foi projetado para ser facilmente extensível:

- **Novos tipos de prioridade**: Adicione valores ao enum `PriorityLevel`
- **Novos atributos**: Estenda os modelos com novos campos
- **Novos bancos**: Implemente novos tipos de banco na classe `DatabaseConfig`
- **APIs REST**: Adicione uma camada de API usando Flask/FastAPI
- **Interface Web**: Crie uma interface web usando frameworks como React/Vue

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou suporte, abra uma issue no repositório.