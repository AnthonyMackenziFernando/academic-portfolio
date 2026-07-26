import os
import hashlib

# CONSTANTS PROVIDED
p = 178011905478542266528237562450159990145232156369120674273274450314442865788737020770612695252123463079567156784778466449970650770920727857050009668388144034129745221171818506047231150039301079959358067395348717066319802262019714966524135060945913707594956514672855690606794135837542707371727429551343320695239
g = 174068207532402095185811980123523436538604490794561350978495831040599953488455823147851597408940950725307797094915759492368300574252438761037084473467180148876118103083043754985190983472601550494691329488083395492313850000361646482644608492304078721818959999056496097769368017749273708962006689187956744210730

#160-bit Random Number Generator and SHA1
def generate_160bit_random():
    return os.urandom(20)

def compute_sha1(data_bytes):
    # Returns the hex representation of the SHA1 hash
    return hashlib.sha1(data_bytes).hexdigest()

#Modular Exponentiation using Student ID
print("Modular Exponentiation")
student_id = "S4129857"
print(f"Student ID: {student_id}")

#Compute X = SHA1(student ID)
X_hex = compute_sha1(student_id.encode('utf-8'))
X = int(X_hex, 16) # Convert hex string to integer

#Using built-in pow() for optimized modular exponentiation
Y = pow(g, X, p)

print(f"X (Hex): {X_hex}")
print(f"Y = g^X mod p: \n{Y}\n")

#Diffie-Hellman Key Exchange
print("Key Establishment")

#Step A- Generate random bytes for a and b
a_bytes = generate_160bit_random()
b_bytes = generate_160bit_random()

#Step B- Compute A and B
A_hex = compute_sha1(a_bytes + b"Anthony")
B_hex = compute_sha1(b_bytes + b"Fernando")

#Convert hashes to integers
A = int(A_hex, 16)
B = int(B_hex, 16)

#Step C: Compute public values to exchange
vpc_public = pow(g, A, p)
dc_public = pow(g, B, p)

print(f"VPC (Anthony) outputs (A, g^A mod p): \n({A_hex}, \n{vpc_public})\n")
print(f"Data Centre (Fernando) outputs (B, g^B mod p): \n({B_hex}, \n{dc_public})\n")

#Step D: Compute the shared secret key
#VPC receives dc_public and raises it to power A
secret_vpc = pow(dc_public, A, p)

#Data Centre receives vpc_public and raises it to power B
secret_dc = pow(vpc_public, B, p)

#Ensure both secrets match (they mathematically must)
assert secret_vpc == secret_dc

print(f"Established Secret Key (g^AB mod p): \n{secret_vpc}")
