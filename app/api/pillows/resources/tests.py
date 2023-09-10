import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from service import create_pillow_with_history

@pytest.mark.asyncio
async def test_create_pillow_with_history():
    # Mock the AsyncSession
    db = AsyncMock(spec=AsyncSession)

    # Test when user_id and uuid are None
    result = await create_pillow_with_history(db, 10, None, None)
    assert result == -1

    # Test when user_id is provided and pillow exists
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=AsyncMock(num_pillows=5))))
    result = await create_pillow_with_history(db, 10, 1, None)
    assert result == 0

    # Test when user_id is provided and pillow does not exist
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
    result = await create_pillow_with_history(db, 10, 1, None)
    assert result == 0

    # Test when uuid is provided and pillow exists
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=AsyncMock(num_pillows=5))))
    result = await create_pillow_with_history(db, 10, None, '123e4567-e89b-12d3-a456-426614174000')
    assert result == 0

    # Test when uuid is provided and pillow does not exist
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
    result = await create_pillow_with_history(db, 10, None, '123e4567-e89b-12d3-a456-426614174000')
    assert result == 0

    # Test when amount is negative and pillow exists
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=AsyncMock(num_pillows=5))))
    result = await create_pillow_with_history(db, -10, 1, None)
    assert result == -2

    # Test when amount is negative and pillow does not exist
    db.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
    result = await create_pillow_with_history(db, -10, 1, None)
    assert result == -2
