import os
from dotenv import load_dotenv
import psycopg2
from validation import validate_user_input
from schema import User

# Load environment variables
load_dotenv()

# Connection string from environment variables
connection_string = os.environ.get("DATABASE_URL")

# Function to handle user login (returns True/False)
# In auth.py
def user_login(user: User) -> str:
    try:
        # Assuming you check the credentials in the database
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM users WHERE name = %s AND password = %s"
                cur.execute(query, (user.name, user.password))
                result = cur.fetchone()
                if result:
                    return "Login successful"
                else:
                    return "Invalid credentials"
    except Exception as e:
        return f"Error during login: {e}"


# Function to handle user sign-up
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
                    INSERT INTO users (name, email, phoneno, password)
                    VALUES (%s, %s, %s, %s);
                """
                cur.execute(query, (user.name, user.email, user.phoneno, user.password))
                conn.commit()
                return "User created successfully."
    except Exception as e:
        print(f"Error during sign-up: {e}")
        return f"Error during sign-up: {e}"

# Function to check if a user is an admin
def is_admin(email: str) -> bool:
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT is_admin FROM users WHERE email = %s", (email,))
                result = cur.fetchone()
                return bool(result and result[0])
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False
