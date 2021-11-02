import numpy as np
import pandas as pd

from package.recommender_model.config.core import DATASET_DIR, config


def load_dataset_main() -> pd.DataFrame:
    load_file = f"{config.app_config.file_1}.csv"
    load_path = DATASET_DIR / load_file
    df = pd.read_csv(load_path)
    df = df[df.columns[1:]].drop_duplicates().reset_index(drop=True)
    df = df.reset_index(drop=False).rename(columns={"index": "show_id"})
    df.show_id = df.show_id + 1
    df.show_id = "s" + df.show_id.astype("string")
    df.date_added = pd.to_datetime(df.date_added)
    df["add_year"] = df.date_added.dt.year
    df["add_month"] = df.date_added.dt.month
    df["add_day"] = df.date_added.dt.day
    df = df.drop("date_added", axis=1)
    df.release_year.loc[7109] = 2010
    df.release_year.loc[5658] = 2015
    df.release_year.loc[4845] = 2003
    df.release_year.loc[3168] = 2016
    df.release_year.loc[3433] = 2018
    df.release_year.loc[7060] = 2018
    df.release_year.loc[3287] = 2019
    df.release_year.loc[2920] = 2020
    df.release_year.loc[4844] = 2015
    df.release_year.loc[1551] = 2018
    df.release_year.loc[1696] = 2018
    df.release_year.loc[5394] = 2016
    df.release_year.loc[5677] = 2016
    df.release_year.loc[3369] = 2014
    df["time_bw_add_release"] = df.add_year - df.release_year
    l1 = df[df.duration.isnull() == True].index
    df.duration = df.duration.replace(np.NaN, "t", regex=False)
    for x in l1:
        df.duration.loc[x] = df.loc[x].rating
        df.rating.loc[x] = np.NaN
    for x in df.columns[1:6]:
        df[x] = df[x].str.strip()
    for x in df.columns[8:11]:
        df[x] = df[x].str.strip()
    return df


def load_dataset_sub() -> pd.DataFrame:
    load_file_1 = f"{config.app_config.file_2}.csv"
    load_path_1 = DATASET_DIR / load_file_1
    df1 = pd.read_csv(load_path_1)
    load_file_2 = f"{config.app_config.file_3}.csv"
    load_path_2 = DATASET_DIR / load_file_2
    df2 = pd.read_csv(load_path_2)
    for x in df1.columns[:6]:
        df1[x] = df1[x].str.strip()
    for x in df1.columns[7:14]:
        df1[x] = df1[x].str.strip()
    for x in df1.columns[16:19]:
        df1[x] = df1[x].str.strip()
    for x in df2.columns[0:1]:
        df2[x] = df2[x].str.strip()
    df3 = (
        pd.merge(
            df1[["imdb_title_id", "title", "year", "genre"]],
            df2[["imdb_title_id", "weighted_average_vote"]],
            on="imdb_title_id",
        )
            .drop_duplicates()
            .drop("imdb_title_id", axis=1)
    )
    df = load_dataset_main()
    mer = pd.merge(df, df3, how="left", on=["title"])
    mer["weighted_average_vote"] = mer["weighted_average_vote"].replace(
        np.NaN, 0, regex=False
    )
    return mer


def create_dataset_movies_on_netflix() -> pd.DataFrame:
    mer = load_dataset_sub()
    mer_nm = mer.groupby("type").get_group("Movie")
    mer_nm = pd.merge(
        mer_nm,
        mer_nm.country.dropna().str.strip().str.split(",").explode().str.strip(),
        how="left",
        left_index=True,
        right_index=True,
    )
    mer_nm.country_x = mer_nm.country_y
    mer_nm = mer_nm.rename(columns={"country_x": "country"})
    mer_nm = mer_nm.drop("country_y", axis=1)
    mer_nm = mer_nm[mer_nm.country != ""]
    mer_nm = mer_nm.reset_index(drop=True)
    mer_nm.genre = mer_nm.genre.replace(np.NaN, "", regex=False)
    mer_nm["tg"] = mer_nm["listed_in"] + ", " + mer_nm["genre"]
    stg = (
        mer_nm.tg.str.strip()
            .str.split(",")
            .explode()
            .str.strip()
            .str.split("&")
            .explode()
            .str.strip()
            .str.strip()
            .str.split(" ")
            .apply(lambda x: x[0])
    )
    stg = stg.replace(
        {
            "Comedies": "Comedy",
            "Dramas": "Drama",
            "Romantic": "Romance",
            "Thrillers": "Thriller",
            "Sports": "Sport",
            "Musicals": "Musical",
            "Music": "Musical",
        }
    )
    stg = stg[stg != ""]
    stg = stg.to_frame("g")
    stg = (
        stg.reset_index()
            .rename(columns={"index": "gpb"})
            .groupby(["gpb", "g"])
            .count()
            .reset_index()
            .set_index("gpb")
    )
    stg = (
        stg.reset_index()
            .groupby("gpb")
            .agg(lambda x: x.tolist())
            .g.apply(lambda x: ",".join(x))
            .to_frame("g")
    )
    stg = pd.merge(
        stg,
        stg.g.str.strip().str.split(",").explode(),
        how="left",
        left_index=True,
        right_index=True,
    ).rename(columns={"g_x": "cg", "g_y": "g"})
    mer_nm = pd.merge(mer_nm, stg, left_index=True, right_index=True, how="left")
    mer_nm = mer_nm.reset_index(drop=True)
    mer_nm = mer_nm.drop(["listed_in", "genre", "tg"], axis=1)
    mer_nm = mer_nm.rename(columns={"g": "genre", "cg": "combined_genre"})
    mer_nm.duration = mer_nm.duration.apply(lambda x: float(x.strip().split(" ")[0]))
    mer_nm = mer_nm.reset_index(drop=True)
    movies_on_netflix = mer_nm[
        [
            "title",
            "director",
            "cast",
            "country",
            "release_year",
            "duration",
            "rating",
            "add_year",
            "weighted_average_vote",
            "combined_genre",
            "genre",
            "description",
        ]
    ]
    return movies_on_netflix


