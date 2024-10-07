#define _WIN32_WINNT 0x0601  // Windows 7 or later

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

#define DEFAULT_PORT "23"  // Telnet default port
#define BUFFER_SIZE 1024

void cleanup(SOCKET sock) {
    closesocket(sock);
    WSACleanup();
}

// Function to handle Telnet control sequences
void handle_telnet_control(SOCKET ConnectSocket) {
    const char *terminal_type = "\xFF\xFB\x18";  // IAC DO TERMINAL-TYPE
    send(ConnectSocket, terminal_type, strlen(terminal_type), 0);
}

int main(int argc, char *argv[]) {
    WSADATA wsaData;
    SOCKET ConnectSocket = INVALID_SOCKET;
    struct addrinfo *result = NULL, *ptr = NULL, hints;
    char sendbuf[BUFFER_SIZE];
    char recvbuf[BUFFER_SIZE];
    int iResult, recvbuflen = BUFFER_SIZE;

    // Check command line arguments
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <server address>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        fprintf(stderr, "WSAStartup failed: %d\n", iResult);
        return EXIT_FAILURE;
    }

    // Set up hints structure for TCP connection
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;        // Allow IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM;    // Stream socket
    hints.ai_protocol = IPPROTO_TCP;    // TCP protocol

    // Resolve server address and port
    iResult = getaddrinfo(argv[1], DEFAULT_PORT, &hints, &result);
    if (iResult != 0) {
        fprintf(stderr, "getaddrinfo failed: %d\n", iResult);
        WSACleanup();
        return EXIT_FAILURE;
    }

    // Attempt to connect to the first resolved address
    for (ptr = result; ptr != NULL; ptr = ptr->ai_next) {
        ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
        if (ConnectSocket == INVALID_SOCKET) {
            fprintf(stderr, "Socket failed: %ld\n", WSAGetLastError());
            cleanup(ConnectSocket);
            return EXIT_FAILURE;
        }

        // Establish connection
        iResult = connect(ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (iResult == SOCKET_ERROR) {
            closesocket(ConnectSocket);
            ConnectSocket = INVALID_SOCKET;
            continue; // Try next address
        }
        break; // Successfully connected
    }

    freeaddrinfo(result); // Free address info

    // Check if connection was successful
    if (ConnectSocket == INVALID_SOCKET) {
        fprintf(stderr, "Unable to connect to server!\n");
        WSACleanup();
        return EXIT_FAILURE;
    }

    // Handle Telnet control sequence for terminal type negotiation
    handle_telnet_control(ConnectSocket);

    printf("Connected to the server. Type your commands (type 'quit' to exit):\n");

    // Main loop to send and receive data
    do {
        printf("Command> ");
        // Read user input
        if (fgets(sendbuf, BUFFER_SIZE, stdin) == NULL) {
            fprintf(stderr, "Input error.\n");
            break;
        }

        // Remove newline character from input
        sendbuf[strcspn(sendbuf, "\n")] = '\0';

        // Check for quit command
        if (strcmp(sendbuf, "quit") == 0) {
            break; // Exit loop
        }

        // Send command to the server
        iResult = send(ConnectSocket, sendbuf, (int)strlen(sendbuf), 0);
        if (iResult == SOCKET_ERROR) {
            fprintf(stderr, "Send failed: %ld\n", WSAGetLastError());
            cleanup(ConnectSocket);
            return EXIT_FAILURE;
        }

        // Receive data from server
        iResult = recv(ConnectSocket, recvbuf, recvbuflen, 0);
        if (iResult > 0) {
            // Filter out Telnet control sequences
            int j = 0;
            for (int i = 0; i < iResult; i++) {
                if ((unsigned char)recvbuf[i] == 255) {
                    // Skip control sequences
                    if (i + 2 < iResult) {
                        i += 2;  // Skip over IAC sequences
                    }
                } else {
                    recvbuf[j++] = recvbuf[i];  // Copy valid data
                }
            }
            recvbuf[j] = '\0';  // Null-terminate the received data
            printf("Server> %s\n", recvbuf);
        } else if (iResult == 0) {
            printf("Connection closed\n");
            break;
        } else {
            fprintf(stderr, "Recv failed: %ld\n", WSAGetLastError());
            cleanup(ConnectSocket);
            return EXIT_FAILURE;
        }

    } while (1);

    // Cleanup
    cleanup(ConnectSocket);
    printf("Connection closed.\n");
    return EXIT_SUCCESS;
}