import models
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


UserIn_Pydantic = pydantic_model_creator(
    models.User, name="UserIn", include=(
        "username", "password",
    )
)
UserOut_Pydantic = pydantic_model_creator(
    models.User, name="UserOut", include=(
        "id", "username",
    )
)
UserBrokerIn_Pydantic = pydantic_model_creator(
    models.UserBroker, name="UserBrokerIn", include=(
        "url", "client_key", "client_secret",
    )
)
UserBrokerOut_Pydantic = pydantic_model_creator(
    models.UserBroker, name="UserBrokerOut", include=(
        "id", "user_id", "url", "client_key", "client_secret",
    )
)


class Status(BaseModel):
    message: str
