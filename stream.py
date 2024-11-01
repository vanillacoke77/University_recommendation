import re
import streamlit as st
import requests
import json
from recommendation import user_login
from schema import User,UserPreference

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login Page")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phoneno = st.text_input("Phone No")
    password = st.text_input("Password", type="password")
    login_obj = User(
        name=username,
        email=email,
        phoneno=phoneno,
        password=password
    )
    if st.button("Login","login"):
        login = user_login(login_obj)
        if  login == "User Created Successfully":
            st.success("Logged in as {}".format(username))
            st.session_state.logged_in = True
            st.session_state.login_button_disabled = True
        else:
            st.success(f"Failed to create User: {login}")
    
    

else:
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