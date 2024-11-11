import streamlit as st
from auth import user_login, user_signup
from schema import User, UserPreference
from recommendation import get_recommendation
import requests
import json
import psycopg2
from auth import connection_string

def display_login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    
    if st.button("Login"):
        if username and password:
            user = User(name=username, password=password, email=None, phoneno=None)
            result = user_login(user)
            if result == "Login successful as admin":
                st.success("Logged in as Administrator")
                st.session_state.page = "admin"
            elif result == "Login successful as user":
                st.success("Logged in successfully")
                st.session_state.page = "preferences"
            else:
                st.error(result)
        else:
            st.error("Please fill in both username and password.")
    
    if st.button("Go to Signup Page"):
        st.session_state.page = "signup"

def display_signup_page():
    st.title("Signup Page")
    fname = st.text_input("Full Name")
    name = st.text_input("Username")
    email = st.text_input("Email")
    phoneno = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    admin_check = st.checkbox("Register as Admin")

    if st.button("Signup"):
        if fname and name and email and phoneno and password:
            new_user = User(fname=fname, name=name, email=email, phoneno=phoneno, password=password, is_admin=admin_check)
            result = user_signup(new_user)
            st.success(result)
            st.session_state.page = "login"
        else:
            st.error("Please fill in all fields.")

    if st.button("Go to Login Page"):
        st.session_state.page = "login"

def display_preferences_page():
    st.title("Preferences Page")
    st.write("Welcome to the preferences page!")
    st.title("User Preferences")
    country = st.selectbox("Country Preference", ["USA", "Canada", "UK", "Australia", "Germany"])
    
    stream_pref = st.selectbox("Stream Preference", ["Engineering", "Business", "Arts", "Science", "Law"])

    fees = st.selectbox("Fee Bracket", ["<$10,000", "$10,000-$20,000", ">$20,000"])

    rank = st.selectbox("Rank", ["Top 10", "Top 50", "Top 100", "Top 200"])


    if st.button("Submit"):
        # Prepare the data to send in JSON format
        if fees == "<$10,000":
            fee_bracket = 10000
        elif fees == "$10,000-$20,000":
            fee_bracket = 15000
        else:
            fee_bracket = 20000
        data = {
            "country": country,
            "fees": fee_bracket,
            "stream": stream_pref,
            "rank": rank
        }
        print(f"Sending data: {data}")
        st.success("Preferences recorded")
        req = requests.post("http://localhost:8080/recommendation",data=json.dumps(data))
        recommendations = req.json()
        print(recommendations)
        tabs = st.tabs([f"Recommendation {i + 1}" for i in range(len(recommendations['recommendation']))])
        
        for i, tab in enumerate(tabs):
            with tab:
                rec = recommendations['recommendation'][i]
                st.subheader("Recommendation Details")
                st.write(f"**University**: {rec.get('name', 'N/A')}")
                st.write(f"**Country**: {rec.get('country', 'N/A')}")
                st.write(f"**Fees**: {rec.get('fees', 'N/A')}")
                st.write(f"**Stream**: {rec.get('stream', 'N/A')}")
                st.write(f"**Rank**: {rec.get('rank', 'N/A')}")

def display_admin_page():
    st.title("Admin Page")
    st.write("Welcome, Admin!")

    # Add admin-specific functionalities, e.g., user management, viewing logs, etc.
    if st.button("View All Users"):
        try:
            with psycopg2.connect(connection_string) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT name, email, is_admin FROM users")
                    users = cur.fetchall()
                    for user in users:
                        st.write(f"Name: {user[0]}, Email: {user[1]}, Admin: {user[2]}")
        except Exception as e:
            st.error(f"Error fetching users: {e}")

    if st.button("Logout"):
        st.session_state.page = "login"

if 'page' not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    display_login_page()
elif st.session_state.page == "signup":
    display_signup_page()
elif st.session_state.page == "preferences":
    display_preferences_page()
elif st.session_state.page == "admin":
    display_admin_page()
