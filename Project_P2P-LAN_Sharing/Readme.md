P2P LAN File Sharing System
Overview
A peer-to-peer (P2P) file sharing system designed for Local Area Networks (LAN), enabling users to share, search, download, and upload files effortlessly.
You Tube Video

Features
User Registration: Unique username creation for each user.
File Sharing: Share files from local machines.
Search Functionality: Search shared files by name, type, or description.
Download & Upload: Download shared files and upload new files to share.
File Transfer: Efficient file transfer protocol between peers.
LAN Connectivity: Peer connection via IP addresses or hostnames.
User-Friendly Interface: Easy-to-navigate interface for smooth user interaction.

Optional Features
Access Control: Restrict file sharing based on user roles or permissions.
File Categorization: Categorize shared files (e.g., documents, images, videos).
File Rating: Rate shared files for quality feedback.
Network Discovery: Automatically detect peers on the LAN.

Technical Details
Programming Language: Python.
Network Communication: Used socket programming.
File Transfer Protocol: TCP, UDP, or FTP for efficient file transfers.
Database: SQLite to store user data, file metadata, and search indexes.
Compatibility: Works on Windows, macOS, and Linux.
This project brings seamless file sharing to LAN environments with a focus on usability, flexibility, and scalability.

Steps to execute project-
activate virtual environment
.\env\Scripts\activate

Now, install all dependencies that is in requirements.txt
pip install -r requirements.txt

Run server first
python server.py

Then open another terminal and activate virtual environment
.\env\Scripts\activate

Then, Run client that will open frontend in browser
streamlit run client.py

Final step:
Now, Copy IP address of server from server terminal where we executed 'python server.py'
Then paste that IP on server link left side option on frontend page, then press enter.
Now, Our P2P sharing setup is complete Anyuser can login or signup and share data and also rate files.
For more details about feature refer to youtube video Link given above.
