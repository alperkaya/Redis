#!/usr/bin/env python

import socket
import threading
from redis_process import RedisProcess

def receive_data(sock):
    buffer_size = 1024
    data = b''  # Initialize as bytes

    chunk = sock.recv(buffer_size)
    data += chunk

    return data

def handle_client(client_socket, redis_process):
    while True:
        bytes_data = receive_data(client_socket)
        
        if not bytes_data:
            break
    
        try:
            response = redis_process.set_command(bytes_data)
        except ValueError as e:
            print(f"Error: {e}")
        else:
            client_socket.send(response)

    client_socket.close() 

def start_server():
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to address and port
        port = 6379 
        server_addr = ('', port)
        server_socket.bind(server_addr)

        # Listen for incoming connections
        server_socket.listen(50000)
        #print(f"Server is listening on port {port}")
        redis_process = RedisProcess()
        while True:
            #print("Waiting for connection")
            client_socket, client_addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, redis_process))
            client_thread.start()
    except Exception as e:
        print(f"Error starting server: {e}")
        close_server()

    finally:
        server_socket.close()

def close_server():
    print("Server is closing..") 

def server_start():
    try:
        start_server()
    except KeyboardInterrupt:
        close_server() 