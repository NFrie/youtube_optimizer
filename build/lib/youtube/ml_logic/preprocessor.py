# from sklearn.pipeline import make_pipeline
# from sklearn.compose import ColumnTransformer, make_column_transformer
# from sklearn.preprocessing import OneHotEncoder, FunctionTransformer

# from taxifare.ml_logic.encoders import (transform_time_features,
#                                               transform_lonlat_features,
#                                               compute_geohash)

import numpy as np
import pandas as pd

# from colorama import Fore, Style
from taxifare.ml_logic.utils import simple_time_and_memory_tracker

from youtube.ml_logic.preprocessing import (drop_duplicate_ids,strip_english,preprocessing,drop_y_nas)
from youtube.ml_logic.pull import pull_images

from youtube.ml_logic.params import (
    # CHUNK_SIZE,
    # DTYPES_RAW_OPTIMIZED_HEADLESS,
    # DTYPES_RAW_OPTIMIZED,
    # DTYPES_PROCESSED_OPTIMIZED,
    # COLUMN_NAMES_RAW,
    DATASET,
    # VALIDATION_DATASET_SIZE,
    BUCKET_NAME)

@simple_time_and_memory_tracker
def preprocess_features():

    df = pd.read_csv(f"../../raw_data/{DATASET}")

    print(f'Length of original df = {len(df)}')

    df = drop_duplicate_ids(df)
    print(f'Length without duplicate ids = {len(df)}')

    df = strip_english(df)
    print(f'Length with only english = {len(df)}')

    df['title'] = df['title'].apply(lambda x: preprocessing(x))

    df = drop_y_nas(df)

    assert df.views.isna().sum() == 0

    df = df.sort_values('id')

    df["get"] =  + df["id"] +'_'+ df["views"].astype(int).astype(str)

    videos_to_pick = set(df['get'])

    images, ids = pull_images(BUCKET_NAME,DATASET,videos_to_pick)

    assert len(ids) == len(images)

    df= df[df['id'].isin(ids)]

    assert list(df.id) == ids



    return df, images


    # def create_sklearn_preprocessor() -> ColumnTransformer:
    #     """
    #     Create a scikit-learn preprocessor
    #     that transforms a cleaned dataset of shape (_, 7)
    #     into a preprocessed one of different fixed shape (_, 65)
    #     """
    #     # PASSENGER PIPE
    #     p_min = 1
    #     p_max = 8
    #     passenger_pipe = FunctionTransformer(lambda p: (p - p_min) / (p_max - p_min))

    #     # DISTANCE PIPE
    #     dist_min = 0
    #     dist_max = 100

    #     distance_pipe = make_pipeline(
    #         FunctionTransformer(transform_lonlat_features),
    #         FunctionTransformer(lambda dist: (dist - dist_min) / (dist_max - dist_min))
    #     )

    #     # TIME PIPE
    #     year_min = 2009
    #     year_max = 2019

    #     time_categories = {
    #         0: np.arange(0, 7, 1),  # days of the week
    #         1: np.arange(1, 13, 1)  # months of the year
    #     }

    #     time_pipe = make_pipeline(
    #         FunctionTransformer(transform_time_features),
    #         make_column_transformer(
    #             (OneHotEncoder(
    #                 categories=time_categories,
    #                 sparse=False,
    #                 handle_unknown="ignore"
    #             ), [2,3]), # corresponds to columns ["day of week", "month"], not the other columns

    #             (FunctionTransformer(lambda year: (year - year_min) / (year_max - year_min)), [4]), # min-max scale the columns 4 ["year"]
    #             remainder="passthrough" # keep hour_sin and hour_cos
    #             )
    #         )

    #     # GEOHASH PIPE
    #     lonlat_features = [
    #         "pickup_latitude", "pickup_longitude", "dropoff_latitude",
    #         "dropoff_longitude"
    #     ]

    #     # Below are the 20 most frequent district geohashes of precision 5,
    #     # covering about 99% of all dropoff/pickup locations,
    #     # according to prior analysis in a separate notebook
    #     most_important_geohash_districts = [
    #         "dr5ru", "dr5rs", "dr5rv", "dr72h", "dr72j", "dr5re", "dr5rk",
    #         "dr5rz", "dr5ry", "dr5rt", "dr5rg", "dr5x1", "dr5x0", "dr72m",
    #         "dr5rm", "dr5rx", "dr5x2", "dr5rw", "dr5rh", "dr5x8"
    #     ]

    #     geohash_categories = {
    #         0: most_important_geohash_districts,  # pickup district list
    #         1: most_important_geohash_districts  # dropoff district list
    #     }

    #     geohash_pipe = make_pipeline(
    #         FunctionTransformer(compute_geohash),
    #         OneHotEncoder(
    #             categories=geohash_categories,
    #             handle_unknown="ignore",
    #             sparse=False
    #         )
    #     )

    #     # COMBINED PREPROCESSOR
    #     final_preprocessor = ColumnTransformer(
    #         [
    #             ("passenger_scaler", passenger_pipe, ["passenger_count"]),
    #             ("time_preproc", time_pipe, ["pickup_datetime"]),
    #             ("dist_preproc", distance_pipe, lonlat_features),
    #             ("geohash", geohash_pipe, lonlat_features),
    #         ],
    #         n_jobs=-1,
    #     )

    #     return final_preprocessor


    # print(Fore.BLUE + "\nPreprocess features..." + Style.RESET_ALL)

    # preprocessor = create_sklearn_preprocessor()

    # X_processed = preprocessor.fit_transform(X)

    # print("\n✅ X_processed, with shape", X_processed.shape)

    # return X_processed
