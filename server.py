import socket
import os
import threading
import queue
import time


# request thread
class RequestThread(threading.Thread):
    def __init__(self, connection, address, request_number, request_number_successful):
        # call the init function of the parent class
        threading.Thread.__init__(self)

        self.connection = connection
        self.address = address
        self.request_number = request_number
        self.request_number_successful = request_number_successful
        
        
    # file transfer method
    def run(self):
        ip_address = self.address[0]
        self.request_number += 1
        
        # receive file name from client
        file_name = self.connection.recv(1024).decode('ascii')
        
        # Connection message
        print(f"REQ {self.request_number}: File {file_name} requested from {ip_address}")
        
        # When file exists
        if os.path.isfile("server repo/" + file_name):            
            # Send existance message to client, send total successful requests so far
            self.request_number_successful += 1
            
            self.connection.send("File exists".encode('ascii'))
            
            self.connection.send(f"REQ {self.request_number}: Total successful requests so far = {self.request_number_successful} ".encode('ascii'))
            
            # Send file data to client
            file = open("server repo/"+file_name, 'rb')
            file_data = file.read(1024)
            self.connection.send(file_data)
            
            # Server message
            print(f"REQ {self.request_number}: Total successful requests so far = {self.request_number_successful} ")
            print("File transfer complete\n")
            return self.request_number_successful
            
            

        # When file does not exist
        else:
            # Send existance message to client, send total successful requests so far
            self.connection.send("File not found".encode('ascii'))
            self.connection.send(f"File {file_name} [not] found at server ".encode('ascii'))

            # Server message
            print(f"REQ {self.request_number}: [Not] Successful ")
            print(f"REQ {self.request_number}: Total successful requests so far = {self.request_number_successful} \n")
            
            
            self.connection.send(f"REQ {self.request_number}: Total successful requests so far = {self.request_number_successful} ".encode('ascii'))

        self.connection.close()       
        
        
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 5000))
    server_socket.listen(5)

    request_number = 0
    request_number_successful = 0
    
    max_threads = 10
    
    while True:
        connection, address = server_socket.accept()

        # Every connection/address is put into a queue
        request_queue = queue.Queue()
        request_queue.put(connection)
        request_queue.put(address)

        # Take the first queue item and create a thread. If the number of threads is less than the max number of threads, create a new thread
        if len(threading.enumerate()) < max_threads:
            
            # creates a new thread for file transfer
            thread = RequestThread(request_queue.get(), request_queue.get(), request_number, request_number_successful)
            thread.start() # start the thread
            
            # update the request number and successful request number
            time.sleep(.001) # wait for the thread to finish (if removed, breaks code)
            request_number = thread.request_number
            request_number_successful = thread.request_number_successful
            
            
            
            



                         
if __name__ == "__main__":
    server()
