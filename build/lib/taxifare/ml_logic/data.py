from taxifare.ml_logic.params import (COLUMN_NAMES_RAW,
                                            DTYPES_RAW_OPTIMIZED,
                                            DTYPES_RAW_OPTIMIZED_HEADLESS,
                                            DTYPES_PROCESSED_OPTIMIZED
                                            )

import os
import pandas as pd
from taxifare.ml_logic.utils import simple_time_and_memory_tracker

@simple_time_and_memory_tracker
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns
    # remove redundant columns or rows
    df = df.drop(columns=['key'])
    df = df.drop_duplicates()
    df = df.dropna(how='any', axis=0)


    # remove buggy transactions
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0) | (df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
    df = df[df.passenger_count > 0]
    df = df[df.fare_amount > 0]

    # remove irrelevant/non-representative transactions (rows) for a training set
    df = df[df["pickup_latitude"].between(left=40.5, right=40.9)]
    df = df[df["dropoff_latitude"].between(left=40.5, right=40.9)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-73.7)]
    df = df[df["dropoff_longitude"].between(left=-74.3, right=-73.7)]

    df = df[df.fare_amount < 400]
    df = df[df.passenger_count < 8]

    print("\n✅ data cleaned")

    return df
