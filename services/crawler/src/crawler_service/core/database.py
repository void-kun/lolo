from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from crawler_service.core.config import get_settings

settings = get_settings()

# Create engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    Initialize the database by creating all tables.
    """
    from crawler_service.models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # TODO: Add logging and error handling


async def drop_db():
    """
    Drop all tables in the database.
    """
    from crawler_service.models.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # TODO: Add logging and error handling


async def close_db():
    """
    Close the database engine and release all resources.
    """
    await engine.dispose()
    # TODO: Add logging
