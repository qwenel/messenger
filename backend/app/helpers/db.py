from app.database.db import BASE, engine
import logging

logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)


async def setup_databases():
    async with engine.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)

    await engine.dispose()
