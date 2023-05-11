import hashlib


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha informada corresponde à senha armazenada no banco de dados"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password
