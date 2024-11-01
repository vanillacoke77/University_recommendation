import psycopg

# Define your connection string
connection_string = "postgresql://neondb_owner:tK4ijw9YHaxc@ep-shy-frost-a5o6ki2u.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Establish the connection
with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        # Execute a test query to check the connection
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Connected to PostgreSQL, version: {db_version}")
