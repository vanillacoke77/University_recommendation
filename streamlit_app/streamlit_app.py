import streamlit as st
import requests
import json

page = st.sidebar.selectbox("Choose your page", ["Login", "Preferences"])

if page == "Login":
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Logged in as {}".format(username))

elif page == "Preferences":
    st.title("User Preferences")
    name = st.text_input("Name")
    country = st.text_input("Country Preference")
    age = st.number_input("Age", min_value=15, max_value=100, step=1)
    stream_pref = st.text_input("Stream Preference")
    fee_bracket = st.selectbox("Fee Bracket", ["<$10,000", "$10,000-$20,000", ">$20,000"])
    rank = st.text_input("Rank")

    if st.button("Submit"):
        # Prepare the data to send in JSON format
        data = {
            "country": country,
            "fees": fee_bracket,
            "stream": stream_pref,
            "rank": rank
        }
        print(f"Sending data: {data}")
        st.success("Preferences recorded")