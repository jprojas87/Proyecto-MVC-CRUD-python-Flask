from typing import Optional
from app.database import db
from app.models.user import UserCreate, UserUpdate

class UserController:
    
    @staticmethod
    def create_user(user: UserCreate) -> dict:
        """Crea un nuevo usuario"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (email, full_name, phone, bio, location)
                    VALUES (%(email)s, %(full_name)s, %(phone)s, %(bio)s, %(location)s)
                    RETURNING id, email, full_name, phone, bio, location, 
                              is_active, created_at, updated_at
                    """,
                    user.model_dump()
                )
                result = cur.fetchone()
                conn.commit()
                return result
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        """Obtiene el perfil de un usuario por su ID"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, email, full_name, phone, bio, location, 
                           is_active, created_at, updated_at 
                    FROM users 
                    WHERE id = %s AND is_active = TRUE
                    """,
                    (user_id,)
                )
                return cur.fetchone()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        """Obtiene un usuario por su email"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, email, full_name, phone, bio, location, 
                           is_active, created_at, updated_at 
                    FROM users 
                    WHERE email = %s AND is_active = TRUE
                    """,
                    (email,)
                )
                return cur.fetchone()
    
    @staticmethod
    def update_user_profile(user_id: int, user: UserUpdate) -> Optional[dict]:
        """Actualiza la información personal del usuario"""
        # Construir query dinámicamente solo con campos proporcionados
        update_data = user.model_dump(exclude_unset=True)
        
        if not update_data:
            return UserController.get_user_by_id(user_id)
        
        set_clauses = ", ".join([f"{key} = %({key})s" for key in update_data.keys()])
        
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE users 
                    SET {set_clauses}
                    WHERE id = %(id)s AND is_active = TRUE
                    RETURNING id, email, full_name, phone, bio, location, 
                              is_active, created_at, updated_at
                    """,
                    {**update_data, "id": user_id}
                )
                result = cur.fetchone()
                conn.commit()
                return result
    
    @staticmethod
    def delete_user_account(user_id: int) -> Optional[dict]:
        """Elimina la cuenta del usuario de forma permanente"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                # Primero obtener información del usuario antes de eliminar
                cur.execute(
                    "SELECT id, email FROM users WHERE id = %s AND is_active = TRUE",
                    (user_id,)
                )
                user = cur.fetchone()
                
                if not user:
                    return None
                
                # Eliminar el usuario de forma permanente
                cur.execute(
                    "DELETE FROM users WHERE id = %s RETURNING id, email",
                    (user_id,)
                )
                deleted_user = cur.fetchone()
                conn.commit()
                
                return deleted_user
    
    @staticmethod
    def deactivate_user_account(user_id: int) -> Optional[dict]:
        """Desactiva la cuenta del usuario (soft delete - alternativa)"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users 
                    SET is_active = FALSE
                    WHERE id = %s AND is_active = TRUE
                    RETURNING id, email, is_active
                    """,
                    (user_id,)
                )
                result = cur.fetchone()
                conn.commit()
                return result
    
    @staticmethod
    def get_all_users() -> list[dict]:
        """Obtiene todos los usuarios activos"""
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, email, full_name, phone, bio, location, 
                           is_active, created_at, updated_at 
                    FROM users 
                    WHERE is_active = TRUE
                    ORDER BY created_at DESC
                    """
                )
                return cur.fetchall()