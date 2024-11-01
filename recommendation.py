import os
import re
from typing import List
import psycopg2
from schema import Recommendation, UserPreference
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define your connection string
connection_string = os.environ.get("DATABASE_URL")

# Establish the connection

def get_recommendation(user_preference:UserPreference):
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                embedding = get_embedding(user_preference)
                query = """
            WITH user_embedding AS (
                SELECT %s::vector AS embedding
            )
            SELECT 
                u.name AS name,
                u.country AS country,
                u.rank AS rank,
                d.name AS stream,
                c.name AS course,
                c.fees AS fees,
                1 - (p.embedding <=> ue.embedding) AS similarity  -- Cosine similarity (higher is better)
            FROM 
                preference p
            JOIN 
                university u ON p.Uid = u.id
            JOIN 
                department d ON p.Did = d.id
            JOIN 
                course c ON p.Cid = c.id,
                user_embedding ue
            ORDER BY 
                similarity DESC
            LIMIT 10;
            """

                cur.execute(query, (embedding,))
                
                # Fetch and print the results
                results = cur.fetchall()
                recommendations = [Recommendation(name=row[0], country=row[1], rank=row[2], stream=row[3], course=row[4], fees=row[5]) for row in results]
                return recommendations
    except Exception as e:
        return f"Error Getting Recommendation: {e}"


def get_embedding(user_preference:UserPreference):
    embd = client.embeddings.create(
    model="text-embedding-3-small",
    input=f"{user_preference.country} {user_preference.fees} {user_preference.stream} {user_preference.rank}",
    dimensions=128,
    encoding_format="float"
    )
    return embd.data[0].embedding

