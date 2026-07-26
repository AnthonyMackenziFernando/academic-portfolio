from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from datetime import datetime

C = "Anthony"
S = "Fernando"
student_id = "S4129857"
Lt = "8"

#Exact local time
ts = str(int(datetime(2026, 5, 16, 13, 48, 57).timestamp()))

#128-bit MD5 Key Derivation
Kc = hashlib.md5((C + student_id).encode()).digest()  
Ks = hashlib.md5((S + student_id).encode()).digest()  
nc = hashlib.md5(C.encode()).hexdigest()              

#Randomly chosen 128-bit Session Key (Kc,s)
Kc_s = bytes.fromhex("0123456789ABCDEF0123456789ABCDEF")

#AES-128 CBC Mode encryption/decryption
#Using a fixed Initialization Vector of 16 zero bytes
IV = b'\x00' * 16

def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_data = pad(plaintext.encode(), AES.block_size)
    return cipher.encrypt(padded_data).hex()

def aes_decrypt(key, ciphertext_hex):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_padded = cipher.decrypt(ciphertext)
    return unpad(decrypted_padded, AES.block_size).decode()

#SIMPLIFIED KERBEROS PROTOCOL
print("Phase 1- Authentication Server (AS) Exchange")
#The Ticket generation (Encrypted with Server's Secret Key Ks)
ticket_plaintext = f"{Kc_s.hex()}|{C}|{Lt}"
ticket = aes_encrypt(Ks, ticket_plaintext)
print(f"Ticket (Hex)- {ticket}")

#The AS Response to Client (Encrypted with Client's Secret Key Kc)
#AS_Rep = E_Kc[ Kc,s || nc || Lt || S || Ticket ]
as_rep_plaintext = f"{Kc_s.hex()}|{nc}|{Lt}|{S}|{ticket}"
as_rep = aes_encrypt(Kc, as_rep_plaintext)

print("\nPhase 2- Client/Server Exchange")
#The Authenticator generation (Encrypted with Session Key Kc,s)
#Authenticator = E_Kc,s[ C || ts ]
authenticator_plaintext = f"{C}|{ts}"
authenticator = aes_encrypt(Kc_s, authenticator_plaintext)
print(f"Authenticator (Hex)- {authenticator}")

#The Server Reply to Client (Encrypted with Session Key Kc,s)
#Server_Rep = E_Kc,s[ ts + 1 ]
ts_plus_1 = str(int(ts) + 1)
server_rep_plaintext = f"{ts_plus_1}"
server_rep = aes_encrypt(Kc_s, server_rep_plaintext)
