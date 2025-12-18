import asyncio
import inspect
import logging
from typing import Any, Callable, List, Optional, Type

from fastapi import params
from fastapi.dependencies.models import Dependant
from pydantic import BaseModel, Schema
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.fields import Field
from pydantic.utils import lenient_issubclass
from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import compile_path, get_name, request_response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.encoders import jsonable_encoder


def serialize_response(*, field: Field = None, response: Response) -> Any:
    encoded = jsonable_encoder(response)
    if field:
        errors = []
        value, errors_ = field.validate(encoded, {}, loc=("response",))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        if errors:
            raise ValidationError(errors)
        return jsonable_encoder(value)
    else:
        return encoded
