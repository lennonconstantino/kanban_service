from sqlalchemy.ext.declarative import declarative_base

# Configuração de Base
Base = declarative_base()

# Classe de Configuração do Banco
class DatabaseConfig:
    def __init__(self, database_url: str, database_type="sqlite", **kwargs):
        self.database_type = database_type.lower()
        
        if self.database_type == "sqlite":
            db_path = kwargs.get("db_path", "kanban.db")
            self.connection_string = f"sqlite:///{db_path}"          
        elif self.database_type == "postgresql":
            host = kwargs.get("host", "localhost")
            port = kwargs.get("port", 5432)
            database = kwargs.get("database", "kanban")
            username = kwargs.get("username", "postgres")
            password = kwargs.get("password", "")
            self.connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError("Tipo de banco não suportado. Use 'sqlite' ou 'postgresql'")
