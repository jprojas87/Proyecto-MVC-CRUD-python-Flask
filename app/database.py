import psycopg
from psycopg.rows import dict_row
from app.config import settings

class Database:
    def __init__(self):
        self.connection_string = settings.database_url
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return psycopg.connect(
            self.connection_string,
            row_factory=dict_row
        )
    
    def init_db(self):
        """Inicializa la base de datos creando las tablas necesarias"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        full_name VARCHAR(200) NOT NULL,
                        phone VARCHAR(20),
                        bio TEXT,
                        location VARCHAR(100),
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Trigger para actualizar updated_at automáticamente
                cur.execute("""
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                """)
                
                cur.execute("""
                    DROP TRIGGER IF EXISTS update_users_updated_at ON users;
                    CREATE TRIGGER update_users_updated_at
                    BEFORE UPDATE ON users
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
                """)
                
                conn.commit()

db = Database()