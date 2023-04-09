import socket
import sys


# handles command line arguments, [server_ip, server_port, file_name]
def argument_handler():
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <server IP> <server port>")
        sys.exit(1)
    else:
        server_ip = sys.argv[1]
        server_port = sys.argv[2]
        server_file = sys.argv[3]

        # call client function
        client(server_ip, server_port, server_file)


# client function
def client(ip, port, file_name):
    
    # create socket, map ip and port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))

    # send file name to server
    s.send(file_name.encode('ascii'))

    # receives file existance from server "File exists" | "File not found"
    file_existance = (s.recv(1024)).decode('ascii')

    # When file exists
    if file_existance == "File exists":
        severmessage = (s.recv(1024)).decode('ascii')
        print("\n" + severmessage)
        print(f"Downloading file {file_name}")
        
        # receive file size from server
        # file_size = (s.recv(1024)).decode('ascii')
        

        # receive file data from server and write to file
        file_data = s.recv(1024)
        file_name = open("client repo/" + file_name, 'wb')
        file_name.write(file_data)

        print("Download complete" + "\n" )

    # When file does not exist
    elif file_existance == "File not found":
        severmessage = (s.recv(1024)).decode('ascii')
        print("\n" + severmessage)

        severmessage = (s.recv(1024)).decode('ascii')
        print(severmessage + "\n")

    s.close()
    sys.exit(1)


if __name__ == "__main__":
    argument_handler()
