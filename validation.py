import re

def validate_email(email: str) -> bool:
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(email_pattern, email))

def validate_phone(phoneno: str) -> bool:
    phone_pattern = r"^\d{10}$"
    return bool(re.match(phone_pattern, phoneno))

def validate_password(password: str) -> bool:
    return len(password) >= 8

def validate_user_input(email: str, phoneno: str, password: str) -> bool:
    return validate_email(email) and validate_phone(phoneno) and validate_password(password)
