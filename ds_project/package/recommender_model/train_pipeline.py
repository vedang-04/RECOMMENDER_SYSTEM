import joblib
import numpy as np
import pandas as pd
from processing.data_manager import (
    create_dataset_movies_on_netflix,
    create_dataset_shows_on_netflix,
    load_dataset_main,
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from package.recommender_model import __version__ as _version
from package.recommender_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


def run_training() -> None:
    df = load_dataset_main()
    df.description = df.description.str.lower()
    df.description = df.description.replace("[\W]+", " ", regex=True)
    tv = TfidfVectorizer(lowercase=True, stop_words="english")
    tvdf = df.description.to_frame("description")
    tv.fit(tvdf.description.tolist())
    stvdf = pd.DataFrame(
        tv.transform(tvdf.description.tolist()).toarray(),
        columns=tv.get_feature_names(),
        index=df.title,
    )
    nn = NearestNeighbors(n_neighbors=11, metric="cosine", n_jobs=-1, p=2)
    nn.fit(stvdf.values)
    dist, ind = nn.kneighbors(X=stvdf.values, n_neighbors=11)
    ind_csv = pd.DataFrame(ind)
    load_file = "ind_csv.csv"
    load_path = DATASET_DIR / load_file
    ind_csv.to_csv(load_path)

    from package.recommender_model.predict import (
        make_recommendation_content,
        make_recommendation_country,
        make_recommendation_genre,
    )

    print(make_recommendation_content("Gol Maal"))
    print(make_recommendation_genre("Gol Maal"))
    print(make_recommendation_country("Gol Maal"))


if __name__ == "__main__":
    run_training()
