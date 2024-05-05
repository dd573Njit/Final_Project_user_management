from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re
from app.models.user_model import UserRole
from app.utils.nickname_gen import generate_nickname
from typing import ClassVar
from urllib.parse import urlparse
from pydantic import BaseModel, UUID4


def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, max_length=100, example="John")
    last_name: Optional[str] = Field(None, max_length=100, example="Doe")
    bio: Optional[str] = Field(None, max_length=500, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, max_length=255, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, max_length=255, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, max_length=255, example="https://github.com/johndoe")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
    
    @validator('nickname')
    def validate_nickname(cls, v):
        if v and not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Nickname can only contain letters, numbers, underscores, and hyphens.")
        return v

    @validator('first_name')
    def validate_first_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("First name can only contain letters, spaces, hyphens, or apostrophes.")
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Last name can only contain letters, spaces, hyphens, or apostrophes.")
        return v

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is not None:
            parsed_url = urlparse(v)
            if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
                raise ValueError("Profile Picture URL must point to a valid image file (JPEG, PNG).")
        return v
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(..., example="Secure*1234")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(v) > 128:
            raise ValueError("Password must be less than 128 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        if ' ' in v:
            raise ValueError("Password must not contain spaces.")
        return v

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, max_length=255, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r'^[\w-]+$', example="john_doe123")
    first_name: Optional[str] = Field(None, max_length=100, example="John")
    last_name: Optional[str] = Field(None, max_length=100, example="Doe")
    bio: Optional[str] = Field(None, max_length=500, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, max_length=255, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] =Field(None, max_length=255, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, max_length=255, example="https://github.com/johndoe")
    role: Optional[str] = Field(None, example="AUTHENTICATED")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())    
    is_professional: Optional[bool] = Field(default=False, example=True)
    role: UserRole

class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), "nickname": generate_nickname(), "email": "john.doe@example.com",
        "first_name": "John", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "last_name": "Doe", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/john.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
        "github_profile_url": "https://github.com/johndoe"
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
    
class RoleUpdateRequest(BaseModel):
    new_role: str
    requester_id: UUID4  # ID of the admin requesting the change

class RoleUpdateResponse(BaseModel):
    message: str
    user_id: UUID4
    new_role: str
