import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "j_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        # "last_login_at": datetime.now(),
        # "created_at": datetime.now(),
        # "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@emai.com", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us", "us" * 26])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)
        
@pytest.mark.parametrize("email", ["valid@email.com"])
def test_user_base_email_valid(email, user_base_data):
    user_base_data["email"] = email
    user = UserBase(**user_base_data)
    assert user.email == email

@pytest.mark.parametrize("email", ["", "invalidemail", "invalid@email", "invalid.email", "verylong" * 32 + "@email.com"])
def test_user_base_email_invalid(email, user_base_data):
    user_base_data["email"] = email
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for first_name and last_name validation
@pytest.mark.parametrize("first_name", ["Test", "Test First", "Test-First", "Test'First"])
def test_user_base_first_name_valid(first_name, user_base_data):
    user_base_data["first_name"] = first_name
    user = UserBase(**user_base_data)
    assert user.first_name == first_name

@pytest.mark.parametrize("first_name", ["test123", "test$", "test_first", "test" * 26])
def test_user_base_first_name_invalid(first_name, user_base_data):
    user_base_data["first_name"] = first_name
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("last_name", ["Test", "Test Last", "Test-Last", "Test'Last"])
def test_user_base_last_name_valid(last_name, user_base_data):
    user_base_data["last_name"] = last_name
    user = UserBase(**user_base_data)
    assert user.last_name == last_name

@pytest.mark.parametrize("last_name", ["test123", "test$", "test_last", "test" * 26])
def test_user_base_last_name_invalid(last_name, user_base_data):
    user_base_data["last_name"] = last_name
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for bio validation
@pytest.mark.parametrize("bio", ["Bio", "Bio Test $"])
def test_user_base_bio_valid(bio, user_base_data):
    user_base_data["bio"] = bio
    user = UserBase(**user_base_data)
    assert user.bio == bio

@pytest.mark.parametrize("bio", ["Bio" * 167])
def test_user_base_bio_invalid_too_long(bio, user_base_data):
    user_base_data["bio"] = bio
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)
        
@pytest.mark.parametrize("url", ["http://valid.com/" + "a" * 255 + ".jpg", "http://valid.com/profile.jg"])
def test_user_base_url_invalid_too_long(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("url", ["http://valid.com/profile.jg"])
def test_user_base__profile_picture_url_invalid_image_extension(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Tests for UserCreate Password Validation
def test_UserCreate_valid_password(user_create_data):
    assert UserCreate(**user_create_data).password == user_create_data["password"]

def test_UserCreate_password_too_short(user_create_data):
    with pytest.raises(ValueError, match="Password must be at least 8 characters long."):
        UserCreate(**{**user_create_data, "password": "Short1!"})

def test_UserCreate_password_too_long(user_create_data):
    with pytest.raises(ValueError, match="Password must be less than 128 characters long."):
        UserCreate(**{**user_create_data, "password": "ThisIsAVeryLongPasswordThatExceeds128Characters!" * 3})

def test_UserCreate_password_no_uppercase(user_create_data):
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter."):
        UserCreate(**{**user_create_data, "password": "nouppercase123!"})

def test_UserCreate_password_no_lowercase(user_create_data):
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter."):
        UserCreate(**{**user_create_data, "password": "NOLOWERCASE123!"})

def test_UserCreate_password_no_digit(user_create_data):
    with pytest.raises(ValueError, match="Password must contain at least one digit."):
        UserCreate(**{**user_create_data, "password": "NoDigitPassword!"})

def test_UserCreate_password_no_special_character(user_create_data):
    with pytest.raises(ValueError, match="Password must contain at least one special character."):
        UserCreate(**{**user_create_data, "password": "NoSpecialCharacter123"})

def test_UserCreate_password_with_space(user_create_data):
    with pytest.raises(ValueError, match="Password must not contain spaces."):
        UserCreate(**{**user_create_data, "password": "Space Password123!"})
