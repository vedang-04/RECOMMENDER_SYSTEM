import os
from typing import Any

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

try:
    from api.app.api import api_router
    from api.app.config import settings
except:
    from config import settings

    from api import api_router
from package.recommender_model.predict import make_recommendation_content, make_recommendation_genre, \
    make_recommendation_country


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    templates = Jinja2Templates(directory=os.getcwd() + r"\api\app\templates")

    root_router = APIRouter()

    @root_router.get("/")
    def index() -> Any:
        """Basic HTML response."""
        body = (
            "<html>"
            "<body style='padding: 10px;'>"
            "<h1>Welcome to the API</h1>"
            "<div>"
            "Check the docs: <a href='/docs'>here</a>"
            "</div>"
            "</body>"
            "</html>"
        )
        return HTMLResponse(content=body)

    @root_router.get("/recommendersystem", response_class=HTMLResponse)
    def form_post_get(
            request: Request,
    ):
        result = "Enter Content"
        return templates.TemplateResponse(
            "ds_project.html", context={"request": request, "result": result}
        )

    @root_router.post("/recommendersystem")
    async def form_post(request: Request, assignment_file: str = Form(...)):
        try:
            logger.info(assignment_file)
            content_to_be_read = str(assignment_file)
            prediction = make_recommendation_content(content_to_be_read)
            prediction1 = make_recommendation_genre(content_to_be_read)
            prediction2 = make_recommendation_country(content_to_be_read)
            d=prediction['predictions']
            d.update(prediction1['predictions'])
            d.update(prediction2['predictions'])
            result = d

            return templates.TemplateResponse(
                "ds_project.html", context={"request": request, "result": result}
            )
        except Exception as e:
            logger.info("HERE")
            logger.info(e)
            result = "Enter Content"
            return templates.TemplateResponse(
                "ds_project.html", context={"request": request, "result": result}
            )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(root_router)
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.add_route("/", index)
    app.add_route("/recommendersystem", form_post_get)
    app.add_route("/recommendersystem", form_post)
    logger.info("Application instance created")
    return app
