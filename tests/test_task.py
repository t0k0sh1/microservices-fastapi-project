import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import starlette.status

from app.database import get_session, Base
from main import app

DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async_engine = create_async_engine(DB_URL, echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_test_session():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client: AsyncClient):
    response = await async_client.post("/api/v1/tasks", json={"title": "Test title", "description": "Test description"})
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json() == {"id": 1, "title": "Test title", "description": "Test description"}
