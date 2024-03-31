import random
from typing import Iterator

import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import LongType


class SentimentModel:
    def __init__(self):
        pass

    def predict(self, text: str) -> int:
        return random.randint(-1, 1)


@pandas_udf(LongType(), None)
def sentiment_calculate_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    model = SentimentModel()
    for x in iterator:

        # Use that state for whole iterator.
        yield x.apply(model.predict)
