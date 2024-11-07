import streamlit as st
from auth import user_login, user_signup
from schema import User, UserPreference
from recommendation import get_recommendation  # Assuming you have a function to fetch recommendations

# Function to handle login page
def display_login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            # Create a User object with username and password
            user = User(name=username, password=password, email=None, phoneno=None)
            result = user_login(user)  # Pass the entire User object to user_login
            if result == "Login successful":
                st.success("Logged in successfully")
                st.session_state.page = "preferences"  # Update session to show preferences page
            else:
                st.error(result)
        else:
            st.error("Please fill in both username and password.")
    
    if st.button("Go to Signup Page"):
        st.session_state.page = "signup"  # Navigate to signup page

# Function to handle signup page
def display_signup_page():
    st.title("Signup Page")
    fname=st.text_input("Full Name")
    name = st.text_input("Username")
    email = st.text_input("Email")
    phoneno = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    
    if st.button("Signup"):
        if fname and name and email and phoneno and password:
            new_user = User(fname=fname, name=name, email=email, phoneno=phoneno, password=password)
            result = user_signup(new_user)
            st.success(result)
            st.session_state.page = "login"  # Redirect back to login page after signup
        else:
            st.error("Please fill in all fields.")
    
    if st.button("Go to Login Page"):
        st.session_state.page = "login"  # Navigate to login page

def display_preferences_page():
    st.title("Preferences Page")
    st.write("Welcome to the preferences page!")

    # Inputs for user preferences
    country = st.selectbox("Select Country", ["USA", "India", "Germany", "Canada"])
    fees_input = st.selectbox("Preferred Fees Range", ["<$10,000", "$10,000-$20,000", ">$20,000"])
    stream_pref = st.selectbox("Select Stream", ["Engineering", "Business", "Arts", "Law"])
    rank = st.selectbox("Rank", ["Top 10", "Top 50", "Top 100", "Top 200"])

    # Convert fees to an integer before creating the UserPreference object
    if fees_input == "<$10,000":
        fees = 10000
    elif fees_input == "$10,000-$20,000":
        fees = 15000
    else:
        fees = 20000

    # Create a UserPreference object with integer fees
    user_preference = UserPreference(country=country, fees=fees, stream=stream_pref, rank=rank)

    if st.button("Get Recommendations"):
        recommendations = get_recommendation(user_preference)
        if recommendations:
            for rec in recommendations:
                st.write(f"University Name: {rec.name}")
                st.write(f"Country: {rec.country}")
                st.write(f"Rank: {rec.rank}")
                st.write(f"Stream: {rec.stream}")
                st.write(f"Course: {rec.course}")
                st.write(f"Fees: {rec.fees}")
                st.write("---")
        else:
            st.error("No recommendations found.")

    if st.button("Logout"):
        st.session_state.page = "login"  # Log out and go back to login page

# Handle page navigation using session state
if 'page' not in st.session_state:
    st.session_state.page = "login"  # Default to login page

if st.session_state.page == "login":
    display_login_page()
elif st.session_state.page == "signup":
    display_signup_page()
elif st.session_state.page == "preferences":
    display_preferences_page()
