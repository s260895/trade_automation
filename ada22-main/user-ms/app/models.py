from tortoise import fields, models


class User(models.Model):
    """
        User class
        The credentials used for authentication.
    """
    id = fields.IntField(pk=True)
    broker: fields.ReverseRelation["UserBroker"]
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)


    class Meta:
        table = "users"


class UserBroker(models.Model):
    """
        UserBroker class
        Stores the API credentials to connect to a broker.
    """
    id = fields.IntField(pk=True)
    user: fields.OneToOneRelation[User] = fields.OneToOneField(
        "models.User", related_name="broker"
    )
    url = fields.CharField(max_length=300)
    client_key = fields.CharField(max_length=128)
    client_secret = fields.CharField(max_length=128)


    class Meta:
        table = "brokers"
