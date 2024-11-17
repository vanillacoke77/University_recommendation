import streamlit as st
from admin import delete_user, execute_query, get_users, insert_user, make_user_admin, get_universities
from auth import user_login, user_signup
from schema import User, UserPreference
from recommendation import get_entries, get_recommendation
import requests,json
import pandas as pd

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
    st.title("User Preferences")

    st.session_state.submitted = False
    tab1, tab2 = st.tabs(["Preferences", "View all Universities"])

    with tab1:
        if st.session_state.submitted == False:
            country = st.selectbox("Country Preference", ["USA", "China", "Germany"])
            stream_pref = st.selectbox("Stream Preference", ["CSE", "Maths", "Law", "Science"])
            rank = st.selectbox("Rank", ["Top 10", "Top 50", "Top 100"])
        else:
            country = st.selectbox("Country Preference", [st.session_state.country])
            stream_pref = st.selectbox("Stream Preference", [st.session_state.stream_pref])
            rank = st.selectbox("Rank", [st.session_state.rank])

        fees = st.selectbox("Fee Bracket", ["<$10,000", "$10,000-$20,000", ">$20,000"])

        if st.button("Submit"):
            # Prepare the data to send in JSON format
            st.session_state.submitted = True
            if fees == "<$10,000":
                fee_bracket = 5000
            elif fees == "$10,000-$20,000":
                fee_bracket = 15000
            elif fees == ">$20,000":
                fee_bracket = 25000
            data = {
                "country": country,
                "fees": fee_bracket,
                "stream": stream_pref,
                "rank": rank
            }
            print(f"Sending data: {data}")
            st.success("Preferences recorded")
            req = requests.post("http://localhost:8080/recommendation", data=json.dumps(data))
            recommendations = req.json()
            print(recommendations)
            rec_tabs = st.tabs([f"Recommendation {i + 1}" for i in range(len(recommendations['recommendation']))])

            for i, rec_tab in enumerate(rec_tabs):
                with rec_tab:
                    rec = recommendations['recommendation'][i]
                    st.subheader("Recommendation Details")
                    st.write(f"**University**: {rec.get('name', 'N/A')}")
                    st.write(f"**Country**: {rec.get('country', 'N/A')}")
                    st.write(f"**Fees**: {rec.get('fees', 'N/A')}")
                    st.write(f"**Stream**: {rec.get('stream', 'N/A')}")
                    st.write(f"**Course**: {rec.get('course', 'N/A')}")
                    st.write(f"**Rank**: {rec.get('rank', 'N/A')}")

    with tab2:
        if st.button("View All Universities"):
            universities = get_universities()
            print(universities)
            df = pd.DataFrame(universities, columns=["Name","Country"])
            st.table(df)

        




def display_admin_page():
    st.title("Admin Page")
    st.write("Welcome, Admin!")


    # Define the tabs
    tabs = ["View All Users", "Make User Admin", "Delete User", "Add New User", "Logout"]
    selected_tab = st.tabs(tabs)

    # View All Users tab
    with selected_tab[0]:
        if st.button("View All Users",key="View Users"):
            try:
                users = get_users()
                df_users = pd.DataFrame(users, columns=["Name", "Email", "Admin"])
                st.table(df_users)
            except Exception as e:
                st.error(f"Error fetching users: {e}")

    # Make User Admin tab
    with selected_tab[1]:
        st.write("### Make User Admin")
        username = st.text_input("Enter Username to Make Admin")
        if st.button("Make User Admin",key="User Admin"):
            if username:
                try: 
                    result = make_user_admin(username)
                    st.success(result)
                    user = execute_query(f"SELECT * FROM users WHERE name = '{username}'")
                    print(user)
                    user_df = pd.DataFrame(user, columns=["UserId", "Name", "Email","PhoneNo", "Admin", "Password"])
                    st.table(user_df)
                except Exception as e:
                    st.error(f"Error {e}")

    # Delete User tab
    with selected_tab[2]:
        st.write("### Delete User")
        username = st.text_input("Enter Username to Delete")
        email = st.text_input("Enter Email to the User")
        if st.button("Delete User",key="Delete User"):
            if username:
                print(username)
                try: 
                    user = execute_query(f"select * from users where name='{username}' and email='{email}';")
                    user_df = pd.DataFrame(user, columns=["UserId", "Name", "Email","PhoneNo", "Password", "Admin"])
                    st.table(user_df)
                    delete_user(username,email)
                    print(user)
                except Exception as e:
                    st.error(f"Error {e}")

    # Add New User tab
    with selected_tab[3]:
        with st.form(key='add_user_form'):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phoneno = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            is_admin = st.checkbox("Is Admin")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                user = User(name=name, email=email, phoneno=phoneno, password=password, is_admin=is_admin)
                result = insert_user(user)
                st.success(result)
                
                # Display the added user info
                user = execute_query(f"SELECT * FROM users WHERE name = '{name}'")
                user_df = pd.DataFrame(user, columns=["UserId", "Name", "Email","PhoneNo", "Password", "Admin"])
                st.table(user_df)

    # Logout tab
    with selected_tab[4]:
        if st.button("Logout",key="Logout"):
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


