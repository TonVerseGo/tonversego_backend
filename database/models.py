from tortoise import Model, fields

class User(Model):
    id = fields.BigIntField(pk=True)
    ton_wallet = fields.CharField(max_length=64, unique=True)
    nickname = fields.CharField(max_length=32)
    created_at = fields.DatetimeField(auto_now_add=True)

    nfts: fields.ReverseRelation["NFT"]
    mints: fields.ReverseRelation["NFTMintLog"]

class NFT(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=64)
    ton_address = fields.CharField(max_length=66, unique=True)
    description = fields.CharField(max_length=256)
    photo_url = fields.TextField()
    lat = fields.FloatField()
    lng = fields.FloatField()
    hint = fields.TextField()
    ownet_wallet = fields.CharField(max_length=64, nullable=True)
    model_url = fields.TextField()
    is_found = fields.BooleanField(default=False)
    owner_id = fields.ForeignKeyField("models.User", related_name="nfts")

    mints: fields.ReverseRelation["NFTMintLog"]

class NFTMintLog(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="mints")
    nft = fields.ForeignKeyField("models.NFT", related_name="mints")
    minted_at = fields.DatetimeField(auto_now_add=True)