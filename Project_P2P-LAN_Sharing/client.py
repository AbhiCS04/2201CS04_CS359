# client_streamlit.py
import streamlit as st
import requests
import socketio
import threading
import os
import logging
from datetime import datetime
import queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server Configuration
DEFAULT_SERVER_URL = 'http://192.168.130.52:5000'  # Replace with your server's IP and port 

# Directories
DOWNLOAD_DIR = os.path.abspath('downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize SocketIO client
sio = socketio.Client()

# Initialize a thread-safe queue for chat messages
chat_queue = queue.Queue()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'update_chat_started' not in st.session_state:
    st.session_state.update_chat_started = False

# Function to handle incoming chat messages
@sio.event
def message(data):
    user = data.get('user')
    msg = data.get('msg')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {user}: {msg}"
    chat_queue.put(formatted_message)
    logging.info(f"Received message: {formatted_message}")

# Handle successful connection
@sio.event
def connect():
    logging.info("SocketIO connected.")
    st.session_state.connected = True
    if st.session_state.username:
        sio.emit('join', {'username': st.session_state.username})

# Handle disconnection
@sio.event
def disconnect():
    logging.info("SocketIO disconnected.")
    st.session_state.connected = False

def connect_socketio(server_url, username):
    try:
        sio.connect(server_url)
        logging.info("Connected to SocketIO server.")
    except Exception as e:
        logging.error(f"Failed to connect to chat server: {e}")
        st.error("Failed to connect to chat server.")

def disconnect_socketio(username):
    try:
        sio.emit('leave', {'username': username})
        sio.disconnect()
        logging.info("Disconnected from SocketIO server.")
    except Exception as e:
        logging.error(f"Failed to disconnect from chat server: {e}")

# Function to periodically update chat messages from the queue
def update_chat():
    while True:
        while not chat_queue.empty():
            msg = chat_queue.get()
            st.session_state.chat_messages.append(msg)
        # Sleep briefly to prevent high CPU usage
        sio.sleep(1)

# Streamlit App
def main():
    st.set_page_config(page_title="P2P LAN File Sharing System", layout="wide")
    st.title("P2P LAN File Sharing System")

    if 'menu_choice' not in st.session_state:
        st.session_state.menu_choice = "Login"  # Default menu choice

    # Sidebar for navigation
    menu = ["Login", "Register", "Share Files"]
    if st.session_state.logged_in:
        menu = ["Share Files", "Logout"]

    if st.session_state.logged_in and st.session_state.menu_choice == "Login":
        st.session_state.menu_choice = "Share Files"
    choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state.menu_choice))
    st.session_state.menu_choice = choice  # Update the session state based on user selection

    # Update server URL
    server_url = st.sidebar.text_input("Server URL", DEFAULT_SERVER_URL)

    if choice == "Register":
        st.subheader("Register")
        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
        if submit:
            if not username or not password:
                st.error("Username and password are required.")
            else:
                try:
                    response = requests.post(f"{server_url}/register", data={'username': username, 'password': password})
                    if response.status_code == 201:
                        data = response.json()
                        st.success("Registration successful. Please log in.")
                        logging.info(f"User '{username}' registered successfully.")
                    else:
                        st.error(response.json().get('message', 'Registration failed.'))
                        logging.warning(f"Registration failed for username '{username}'.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to server: {e}")
                    logging.error(f"Registration connection error: {e}")

    elif choice == "Login":
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
        if submit:
            if not username or not password:
                st.error("Username and password are required.")
            else:
                try:
                    response = requests.post(f"{server_url}/login", data={'username': username, 'password': password})
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = data['user_id']
                        st.session_state.username = username
                        st.success("Login successful.")
                        st.session_state.menu_choice = "Share Files"  # Automatically switch to Share Files
                        logging.info(f"User '{username}' logged in successfully.")
                        # Connect to SocketIO in a separate thread
                        if not st.session_state.update_chat_started:
                            threading.Thread(target=connect_socketio, args=(server_url, username), daemon=True).start()
                            threading.Thread(target=update_chat, daemon=True).start()
                            st.session_state.update_chat_started = True
                    else:
                        st.error(response.json().get('message', 'Login failed.'))
                        logging.warning(f"Login failed for username '{username}'.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to server: {e}")
                    logging.error(f"Login connection error: {e}")

    elif choice == "Logout":
        if st.session_state.logged_in:
            disconnect_socketio(st.session_state.username)
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.chat_messages = []
            st.success("Logged out successfully.")
            st.session_state.menu_choice = "Login"  # Automatically switch to Share Files
            logging.info("User logged out successfully.")

    elif choice == "Share Files":
        if st.session_state.logged_in:
            st.subheader(f"Welcome, {st.session_state.username}!")
            # Tabs for different functionalities
            tabs = st.tabs(["Share File", "Search Files", "My Shared Files"])
            # Share File Tab
            with tabs[0]:
                st.markdown("### Share a File")
                uploaded_file = st.file_uploader("Choose a file to share", type=None)
                if uploaded_file is not None:
                    if st.button("Share File"):
                        try:
                            files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
                            data = {
                                'username': st.session_state.username,
                                'user_id': st.session_state.user_id
                            }
                            response = requests.post(f"{server_url}/register_file", data=data, files=files)
                            if response.status_code == 201:
                                st.success("File shared successfully.")
                                logging.info(f"User '{st.session_state.username}' shared file '{uploaded_file.name}'.")
                            else:
                                st.error(response.json().get('message', 'Failed to share file.'))
                                logging.warning(f"File sharing failed for '{uploaded_file.name}'.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Failed to connect to server: {e}")
                            logging.error(f"File sharing connection error: {e}")
            # Search Files Tab
            with tabs[1]:
                st.markdown("### Search Files")

                # Store search results and ratings in session state
                if 'search_results' not in st.session_state:
                    st.session_state.search_results = []

                if 'ratings' not in st.session_state:
                    st.session_state.ratings = {}

                # Track which file's rating slider is shown
                if 'show_slider' not in st.session_state:
                    st.session_state.show_slider = {}

                # Search Form
                with st.form("search_form"):
                    query = st.text_input("File Name")
                    file_type = st.text_input("File Type")
                    submit = st.form_submit_button("Search")

                if submit:
                    try:
                        params = {'query': query, 'file_type': file_type.lower()}  # Send file_type as lowercase
                        response = requests.get(f"{server_url}/search", params=params)
                        if response.status_code == 200:
                            files = response.json().get('files', [])
                            st.session_state.search_results = files  # Save results in session state
                            st.session_state.ratings = {file['file_id']: 5 for file in files}  # Default rating is 5
                            # Initialize slider visibility state
                            st.session_state.show_slider = {file['file_id']: False for file in files}
                        else:
                            st.error("Search failed.")
                            logging.warning("Search request failed.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Failed to connect to server: {e}")
                        logging.error(f"Search connection error: {e}")

                # Display Search Results
                if st.session_state.search_results:
                    logging.info(f"{st.session_state.search_results}")
                    st.markdown("### Search Results")
                    for file in st.session_state.search_results:
                        # Create columns for cleaner alignment
                        col1, col2, col3 = st.columns([3, 1, 1])

                        # Display file details in the first column
                        with col1:
                            st.markdown(
                                f"**Name:** {file['file_name']}  \n"
                                f"**Size:** {file['file_size']} bytes  \n"
                                f"**Shared by:** {file['shared_by']}"
                            )

                        # Show average rating and total votes in the second column
                        with col2:
                            average_rating = file.get('average_rating', 0)
                            rating_count = file.get('rating_count', 0)
                            full_stars = int(average_rating)
                            half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
                            empty_stars = 5 - full_stars - half_star
                            star_display = "★" * full_stars + "✩" * half_star + "☆" * empty_stars
                            st.markdown(f"**Rating:** {star_display} ({rating_count} votes)")

                        # Add a download button in the third column
                        with col3:
                            download_url = f"{server_url}/download/{file['file_id']}"
                            st.markdown(f"[Download]({download_url})", unsafe_allow_html=True)

                        # Button to show rating slider
                        if st.button("Rate this file", key=f"show_slider_{file['file_id']}"):
                            st.session_state.show_slider[file['file_id']] = True

                        # Show the slider if "Rate this file" has been clicked
                        if st.session_state.show_slider.get(file['file_id'], False):
                            rating = st.slider(
                                " ",
                                min_value=1.0,
                                max_value=5.0,
                                value=float(st.session_state.ratings[file['file_id']]),
                                step=0.5,
                                key=f"rating_{file['file_id']}"
                            )

                            # Submit Rating Button
                            if st.button("Submit Rating", key=f"submit_rate_{file['file_id']}"):
                                st.session_state.ratings[file['file_id']] = rating
                                try:
                                    rating = st.session_state.ratings[file['file_id']]
                                    rating_response = requests.post(
                                        f"{server_url}/rate_file",
                                        data={
                                            'file_id': file['file_id'],
                                            'user_id': st.session_state.user_id,
                                            'rating': rating
                                        }
                                    )
                                    if rating_response.status_code == 201:
                                        st.success("Rating submitted successfully.")
                                        logging.info(
                                            f"User {st.session_state.user_id} rated file {file['file_id']} with {rating} stars."
                                        )
                                    else:
                                        st.error(rating_response.json().get('message', 'Failed to submit rating.'))
                                        logging.warning(f"Rating submission failed for file_id {file['file_id']}.")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Failed to connect to server: {e}")
                                    logging.error(f"Rating submission connection error: {e}")

                        st.markdown("---")  # Divider for separating files
            # My Shared Files Tab
            with tabs[2]:
                st.markdown("### My Shared Files")
                try:
                    # Fetch shared files
                    params = {'query': '', 'type': ''}
                    response = requests.get(f"{server_url}/search", params=params)
                    if response.status_code == 200:
                        files = response.json().get('files', [])
                        # Filter files shared by the logged-in user
                        my_files = [file for file in files if file['shared_by'] == st.session_state.username]
                        
                        if my_files:
                            for file in my_files:
                                # Display file details in a similar layout to Search Files
                                col1, col2, col3 = st.columns([3, 1, 1])
                                # File details
                                with col1:
                                    st.markdown(
                                        f"**Name:** {file['file_name']}  \n"
                                        f"**Size:** {file['file_size']} bytes"
                                    )

                                # Display star rating with fractional stars
                                with col2:
                                    average_rating = file.get('average_rating', 0)
                                    rating_count = file.get('rating_count', 0)

                                    # Calculate full, half, and empty stars
                                    full_stars = int(average_rating)
                                    half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
                                    empty_stars = 5 - full_stars - half_star

                                    # Construct star display with full, half, and empty stars
                                    star_display = "★" * full_stars + "✩" * half_star + "☆" * empty_stars
                                    st.markdown(f"**Rating:** {star_display} ({rating_count} votes)")

                                # Add a download button
                                with col3:
                                    download_url = f"{server_url}/download/{file['file_id']}"
                                    st.markdown(f"[Download]({download_url})", unsafe_allow_html=True)

                                st.markdown("---")  # Divider for separating files

                        else:
                            st.info("You haven't shared any files yet.")
                    else:
                        st.error("Failed to fetch your shared files.")
                        logging.warning("Fetching shared files failed.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to server: {e}")
                    logging.error(f"Shared files connection error: {e}")

        else:
            st.markdown(f"#### Please Login [here](http://192.168.130.52:8501/) First", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
