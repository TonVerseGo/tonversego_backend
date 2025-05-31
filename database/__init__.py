import os
from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}

async def init():
    # Get database configuration from environment variables
    DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOSTNAME = os.getenv("DB_HOSTNAME", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "tonverse")

    connection_url = TORTOISE_ORM["connections"]["default"].format(
        DB_USERNAME=DB_USERNAME,
        DB_PASSWORD=DB_PASSWORD,
        DB_HOSTNAME=DB_HOSTNAME,
        DB_PORT=DB_PORT,
        DB_NAME=DB_NAME
    )
    
    config = TORTOISE_ORM.copy()
    config["connections"]["default"] = connection_url
    
    await Tortoise.init(config=config)
    # Create tables
    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()
