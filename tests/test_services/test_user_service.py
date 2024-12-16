from datetime import datetime
from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from sqlalchemy import asc, desc

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ADMIN.name
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test searching users with filters
async def test_search_users_with_filters(db_session):
    # Arrange: Add users to the database
    user1 = User(
        nickname="valeria",
        email="valeria@example.com",
        role=UserRole.ADMIN,
        is_locked=False,
        created_at=datetime(2023, 1, 1, 0, 0, 0),  # Use datetime object
        hashed_password=hash_password("StrongPassword123"),
    )
    user2 = User(
        nickname="john",
        email="john@example.com",
        role=UserRole.MANAGER,
        is_locked=True,
        created_at=datetime(2023, 5, 1, 0, 0, 0),  # Use datetime object
        hashed_password=hash_password("AnotherStrongPassword123"),  # Add hashed password
    )
    db_session.add_all([user1, user2])
    await db_session.commit()

    # Act: Search for users by nickname
    filters = {"nickname": "valeria"}
    results = await UserService.search_users(db_session, filters)

    # Assert: Ensure the correct user is returned
    assert len(results) == 1
    assert results[0].nickname == "valeria"
    assert results[0].role == UserRole.ADMIN

    # Act: Search for users by role
    filters = {"role": "MANAGER"}
    results = await UserService.search_users(db_session, filters)

    # Assert: Ensure the correct user is returned
    assert len(results) == 1
    assert results[0].nickname == "john"
    assert results[0].role == UserRole.MANAGER

    # Act: Search for users with date range
    filters = {
        "created_at_start": datetime(2023, 1, 1, 0, 0, 0),  # Use datetime object
        "created_at_end": datetime(2023, 12, 31, 23, 59, 59),  # Use datetime object
    }
    results = await UserService.search_users(db_session, filters)

    # Assert: Ensure all users in the range are returned
    assert len(results) == 2

#adding test for pagination and sorting
async def test_search_users_with_pagination_and_sorting(db_session):
    # Arrange: Add users to the database
    users = [
        User(nickname=f"user{i:02d}", email=f"user{i}@example.com", role=UserRole.ADMIN, created_at=datetime(2023, 1, i, 0, 0, 0), hashed_password=hash_password("StrongPassword123"))
        for i in range(1, 21)
    ]
    db_session.add_all(users)
    await db_session.commit()

    # Act: Fetch first 10 users sorted by nickname in ascending order
    filters = {}
    results = await UserService.search_users(db_session, filters, skip=0, limit=10, sort_field="nickname", sort_direction="asc")

    # Assert: Ensure pagination and sorting work correctly
    assert len(results) == 10
    assert results[0].nickname == "user01"
    assert results[-1].nickname == "user10"