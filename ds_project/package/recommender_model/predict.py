import typing as t

import numpy as np
import pandas as pd

from package.recommender_model import __version__ as _version
from package.recommender_model.config.core import DATASET_DIR, config
from package.recommender_model.processing.data_manager import (
    create_dataset_movies_on_netflix,
    create_dataset_shows_on_netflix,
    load_dataset_main,
)


def make_recommendation_content(movie: str) -> dict:
    df = load_dataset_main()
    movies_on_netflix = create_dataset_movies_on_netflix()
    shows_on_netflix = create_dataset_shows_on_netflix()
    d = {}
    d["top_movies"] = (
        movies_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    d["top_shows"] = (
        shows_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    mdf = df[df.title == movie]
    if len(mdf) == 0:
        results = {
            "predictions": {
                "Top-rated movies": d.get("top_movies"),
                "Top-rated shows": d.get("top_shows"),
            },
            "version": _version,
            "errors": None,
        }
    else:
        load_file = "ind_csv.csv"
        load_path = DATASET_DIR / load_file
        ind = pd.read_csv(load_path)
        ind = ind[
            ind.columns[1:]
        ]  # Check ind dataframe first before running this step.
        ind = np.array(ind)
        m = mdf.index[0]
        j = 0
        pred = []
        while j < len(ind[m]):
            if j == 0:
                pass
            else:
                pred.append(df.title.iloc[ind[m][j]])
            j = j + 1
        results = {
            "predictions": {"Top 10 recommendations": pred},
            "version": _version,
            "errors": None,
        }
    return results


def make_recommendation_genre(movie: str) -> dict:
    movies_on_netflix = create_dataset_movies_on_netflix()
    shows_on_netflix = create_dataset_shows_on_netflix()
    d = {}
    d["top_movies"] = (
        movies_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    d["top_shows"] = (
        shows_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    dm = {}
    for x in movies_on_netflix.genre.unique():
        dm[x] = (
            movies_on_netflix.groupby(["genre", "title"])["weighted_average_vote"]
            .max()
            .reset_index()
            .groupby("genre")
            .get_group(x)
            .sort_values(by="weighted_average_vote", ascending=False)
            .iloc[:10]
            .title.tolist()
        )
    ds = {}
    for x in shows_on_netflix.genre.unique():
        ds[x] = (
            shows_on_netflix.groupby(["genre", "title"])["weighted_average_vote"]
            .max()
            .reset_index()
            .groupby("genre")
            .get_group(x)
            .sort_values(by="weighted_average_vote", ascending=False)
            .iloc[:10]
            .title.tolist()
        )
    gbm = {}
    if movie in shows_on_netflix.title.tolist():
        for x in (
            shows_on_netflix[shows_on_netflix.title == movie]
            .genre.drop_duplicates()
            .to_list()
        ):
            if movie in ds.get(x):
                l = ds.get(x)
                l.remove(movie)
                gbm[x] = l
            else:
                gbm[x] = ds.get(x)
        results = {
            "predictions": gbm,
            "version": _version,
            "errors": None,
        }
        return results
    elif movie in movies_on_netflix.title.tolist():
        for x in (
            movies_on_netflix[movies_on_netflix.title == movie]
            .genre.drop_duplicates()
            .to_list()
        ):
            if movie in dm.get(x):
                l = dm.get(x)
                l.remove(movie)
                gbm[x] = l
            else:
                gbm[x] = dm.get(x)
        results = {
            "predictions": gbm,
            "version": _version,
            "errors": None,
        }
        return results
    else:
        results = {
            "predictions": {
                "Top-rated movies": d.get("top_movies"),
                "Top-rated shows": d.get("top_shows"),
            },
            "version": _version,
            "errors": None,
        }
        return results


def make_recommendation_country(movie):
    movies_on_netflix = create_dataset_movies_on_netflix()
    shows_on_netflix = create_dataset_shows_on_netflix()
    d = {}
    d["top_movies"] = (
        movies_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    d["top_shows"] = (
        shows_on_netflix.sort_values(by="weighted_average_vote", ascending=False)
        .title.drop_duplicates()
        .iloc[:10]
        .tolist()
    )
    dcs = {}
    for x in shows_on_netflix.country.dropna().unique():
        dcs[x] = (
            shows_on_netflix.groupby(["country", "title"])["weighted_average_vote"]
            .max()
            .reset_index()
            .groupby("country")
            .get_group(x)
            .sort_values(by="weighted_average_vote", ascending=False)
            .iloc[:10]
            .title.tolist()
        )
    dcm = {}
    for x in movies_on_netflix.country.dropna().unique():
        dcm[x] = (
            movies_on_netflix.groupby(["country", "title"])["weighted_average_vote"]
            .max()
            .reset_index()
            .groupby("country")
            .get_group(x)
            .sort_values(by="weighted_average_vote", ascending=False)
            .iloc[:10]
            .title.tolist()
        )
    gbc = {}
    if movie in shows_on_netflix.title.tolist():
        for x in (
            shows_on_netflix[shows_on_netflix.title == movie]
            .country.drop_duplicates()
            .to_list()
        ):
            if movie in dcs.get(x):
                l = dcs.get(x)
                l.remove(movie)
                gbc[x] = l
            else:
                gbc[x] = dcs.get(x)
        results = {
            "predictions": gbc,
            "version": _version,
            "errors": None,
        }
        return results
    elif movie in movies_on_netflix.title.tolist():
        for x in (
            movies_on_netflix[movies_on_netflix.title == movie]
            .country.drop_duplicates()
            .to_list()
        ):
            if movie in dcm.get(x):
                l = dcm.get(x)
                l.remove(movie)
                gbc[x] = l
            else:
                gbc[x] = dcm.get(x)
        results = {
            "predictions": gbc,
            "version": _version,
            "errors": None,
        }
        return results
    else:
        results = {
            "predictions": {
                "Top-rated movies": d.get("top_movies"),
                "Top-rated shows": d.get("top_shows"),
            },
            "version": _version,
            "errors": None,
        }
        return results
