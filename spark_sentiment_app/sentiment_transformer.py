from typing import Iterator

import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import LongType, DoubleType, StructType, StructField, StringType
from transformers import pipeline


class SentimentModel:
    def __init__(self):
        self.model = pipeline("sentiment-analysis")

    def predict(self, text: str) -> int:
        return self.model.predict([text])[0]


SENTIMENT_STRUCT = StructType([
    StructField("score", DoubleType()),
    StructField("label", StringType()),
])


@pandas_udf(SENTIMENT_STRUCT, None)
def sentiment_calculate_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.DataFrame]:
    model = SentimentModel()
    for x in iterator:
        # Use that state for whole iterator.
        y = x.apply(model.predict)
        yield pd.DataFrame.from_records(y)


if __name__ == '__main__':
    print(SentimentModel().predict("i am a good"))
