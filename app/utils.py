from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#deprecated="auto": This option tells passlib to automatically handle any deprecated algorithms

# pip install bcrypt
def hash(password: str):
    return pwd_context.hash(password)