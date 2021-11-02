import json
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from loguru import logger

try:
    from api.app import __version__, schemas
    from api.app.config import settings
except:
    from __init__ import __version__
    import schemas
    from config import settings

from package.recommender_model import __version__ as model_version
from package.recommender_model.predict import (
    make_recommendation_content,
    make_recommendation_country,
    make_recommendation_genre,
)
from package.recommender_model.processing.data_manager import load_dataset_main

api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )
    logger.info("health")
    return health.dict()


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict() -> Any:
    input_data = load_dataset_main()
    input_df = input_data.copy()
    s = np.random.choice(input_df.title.tolist())
    results = make_recommendation_content(s)
    # results = make_recommendation_genre(s)
    # results = make_recommendation_country(s)
    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))
    return results
