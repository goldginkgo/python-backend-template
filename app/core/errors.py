from fastapi import HTTPException, status


class BackendError(Exception):
    pass


class RetryableError(BackendError):
    pass


class AuthTokenExpiredHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
