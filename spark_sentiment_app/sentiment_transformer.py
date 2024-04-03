from typing import Iterator

import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import LongType ,DoubleType
from transformers import pipeline


class SentimentModel:
    def __init__(self):
        self.model = pipeline("sentiment-analysis")

    def predict(self, text: str) -> int:
        return self.model.predict([text])[0]["score"]


@pandas_udf(DoubleType(), None)
def sentiment_calculate_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    model = SentimentModel()
    for x in iterator:
        # Use that state for whole iterator.
        yield x.apply(model.predict)
