from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from package.recommender_model.processing.data_manager import load_dataset_main


@pytest.fixture(scope="module")
def test_data() -> pd.DataFrame:
    return load_dataset_main()


@pytest.fixture()
def client() -> Generator:
    from app.application import app

    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
