from models import User, UserBroker
from schemas import UserOut_Pydantic, UserIn_Pydantic, UserBrokerIn_Pydantic, UserBrokerOut_Pydantic, Status
from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist
from utils.exceptions import not_found


user_router = APIRouter(tags=["users"])


"""User endpoints"""
@user_router.post("/users", response_model=UserOut_Pydantic, description="Register a new user.")
async def register(user: UserIn_Pydantic):
    new_user = await User.create(**user.dict(exclude_unset=True))
    return await UserOut_Pydantic.from_tortoise_orm(new_user)


@user_router.put("/users/{user_id}", response_model=UserOut_Pydantic, responses={404: {"model": HTTPNotFoundError}}, description="Update a user.")
async def update_user(user_id: int, updated_user: UserIn_Pydantic):
    await User.filter(id=user_id).update(**updated_user.dict(exclude_unset=True))

    try:
        user = User.get(id=user_id)
    except DoesNotExist:
        raise not_found

    return await UserOut_Pydantic.from_queryset_single(user)


@user_router.delete("/users/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}, description="Delete a user.")
async def delete_user(user_id: int):
    user_delete = await User.filter(id=user_id).delete()
    await UserBroker.filter(user_id=user_id).delete()

    if not user_delete:
        raise not_found

    return Status(message=f"User {user_id} was deleted")


"""UserBroker endpoints"""
@user_router.post("/users/{user_id}/broker", response_model=UserBrokerOut_Pydantic, description="Create a broker for a user.")
async def create_user_broker(user_id: int, user_broker: UserBrokerIn_Pydantic):
    import sys
    print(user_broker.dict(), file=sys.stderr)
    user_broker_dict = user_broker.dict(exclude_unset=True)
    user_broker_dict["user_id"] = user_id
    print(user_broker_dict, file=sys.stderr)
    new_user_broker = await UserBroker.create(**user_broker_dict)
    return await UserBrokerOut_Pydantic.from_tortoise_orm(new_user_broker)


@user_router.get('/users/{user_id}/broker', response_model=UserBrokerOut_Pydantic, responses={404: {"model": HTTPNotFoundError}}, description="Retrieve the broker for a user.")
async def get_user_broker(user_id: int):
    try:
        user_broker = UserBroker.get(user_id=user_id)
    except DoesNotExist:
        raise not_found

    return await UserBrokerOut_Pydantic.from_queryset_single(user_broker)


@user_router.put("/users/{user_id}/broker", response_model=UserBrokerOut_Pydantic, responses={404: {"model": HTTPNotFoundError}}, description="Update the broker of a user.")
async def update_user_broker(user_id: int, updated_user_broker: UserBrokerIn_Pydantic):
    # User may not be changed
    updated_user_broker = updated_user_broker.dict(exclude_unset=True)
    updated_user_broker.pop("user_id", None)
    updated_user_broker.pop("user", None)

    await UserBroker.filter(user_id=user_id).update(**updated_user_broker)

    try:
        user_broker = UserBroker.get(user_id=user_id)
    except DoesNotExist:
        raise not_found

    return await UserBrokerOut_Pydantic.from_queryset_single(user_broker)


@user_router.delete("/users/{user_id}/broker", response_model=Status, responses={404: {"model": HTTPNotFoundError}}, description="Delete a user's broker.")
async def delete_user(user_id: int):
    broker_delete = await UserBroker.filter(user_id=user_id).delete()

    if not broker_delete:
        raise not_found

    return Status(message=f"UserBroker {user_id} was deleted")
