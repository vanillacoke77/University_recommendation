import os
import psycopg2
from validation import validate_user_input
from schema import User
from recommendation import connection_string

def user_login(user: User) -> str:
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM users_view WHERE name = %s AND password = %s"
                cur.execute(query, (user.name, user.password))
                result = cur.fetchone()
                print(result)
                if result[4]==True:
                    user.is_admin = result[4] 
                    return "Login successful as admin"
                else:
                    return "Login successful as user"
    except Exception as e:
        return f"Error during login: User Doesn't exist {e}"

def user_signup(user: User) -> str:
    if not validate_user_input(user.email, user.phoneno, user.password):
        return "Invalid user input: Check email, phone number, or password format."
    
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
                if cur.fetchone():
                    return "User already exists."
                
                query = """
                    INSERT INTO users (name, email, phoneno, is_admin,password)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cur.execute(query, (user.name, user.email, user.phoneno, user.is_admin,user.password))
                conn.commit()
                return "User created successfully."
    except Exception as e:
        return f"Error during sign-up: {e}"


