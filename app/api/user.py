from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import auth_backend, current_active_user, fastapi_users, github_client
from app.utils.settings import settings

router = APIRouter()


router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

router.include_router(
    fastapi_users.get_oauth_router(
        github_client,
        auth_backend,
        settings.SECRET_KEY,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/auth/oauth2",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_oauth_associate_router(github_client, UserRead, settings.SECRET_KEY),
    prefix="/auth/associate/oauth2",
    tags=["auth"],
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


# @router.post("/register", status_code=status.HTTP_201_CREATED)
# async def register_user(
#     user_data: UserIn,
#     session: AsyncSession = Depends(get_session),
# ):
#     return await UserService.register_user(user_data, session)


# @router.post("/token", status_code=status.HTTP_200_OK)
# async def token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: AsyncSession = Depends(get_session),
# ) -> Token:
#     return await UserService.login(form_data, session)


# @router.get("/login", status_code=status.HTTP_200_OK)
# async def login(current_user=Depends(UserService.get_current_user)) -> UserOut:
#     return UserOut.model_validate(current_user)


# @router.get("/get_by_id/{user_id}", status_code=status.HTTP_200_OK)
# async def get_user_by_id(
#     user_id: int,
#     session: AsyncSession = Depends(get_session),
# ) -> UserOut:
#     return await UserService.get_user_by_id(user_id, session)


# @router.get("/get_all", status_code=status.HTTP_200_OK)
# async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
#     return await UserService.get_all_users(session)


# @router.delete("/delete_by_id/{user_id}", status_code=status.HTTP_200_OK)
# async def delete_user_by_id(
#     user_id: int,
#     session: AsyncSession = Depends(get_session),
# ):
#     return await UserService.delete_user_by_id(user_id, session)


# @router.delete("/delete_all", status_code=status.HTTP_200_OK)
# async def delete_all_users(session: AsyncSession = Depends(get_session)):
#     return await UserService.delete_all_users(session)


# @router.patch(
#     "/change_password",
#     status_code=status.HTTP_200_OK,
#     summary="Change password for current user that is logged in",
# )
# async def change_password(
#     password_data: ChangePasswordIn,
#     current_user=Depends(UserService.get_current_user),
#     session: AsyncSession = Depends(get_session),
# ):
#     return await UserService.change_password(password_data, current_user, session)
