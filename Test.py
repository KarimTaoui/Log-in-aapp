import pyodbc
import streamlit as st
import streamlit.components.v1 as components
import toml
import os

# Get the absolute path to the directory containing this file
this_dir = os.path.abspath(os.path.dirname(__file__))

# Load secrets from secrets.toml file located in the same directory as this file
secrets_path = os.path.join(this_dir, "C:\Users\moham\OneDrive\Bureau\login\secrets.toml")
secrets = toml.load(secrets_path)


def home_page():
    st.sidebar.title("Navigation")
    st.title('Home Page')
    st.write('Welcome to my Streamlit app!')
    # Establish a connection to the SQL Server database
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LAPTOP-4294FHVD;'
                        'Database=users2;'
                        'Trusted_Connection=yes;')

    # Define a function to check the user credentials
    def check_user_credentials(username, password):
        cursor = conn.cursor()
        query = "INSERT INTO users VALUES (?, ?)"
        data = (username,password)
        cursor.execute(query, data)
        conn.commit()
        
        

    # Define a function to validate the username input
    def validate_username(username):
        if not username:
            return "Please enter a username."
        elif len(username) < 3:
            return "Username should be at least 3 characters long."

    # Define a function to validate the password input
    def validate_password(password):
        if not password:
            return "Please enter a password."
        elif len(password) < 6:
            return "Password should be at least 6 characters long."

    # Create a login form with input fields for username and password
    with st.expander("Login Form"):
        with st.form(key='login_form'):
            username = st.text_input("Username", max_chars=50)
            password = st.text_input("Password", type="password", max_chars=50)
            username_error = validate_username(username)
            password_error = validate_password(password)
            if username_error or password_error:
                st.error("Please fix the following errors:")
                if username_error:
                    st.error(username_error)
                if password_error:
                    st.error(password_error)
            login_button = st.form_submit_button("Login")

    # Handle the login button click event
    if login_button and not username_error and not password_error:
        if check_user_credentials(username, password):
            st.success("Access granted.")
        else:
            st.error("Access denied.")

def about_page():
    st.sidebar.title("Navigation")
    st.title('About Page')
    st.write('This is the about page of my Streamlit app.')
    
PAGES = {
    "Home": home_page,
    "About": about_page
}

def main():
    page = st.sidebar.radio("Go to", list(PAGES.keys()))
    PAGES[page]()

if __name__ == "__main__":
    main()