def create_dataset_shows_on_netflix() -> pd.DataFrame:
    mer = load_dataset_sub()
    mer_ns = mer.groupby("type").get_group("TV Show")
    mer_ns = pd.merge(
        mer_ns,
        mer_ns.country.dropna().str.strip().str.split(",").explode().str.strip(),
        how="left",
        left_index=True,
        right_index=True,
    )
    mer_ns.country_x = mer_ns.country_y
    mer_ns = mer_ns.rename(columns={"country_x": "country"})
    mer_ns = mer_ns.drop("country_y", axis=1)
    mer_ns = mer_ns[mer_ns.country != ""]
    mer_ns = mer_ns.reset_index(drop=True)
    mer_ns.genre = mer_ns.genre.replace(np.NaN, "", regex=False)
    mer_ns["tgs"] = mer_ns["listed_in"] + ", " + mer_ns["genre"]
    stgs = (
        mer_ns.tgs.str.strip()
            .str.split(",")
            .explode()
            .str.strip()
            .str.split("&")
            .explode()
            .str.strip()
    )
    stgs = stgs.replace(
        {
            "Comedy": "TV Comedies",
            "Drama": "TV Dramas",
            "Romance": "Romantic TV Shows",
            "Action": "TV Action",
            "Horror": "TV Horror",
            "Music": "Musical Shows",
            "Musical": "Musical Shows",
            "Crime": "Crime TV Shows",
            "Spanish-Language TV Shows": "Spanish TV Shows",
            "Mystery": "TV Mysteries",
            "Thriller": "TV Thrillers",
            "Cult": "Cult TV",
            "Nature": "Nature TV",
            "Sci-Fi": "TV Sci-Fi",
            "Adventure": "TV Adventures",
            "Classic": "Classic TV",
            "Fantasy": "TV Fantasies",
            "War": "War Shows",
            "Biography": "Biography Shows",
            "Western": "Western Shows",
            "Family": "Family Shows",
            "History": "History TV",
            "Animation": "Animated Shows",
        }
    )
    stgs = stgs[stgs != ""]
    stgs = stgs.to_frame("g")
    stgs = (
        stgs.reset_index()
            .rename(columns={"index": "gpb"})
            .groupby(["gpb", "g"])
            .count()
            .reset_index()
            .set_index("gpb")
    )
    stgs = (
        stgs.reset_index()
            .groupby("gpb")
            .agg(lambda x: x.tolist())
            .g.apply(lambda x: ",".join(x))
            .to_frame("g")
    )
    stgs = pd.merge(
        stgs,
        stgs.g.str.strip().str.split(",").explode(),
        how="left",
        left_index=True,
        right_index=True,
    ).rename(columns={"g_x": "cg", "g_y": "g"})
    mer_ns = pd.merge(mer_ns, stgs, left_index=True, right_index=True, how="left")
    mer_ns = mer_ns.reset_index(drop=True)
    mer_ns = mer_ns.drop(["listed_in", "genre", "tgs"], axis=1)
    mer_ns = mer_ns.rename(columns={"g": "genre", "cg": "combined_genre"})
    mer_ns.groupby(["combined_genre", "country"])[
        "weighted_average_vote"
    ].max().reset_index().sort_values(
        by="weighted_average_vote", ascending=False
    ).reset_index().rename(
        columns={"index": "title"}
    )
    mer_ns.duration = mer_ns.duration.apply(lambda x: int(x.strip().split(" ")[0]))
    mer_ns = mer_ns.reset_index(drop=True)
    shows_on_netflix = mer_ns[
        [
            "title",
            "director",
            "cast",
            "country",
            "release_year",
            "duration",
            "rating",
            "add_year",
            "weighted_average_vote",
            "combined_genre",
            "genre",
            "description",
        ]
    ]
    return shows_on_netflix
