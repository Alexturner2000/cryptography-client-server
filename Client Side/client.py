import rsa
import socket

# Opens available keys [Client Private, Server Public]
with open("Public Keys/server-rsa-public.pem") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("Client Side/client-rsa-private.pem") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


def client_program():
    host = socket.gethostname()
    port = 9999
    port2 = 10000

    while True:
        #########################################################################
        # Sending
        #########################################################################
        # Socket Setup
        client_socket = socket.socket()
        client_socket.connect((host, port))

        message = input("message: ")

        # Encrypted Data
        encrypted_message = rsa.encrypt(message.encode(), public_key)
        # Hashing, Signing, Encrypting Digest
        digital_signature = rsa.sign(message.encode(), private_key, "SHA-256")

        # Sending Data
        client_socket.send(encrypted_message)
        client_socket.send(digital_signature)

        # Socket Close
        client_socket.close()

        #########################################################################
        # Receiving
        #########################################################################
        # Socket Setup
        server_socket = socket.socket()
        server_socket.bind((host, port2))
        server_socket.listen(2)
        conn, address = server_socket.accept()

        encrypted_message2 = conn.recv(2048)
        digital_signature2 = conn.recv(2048)

        # Decrypted Data
        clear_message2 = (rsa.decrypt(encrypted_message2,
                                      private_key)).decode('utf-8')
        # Decrypting and Verifying Signature
        rsa.verify(clear_message2.encode(), digital_signature2, public_key)

        print(clear_message2)

        # Socket Close
        conn.close()


if __name__ == '__main__':
    client_program()
