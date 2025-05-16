# app/core/config.py
import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API settings
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Document Processor API"
    PROJECT_DESCRIPTION: str = (
        "API for processing Word documents and storing extracted data in Firestore"
    )
    VERSION: str = "1.0.0"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Firebase settings
    FIREBASE_PROJECT_ID: str = "hilo-ai-platform-uat"
    FIREBASE_CLIENT_EMAIL: str = "firebase-adminsdk-fbsvc@hilo-ai-platform-uat.iam.gserviceaccount.com"
    FIREBASE_PRIVATE_KEY: str = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDv9tqucT08mSYL\nUsySw8zClcc+XJUnvw0+0ysgOIbFxrj32Zij7LppOMc0p+H17pbEIsgI8CLOZxqa\nO9YRHj/RCJ0FdVzV1trrhlMsOh4kgNhadBm+MBnd8sIaoFHor4iuKTGsKJikGHuP\ngNw9j7GNUY9JJGB6YZdUNA5Wa9dFKNkIEBFRXUn/ioMIe+4IVGi3kohUp52xeHUG\nR7eiRWEpTBcRBR91xGwYGx7o5I+v1zRVxogzeHcaXPmf175s61twX5Hekq+hfkT1\nY6mJ/wjsS4HsOaBcoIkd6ykWZPPTvPAkeFlvQI/DjBLkMbjXd4wzfHYB+Z3X85CH\nSnw5HnNNAgMBAAECggEAKpaB4LBVyS24EA3po0mPS2CYPDPjv+pbMDF7p6wIlUzL\n0qcifUNcISUTy79Y7dQim1w96sIttzqawNFKUH7xHgj8jzWxXH1VnLPaCpEk/N8G\nJuWQlQ3F5Xt6Yg3eg6C1rg0/FNoenw7+TO12iRF51kYpmzZSzh2IZUgY3FMm4U3C\n2s8R9iqR+5+qO8HOLw27u2WPZzXKVNa5EKJOflP6Di7WJUdQPo5p6+Oqx2b+2ZNu\nqqvSe/Nu+L6+HILdYKtKHbot4aCeCJnwMXGWvMchLNpeT2Lhnr4L7+ISo1zAw7w5\nCaxRvr3YHitpfXAvSjpqxeLvyk8Z8JrgGGmsv61lQQKBgQD8lIEYivdX4cUU8kXb\nKhmhptGQtn5qCguIu6hha0s6lk7KAR1/nZiE3Xf3mM8GfOFlQgCMB9gUcCRuDBw1\n0sRrQ9e42jAY3fMD/je5X0ZwtCgJhgPId175E69iE4ehE9Rxm1Ls5AAWxt9lLZuR\nWcJAA3C6Wk2FsIREw979uG2tjQKBgQDzNp7weN5TCulCaQhjcAYDnd+U5JqpJPCg\nIVL3Refm13bD4mJZjcweHVAftmPaD5954vNe/ks8uMlca9iWvLQfuyFc4DZVvhHW\nIK5hRwuBjiKIA9hKhOkc4wzyIpPO4mtsft7txyTJm67IULHFeQ9BsYHy1ryfpuyh\nkTW7YnwMwQKBgQDlYv1HS9XMg2cYWdslaruyeq0ybvqp1Qual0sZhnbg82cEwDSJ\nFJhSekwcmjPSYZHWAzY59lnAXgRHyUnJe+wUup1s7QLnYpL0mmkDOkrfyk3eME65\nPegL71vFh5USrc6vim+qYnrONLjny57QR6NJvZYgOCjVdHT7eqPG6zr4dQKBgEpm\nWxiU4O3mWJTILJi+nBhfIxYZGHbFphZWG1spN1eWce5aQlvC1L4hmXEaClGald5j\nXq+gesOIg5CSLR9vemp6hCo1LGnuSuaF+NIpOYvYPxf8lR22qtj7W+p2SWDwQoxe\nAzQZx1clGMKObNNLxS8Dbg0rQ2hTV+/Uy+sWpXwBAoGBAI2eorPMQE2ZfHJ9u7V5\nJELiuDxj2a9ZuiEJVDl8wGbrzlAgT3AyjwL91ECboO8K/s/rx+irZIwqfmnl169x\n3/cEcAyMbyaydDHcqh7LA6uOAy7iNCqdMV7qPh7v1lmWV+bnstbZrrrX4u0I3Wlj\nMQYXyOG7sMl5b/tHPNWy1nmZ\n-----END PRIVATE KEY-----\n"
    FIREBASE_DATABASE_URL: str = "https://hilo-ai-platform-uat.firebaseio.com"
    FIREBASE_STORAGE_BUCKET: str = "hilo-ai-platform-uat.appspot.com"
    FIREBASE_COLLECTION_NAME: str = "processed_documents"
    FIREBASE_CREDENTIALS: dict = {
        "type": "service_account",
        "project_id": "hilo-ai-platform-uat",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDv9tqucT08mSYL\nUsySw8zClcc+XJUnvw0+0ysgOIbFxrj32Zij7LppOMc0p+H17pbEIsgI8CLOZxqa\nO9YRHj/RCJ0FdVzV1trrhlMsOh4kgNhadBm+MBnd8sIaoFHor4iuKTGsKJikGHuP\ngNw9j7GNUY9JJGB6YZdUNA5Wa9dFKNkIEBFRXUn/ioMIe+4IVGi3kohUp52xeHUG\nR7eiRWEpTBcRBR91xGwYGx7o5I+v1zRVxogzeHcaXPmf175s61twX5Hekq+hfkT1\nY6mJ/wjsS4HsOaBcoIkd6ykWZPPTvPAkeFlvQI/DjBLkMbjXd4wzfHYB+Z3X85CH\nSnw5HnNNAgMBAAECggEAKpaB4LBVyS24EA3po0mPS2CYPDPjv+pbMDF7p6wIlUzL\n0qcifUNcISUTy79Y7dQim1w96sIttzqawNFKUH7xHgj8jzWxXH1VnLPaCpEk/N8G\nJuWQlQ3F5Xt6Yg3eg6C1rg0/FNoenw7+TO12iRF51kYpmzZSzh2IZUgY3FMm4U3C\n2s8R9iqR+5+qO8HOLw27u2WPZzXKVNa5EKJOflP6Di7WJUdQPo5p6+Oqx2b+2ZNu\nqqvSe/Nu+L6+HILdYKtKHbot4aCeCJnwMXGWvMchLNpeT2Lhnr4L7+ISo1zAw7w5\nCaxRvr3YHitpfXAvSjpqxeLvyk8Z8JrgGGmsv61lQQKBgQD8lIEYivdX4cUU8kXb\nKhmhptGQtn5qCguIu6hha0s6lk7KAR1/nZiE3Xf3mM8GfOFlQgCMB9gUcCRuDBw1\n0sRrQ9e42jAY3fMD/je5X0ZwtCgJhgPId175E69iE4ehE9Rxm1Ls5AAWxt9lLZuR\nWcJAA3C6Wk2FsIREw979uG2tjQKBgQDzNp7weN5TCulCaQhjcAYDnd+U5JqpJPCg\nIVL3Refm13bD4mJZjcweHVAftmPaD5954vNe/ks8uMlca9iWvLQfuyFc4DZVvhHW\nIK5hRwuBjiKIA9hKhOkc4wzyIpPO4mtsft7txyTJm67IULHFeQ9BsYHy1ryfpuyh\nkTW7YnwMwQKBgQDlYv1HS9XMg2cYWdslaruyeq0ybvqp1Qual0sZhnbg82cEwDSJ\nFJhSekwcmjPSYZHWAzY59lnAXgRHyUnJe+wUup1s7QLnYpL0mmkDOkrfyk3eME65\nPegL71vFh5USrc6vim+qYnrONLjny57QR6NJvZYgOCjVdHT7eqPG6zr4dQKBgEpm\nWxiU4O3mWJTILJi+nBhfIxYZGHbFphZWG1spN1eWce5aQlvC1L4hmXEaClGald5j\nXq+gesOIg5CSLR9vemp6hCo1LGnuSuaF+NIpOYvYPxf8lR22qtj7W+p2SWDwQoxe\nAzQZx1clGMKObNNLxS8Dbg0rQ2hTV+/Uy+sWpXwBAoGBAI2eorPMQE2ZfHJ9u7V5\nJELiuDxj2a9ZuiEJVDl8wGbrzlAgT3AyjwL91ECboO8K/s/rx+irZIwqfmnl169x\n3/cEcAyMbyaydDHcqh7LA6uOAy7iNCqdMV7qPh7v1lmWV+bnstbZrrrX4u0I3Wlj\nMQYXyOG7sMl5b/tHPNWy1nmZ\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-fbsvc@hilo-ai-platform-uat.iam.gserviceaccount.com",
    }

    # Document processing settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".docx", ".pdf"]

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
