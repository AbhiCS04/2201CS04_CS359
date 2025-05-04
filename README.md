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
First clone this repository in your machine, Run-

git clone [https://github.com/AbhiCS04/2201CS04_CS359.git](https://github.com/AbhiCS04/2201CS04_CS359.git)

then setup things as of your need.
Then goto folrder "Project_P2P-LAN_Sharing".
cd Project_P2P-LAN_Sharing
Then execute these commands

##### Activate virtual environment 
(run this command if your machine do not have virtual environment folder named env- "python -m venv env")
.\env\Scripts\activate
##### Now, install all dependencies that is in requirements.txt
pip install -r requirements.txt
![Screenshot 2025-03-23 212411](https://github.com/user-attachments/assets/67d72718-c7a9-4d6c-8f26-a00ce25589fc)

##### Run server first
python server.py
![Screenshot 2025-03-23 212438](https://github.com/user-attachments/assets/f4c948af-4b23-45cb-b003-8c20012bf794)

##### Then open another terminal and activate virtual environment
.\env\Scripts\activate
##### Then, Run client that will open frontend in browser
streamlit run client.py
![Screenshot 2025-03-23 212253](https://github.com/user-attachments/assets/6c659c1b-e42c-4f85-beb0-dc3d280e9975)

##### Final step:
Now, Copy IP address of server from server terminal where we executed 'python server.py' <br>
Then paste that IP on server link left side option on frontend page, then press enter. <br>
![Screenshot 2025-03-23 212608](https://github.com/user-attachments/assets/707191a3-7a3a-45fe-aa5e-74e65b1e01da)

Now, Our P2P sharing setup is complete Any user can login or signup and share data and also rate files. <br>
![Screenshot 2025-03-23 212620](https://github.com/user-attachments/assets/9a5af992-1df0-425a-aa8c-2999b0e56143)

For more details about feature refer to youtube video Link given above. <br>
