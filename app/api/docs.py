# https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/#self-hosting-javascript-and-css-for-docs

from fastapi import APIRouter, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request):
    return get_swagger_ui_html(
        openapi_url=req.app.openapi_url,
        title=req.app.title + " - Swagger UI",
        oauth2_redirect_url=req.app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@router.get("/redoc", include_in_schema=False)
async def redoc_html(req: Request):
    return get_redoc_html(
        openapi_url=req.app.openapi_url,
        title=req.app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()
