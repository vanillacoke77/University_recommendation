import psycopg2
from recommendation import connection_string
from schema import User

def get_users():
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name, email, is_admin FROM users")
                users = cur.fetchall()
                return users
    except Exception as e:
        return(f"Error fetching users: {e}")
    

def insert_user(user:User):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (name, email, phoneno, password, is_admin) VALUES (%s, %s, %s, %s, %s)",
                    (user.name, user.email, user.phoneno, user.password, user.is_admin)
                )
                conn.commit()
            return "User inserted sucessfully"
    except Exception as e:
        return(f"Error inserting user: {e}")
    

def make_user_admin(username:str):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET is_admin = TRUE WHERE name = %s",
                    (username,)
                )
                conn.commit()
            return "User made admin successfully"
    except Exception as e:
        return(f"Error making user admin: {e}")

def execute_query(query:str):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                user = cur.fetchall()
                conn.commit()
                return user
    except Exception as e:
        return(f"Error executing query: {e}")
    

