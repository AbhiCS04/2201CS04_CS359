#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERVER_PORT 23  // Default Telnet port
#define BUFFER_SIZE 1024

// Function to handle errors
void error(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    int bytes_received;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <Server-IP>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Create a socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        error("Socket creation failed");
    }

    // Set server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    if (inet_pton(AF_INET, argv[1], &server_addr.sin_addr) <= 0) {
        error("Invalid address or address not supported");
    }

    // Establish connection to the server
    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        error("Connection failed");
    }

    printf("Connected to server at %s\n", argv[1]);

    while (1) {
        // Clear buffer and read input from user
        memset(buffer, 0, BUFFER_SIZE);
        printf("Enter command ('quit' to exit from server): ");
        fgets(buffer, BUFFER_SIZE, stdin);

        // Check for 'quit' command to close the connection
        if (strncmp(buffer, "quit", 4) == 0) {
            printf("Closing connection...\n");
            break;
        }

        // Send input to server
        if (send(sockfd, buffer, strlen(buffer), 0) < 0) {
            error("Failed to send data");
        }

        // Clear buffer and receive response from server
        memset(buffer, 0, BUFFER_SIZE);
        bytes_received = recv(sockfd, buffer, BUFFER_SIZE - 1, 0);
        if (bytes_received < 0) {
            error("Failed to receive data");
        }

        // Print server response
        printf("Server response:\n%s\n", buffer);
    }

    // Close the socket
    close(sockfd);
    printf("Connection closed\n");

    return 0;
}

