import binascii
from base64 import b64decode
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.openapi.models import (
    HTTPBase as HTTPBaseModel,
    HTTPBearer as HTTPBearerModel,
)
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param


class HTTPBasicCredentials(BaseModel):
    username: str
    password: str


class HTTPAuthorizationCredentials(BaseModel):
    sheme: str
    credentials: str


class HTTPBase(SecurityBase):
    def __init__(self, *, scheme: str, scheme_name: str = None):
        self.model = HTTPBaseModel(scheme=scheme)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)

