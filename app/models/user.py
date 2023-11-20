from fastapi import Depends

from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import get_session
from app.models.base import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


# from sqlalchemy import DateTime, String, func
# from sqlalchemy.orm import Mapped, mapped_column

# from app.models.base import Base, intpk, str100


# class User(Base):
#     __tablename__ = "user"

#     id: Mapped[intpk]
#     email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
#     password: Mapped[str]
#     first_name: Mapped[str100 | None]
#     last_name: Mapped[str100 | None]
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
