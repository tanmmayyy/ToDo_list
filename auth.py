from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# dict stores users id, hashed pass in key value pair
users_info = {}

if __name__ == "__main__":
    
    password = "abc@123"
    
    
    hashed = hash_password(password)
    print("hashed password", hashed)
    
    print(verify_password("abc@123", hashed))
    print(verify_password("qwer@12", hashed))
    