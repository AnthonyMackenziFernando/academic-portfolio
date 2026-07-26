import hashlib
from Crypto.Util import number

#Provided Server Long-Term Key Data
n_hex = "d71984b49b05be68473e112d79819f5b71d77d5468c2c9017896c245d2de745d26919cfa290edef287968b8d1e63eb4026d730568a7bb0b65afddf85bc5256848938b4c3f9ab7938b1561a693e0188e5bc1710f3c7204af7b4aa8f891f5d8b1d85bd8cc69bb5eb6ceaab9c6c2329196b66eb4b49460fe7a3db14fdc50232951156de171799f7e29d88c72498e32d0414d34d43ef1ded13c15861d227ed686e7e0c33e1d1d2674b38a712dbf8c9ffca0c62838d15ebbcb75c35cf952d54772d388236b99b7c76469320841de66347ce274ea98973be2374c9863a5827cf5238931e408fc101dcc2edc5387a952dc621d3cfb7d440556829c37fa72471aca12717"
d_hex = "32e1ef7985be6b1761daf5d74b09f5b77d0b9bb32f00fce9a32c0e92d3da19aebb63f0bd609f0af05650af7c57770d7c6473bd148bb7cccaa665adcd8609f83b6bf6851462e84449bbf18157e9fa14f73b723d695d6e6f2d7f886561eb90864b1a8b0755281a75b19325bb5ffd4548a516788c9badbe2f6e9c71afc23dcdd7630e6bd5af7f363ebca1a4f174dd91ad86a3ad058cf40a0190a865dfd19ddb8a36b5c72b0eca70a8c64feac4a91760e37c7b9c066c65000881adf9984b7f879211b331aacd1c7ff44922a1de42c3294220c49cc58529c4d5be218fd6adf2e98a907dc783d969ba61e178fb63a0a87f574a70433d22e4919b4a3b4e909ba24904c1"

n_long = int(n_hex, 16)
d_long = int(d_hex, 16)

#Largest Prime Factor & Ephemeral Key
def largest_prime_factor(num):
    i = 2
    while i * i <= num:
        if num % i: i += 1
        else: num //= i
    return num

student_num = 4129857
e_ephemeral = largest_prime_factor(student_num)

# Generate a random 1024-bit prime for the ephemeral modulus
p_ephemeral = number.getPrime(512)
q_ephemeral = number.getPrime(512)
n_ephemeral = p_ephemeral * q_ephemeral

print(f"Ephemeral Key Parameters")
print(f"e_ephemeral (Largest prime factor of {student_num}): {e_ephemeral}")
print(f"n_ephemeral (1024-bit Modulus Hex):\n{hex(n_ephemeral)[2:]}\n")


#ServerKeyExchange Message
#Hash the ephemeral key components
ephemeral_data = str(n_ephemeral).encode() + str(e_ephemeral).encode()
hashed_ephemeral = hashlib.sha256(ephemeral_data).hexdigest()
hashed_int = int(hashed_ephemeral, 16)

#Sign with the long-term private key (d)
signature = pow(hashed_int, d_long, n_long)

print(f"ServerKeyExchange Signature")
print(f"Signature (Hex):\n{hex(signature)[2:]}\n")


#ClientKeyExchange Message
email_address = "s4129857@student.rmit.edu.au"

#Compute Pre-Master Secret
pre_master_secret_hex = hashlib.sha384(email_address.encode('utf-8')).hexdigest()
pre_master_secret_int = int(pre_master_secret_hex, 16)

#Encrypt Pre-Master Secret with the Ephemeral Public Key
encrypted_pms = pow(pre_master_secret_int, e_ephemeral, n_ephemeral)

print(f"ClientKeyExchange Message")
print(f"Pre-Master Secret (Hex): {pre_master_secret_hex}")
print(f"Encrypted Pre-Master Secret (Hex):\n{hex(encrypted_pms)[2:]}")
