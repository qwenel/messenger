from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import config
import logging


BASE = declarative_base(metadata=MetaData(config.DATABASE_SCHEME))


# Асинхронная сессия
@asynccontextmanager
async def engine_session():
    async with __async_session_factory__engine() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            await session.invalidate()
            logging.error(f"[Ошибка SQLAlchemy] {e}")
            await session.close()
            raise


# Синхронная сессия
@contextmanager
def engine_session_sync():
    session = __sync_session_factory__engine()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logging.error(f"[Ошибка SQLAlchemy] {e}")
        session.close()
        raise
    finally:
        session.close()


engine = create_async_engine(
    config.ASYNC_DATABASE_URI,
    echo=False,
    connect_args={"server_settings": {"search_path": f"{config.DATABASE_SCHEME}"}},
    pool_size=16,
    max_overflow=10,
    pool_timeout=30
)

engine_sync = create_engine(
    config.DATABASE_URI,
    connect_args={"options": f"-c search_path={config.DATABASE_SCHEME}"},
)

__async_session_factory__engine = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

__sync_session_factory__engine = sessionmaker(autocommit=False, bind=engine_sync)
