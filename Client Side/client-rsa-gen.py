from cryptography.hazmat.primitives.asymmetric import rsa
import rsa

###############################################################################
# Key Generation        CLIENT
###############################################################################
public_key, private_key = rsa.newkeys(2048)

with open("Client Side/client-rsa-private.pem", "wb") as private_key_file:
    private_key_file.write(private_key.save_pkcs1("PEM"))
    private_key_file.close()

with open("Public Keys/client-rsa-public.pem", "wb") as public_key_file:
    public_key_file.write(public_key.save_pkcs1("PEM"))
    public_key_file.close()

print("Successfully created new key pair for CLIENT")
###############################################################################
