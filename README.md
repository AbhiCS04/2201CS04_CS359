# P2P LAN File Sharing System
#### Overview
A peer-to-peer (P2P) file sharing system designed for Local Area Networks (LAN), enabling users to share, search, download, and upload files effortlessly. <br>
[You Tube Video](https://youtu.be/EihcUknVq10) <br>
#### Features
User Registration: Unique username creation for each user. <br>
File Sharing: Share files from local machines. <br>
Search Functionality: Search shared files by name, type, or description. <br>
Download & Upload: Download shared files and upload new files to share. <br>
File Transfer: Efficient file transfer protocol between peers. <br>
LAN Connectivity: Peer connection via IP addresses or hostnames. <br>
User-Friendly Interface: Easy-to-navigate interface for smooth user interaction. <br>
#### Optional Features
Access Control: Restrict file sharing based on user roles or permissions. <br>
File Categorization: Categorize shared files (e.g., documents, images, videos). <br>
File Rating: Rate shared files for quality feedback. <br>
Network Discovery: Automatically detect peers on the LAN. <br>
#### Technical Details
Programming Language: Python. <br>
Network Communication: Used socket programming. <br>
File Transfer Protocol: TCP, UDP, or FTP for efficient file transfers. <br>
Database: SQLite to store user data, file metadata, and search indexes. <br>
Compatibility: Works on Windows, macOS, and Linux. <br>
This project brings seamless file sharing to LAN environments with a focus on usability, flexibility, and scalability. <br>

#### Steps to execute project-
##### activate virtual environment 
.\env\Scripts\activate
##### Now, install all dependencies that is in requirements.txt
pip install -r requirements.txt
##### Run server first
python server.py
##### Then open another terminal and activate virtual environment
.\env\Scripts\activate
##### Then, Run client that will open frontend in browser
streamlit run client.py
##### Final step:
Now, Copy IP address of server from server terminal where we executed 'python server.py' <br>
Then paste that IP on server link left side option on frontend page, then press enter. <br>
Now, Our P2P sharing setup is complete Anyuser can login or signup and share data and also rate files. <br>
For more details about feature refer to youtube video Link given above. <br>
