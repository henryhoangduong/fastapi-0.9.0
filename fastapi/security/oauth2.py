from typing import Optional

from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.params import Form
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class OAuth2PasswordRequestForm:
    def __init__(self,
                 grant_type: str = Form(None, regex="password"),
                 username: str = Form(...),
                 password: str = Form(...),
                 scope: str = Form(""),
                 client_id: Optional[str] = Form(None),
                 client_secret: Optional[str] = Form(None),):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class OAuth2PasswordRequestFormStrict(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(..., regex="password"),
        username: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )


class OAuth2(SecurityBase):
    def __init__(
        self, *, flows: OAuthFlowsModel = OAuthFlowsModel(), scheme_name: str = None
    ):
        self.model = OAuth2Model(flows=flows)
        self.scheme_name = scheme_name or self.__class__.__name__

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return authorization


class OAuth2PasswordBearer(OAuth2):
    def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name)

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return param
