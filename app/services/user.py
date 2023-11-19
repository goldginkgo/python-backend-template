from fastapi import Depends, Request

import uuid
from typing import Optional

from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.models.user import User, get_user_db
from app.utils.logger import get_logger
from app.utils.settings import settings

logger = get_logger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


# from fastapi import Depends, HTTPException, status
# from fastapi.responses import JSONResponse
# from fastapi.security import OAuth2PasswordRequestForm

# from datetime import timedelta

# from jose import JWTError, jwt
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.database import get_session
# from app.daos import user
# from app.models.user import User as UserModel
# from app.schemas.token import Token, TokenData
# from app.schemas.user import ChangePasswordIn, UserIn, UserOut
# from app.services.utils import UtilsService, oauth2_scheme
# from app.utils.logger import get_logger
# from app.utils.settings import settings

# logger = get_logger(__name__)


# class UserService:
#     @staticmethod
#     async def register_user(user_data: UserIn, session: AsyncSession):
#         user_exist = await UserService.user_email_exists(session, user_data.email)

#         if user_exist:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User with the given email already exists!!!",
#             )

#         user_data.password = UtilsService.get_password_hash(user_data.password)
#         new_user = await user.UserDao(session).create(user_data.model_dump())
#         logger.info(f"New user created successfully: {new_user}!!!")
#         return JSONResponse(
#             content={"message": "User created successfully"},
#             status_code=status.HTTP_201_CREATED,
#         )

#     @staticmethod
#     async def authenticate_user(session: AsyncSession, email: str, password: str) -> UserModel | bool:
#         _user = await user.UserDao(session).get_by_email(email)
#         if not _user or not UtilsService.verify_password(password, _user.password):
#             return False
#         return _user

#     @staticmethod
#     async def user_email_exists(session: AsyncSession, email: str) -> UserModel | None:
#         _user = await user.UserDao(session).get_by_email(email)
#         return _user if _user else None

#     @staticmethod
#     async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession) -> Token:
#         _user = await UserService.authenticate_user(session, form_data.username, form_data.password)
#         if not _user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Incorrect email or password",
#             )

#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = UtilsService.create_access_token(data={"sub": _user.email}, expires_delta=access_token_expires)  # type: ignore
#         token_data = {
#             "access_token": access_token,
#             "token_type": "Bearer",
#         }
#         return Token(**token_data)

#     @staticmethod
#     async def get_current_user(
#         session: AsyncSession = Depends(get_session),
#         token: str = Depends(oauth2_scheme),
#     ) -> UserModel:
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#             email: str = payload.get("sub")
#             if not email:
#                 raise credentials_exception
#             token_data = TokenData(email=email)
#         except JWTError as ex:
#             raise credentials_exception from ex
#         _user = await user.UserDao(session).get_by_email(email=token_data.email)
#         if not _user:
#             raise credentials_exception
#         return _user

#     @staticmethod
#     async def get_all_users(session: AsyncSession) -> list[UserOut]:
#         all_users = await user.UserDao(session).get_all()
#         return [UserOut.model_validate(_user) for _user in all_users]

#     @staticmethod
#     async def delete_all_users(session: AsyncSession):
#         await user.UserDao(session).delete_all()
#         return JSONResponse(
#             content={"message": "All users deleted successfully!!!"},
#             status_code=status.HTTP_200_OK,
#         )

#     @staticmethod
#     async def change_password(
#         password_data: ChangePasswordIn,
#         current_user: UserModel,
#         session: AsyncSession = Depends(get_session),
#     ):
#         if not UtilsService.verify_password(password_data.old_password, current_user.password):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Incorrect old password!!!",
#             )
#         current_user.password = UtilsService.get_password_hash(password_data.new_password)
#         session.add(current_user)
#         await session.commit()
#         return JSONResponse(
#             content={"message": "Password updated successfully!!!"},
#             status_code=status.HTTP_200_OK,
#         )

#     @staticmethod
#     async def get_user_by_id(user_id: int, session: AsyncSession) -> UserOut:
#         _user = await user.UserDao(session).get_by_id(user_id)
#         if not _user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User with the given id does not exist!!!",
#             )
#         return UserOut.model_validate(_user)

#     @staticmethod
#     async def delete_user_by_id(user_id: int, session: AsyncSession):
#         _user = await user.UserDao(session).delete_by_id(user_id)
#         if not _user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User with the given id does not exist!!!",
#             )
#         return JSONResponse(
#             content={"message": "User deleted successfully!!!"},
#             status_code=status.HTTP_200_OK,
#         )
