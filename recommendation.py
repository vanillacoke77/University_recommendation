import os
import psycopg2
from schema import Recommendation, UserPreference
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


connection_string = os.environ.get("DATABASE_URL")


def get_recommendation(user_preference: UserPreference):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                embedding = get_embedding(user_preference)
                query = "SELECT * FROM get_top_matches(%s::vector);"
                cur.execute(query, (embedding,))
                results = cur.fetchall()
                recommendations = [Recommendation(name=row[0], country=row[1], rank=row[2], stream=row[3], course=row[4], fees=row[5]) for row in results]
                return recommendations
    except Exception as e:
        return f"Error getting recommendation: {e}"


def get_embedding(user_preference: UserPreference):
    try:
        embd = client.embeddings.create(
            model="text-embedding-3-small",
            input=f"{user_preference.country} {user_preference.fees} {user_preference.stream} {user_preference.rank}",
            dimensions=128,
            encoding_format="float"
        )
        return embd.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")

def get_entries(entry_type:str):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                if entry_type == "country":
                    cur.execute("SELECT country FROM preference")
                elif entry_type == "stream":
                    cur.execute("SELECT name FROM department")
                elif entry_type == "rank":
                    cur.execute("SELECT rank FROM university")
                results = cur.fetchall()
                return [row[0] for row in results]
    except Exception as e:
        return f"Error getting entries: {e}"
    