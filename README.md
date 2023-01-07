# cryptography-client-server
program to establish a connection that sends secure application messages from
a client to a server using the Python

# packages
```
pip install rsa
pip install socket
```

# Order of opperation:
1. Keys must be generated
	a) run 		Client Side/client-rsa-gen.py
	b) run		Server Side/server-rsa-gen.py
	NOTE:
	 - Private keys are stored in each directory corresponding to the 
	   client and server.
	 - All public keys generated are in the Public Keys/ directory
	 - Every key file will be stored as a .PEM file, and will NOT need
	   to be regenerated after every file exchange

2. File transfer scripts must be run in order
	a) run 		server.py
	b) run 		client.py
	
3. The message transmission works both ways, but in sequence
   i.e 	client -> server -> client -> server ...
   
   SENDING
   - signes the digest with the clients private key
   - uses the servers public key to encrypt the clients secret key

   RECEIVING
   - decrypts both the message and digital signature with the servers private key
   - verifies the digital signature with the clients public key
   - prints the message in terminal
