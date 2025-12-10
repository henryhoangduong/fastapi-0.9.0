from typing import Optional

from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.params import Form
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

