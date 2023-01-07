import rsa
import socket

# Opens available keys [Server Private, Client Public]
with open("Public Keys/client-rsa-public.pem") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("Server Side/server-rsa-private.pem") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


def server_program():
    host = socket.gethostname()
    port = 9999
    port2 = 10000

    while True:
        #########################################################################
        # Receiving
        #########################################################################
        # Socket Setup
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(2)
        conn, address = server_socket.accept()

        encrypted_message = conn.recv(2048)
        digital_signature = conn.recv(2048)

        # Decrypted Data
        clear_message = (rsa.decrypt(encrypted_message,
                         private_key)).decode('utf-8')
        # Decrypting and Verifying Signature
        rsa.verify(clear_message.encode(), digital_signature, public_key)

        print(clear_message)

        # Socket Close
        conn.close()

        #########################################################################
        # Sending
        #########################################################################
        # Socket Setup
        client_socket = socket.socket()
        client_socket.connect((host, port2))

        message2 = input("message: ")

        # Encrypted Data
        encrypted_message2 = rsa.encrypt(message2.encode(), public_key)
        # Hashing, Signing, Encrypting Digest
        digital_signature2 = rsa.sign(
            message2.encode(), private_key, "SHA-256")

        # Sending Data
        client_socket.send(encrypted_message2)
        client_socket.send(digital_signature2)

        # Socket Close
        client_socket.close()


if __name__ == '__main__':
    server_program()
