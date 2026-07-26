import hmac
import hashlib

def sign(key, msg):
    #Returns the raw binary digest, as required for intermediate SigV4 steps
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    #Step01- kDate
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    
    #Step02- kRegion
    kRegion = sign(kDate, region_name)
    
    #Step03- kService
    kService = sign(kRegion, service_name)
    
    #Step04- kSigning
    kSigning = sign(kService, 'aws4_request')
    
    return kDate, kRegion, kService, kSigning

if __name__ == "__main__":
    #Inputs from the assignment
    student_id = "S4129857"
    kSecret = f"{student_id}/K7MDENG+bPxRfiCYEXAMPLEKEY"
    date_val = "20260414"
    region_val = "us-east-1"
    service_val = "iam"

    #Exact string from the assignment
    string_to_sign = (
        "AWS4-HMAC-SHA256\n"
        "20260414M123600Z\n"
        "20260414/us-east-1/iam/aws4_request\n"
        "f536975d06c0309214f805bb90ccff089219ecd68b2577efef23edd43b7e1a59"
    )

    #Calculate Keys
    kDate, kRegion, kService, kSigning = get_signature_key(kSecret, date_val, region_val, service_val)

    #Step05- Final Signature
    signature = hmac.new(kSigning, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    #Output results for the assignment document
    print(f"--- Intermediate Keys (Shown in Hex for Assignment formatting) ---")
    print(f"(1) kDate:    {kDate.hex()}")
    print(f"(2) kRegion:  {kRegion.hex()}")
    print(f"(3) kService: {kService.hex()}")
    print(f"(4) kSigning: {kSigning.hex()}")
    print(f"\n--- Final Result ---")
    print(f"(5) Signature: {signature}")
