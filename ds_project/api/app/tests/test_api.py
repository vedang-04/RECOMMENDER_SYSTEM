import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_predictions(client: TestClient, test_data: pd.DataFrame) -> None:
    payload = {"inputs": test_data.replace({np.NaN: None}).to_dict(orient="records")}
    response = client.post("http://localhost:8001/api/v1/predict", json=payload)
    assert response.status_code == 200
    predictions = response.json()
    print(predictions["predictions"])
    assert predictions["predictions"]
    assert predictions["errors"] is None
