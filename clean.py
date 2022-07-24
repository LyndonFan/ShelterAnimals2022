import numpy as np
import pandas as pd

import datetime
import os
import sys

CWD = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(CWD, 'aac_shelter_outcomes.csv'), parse_dates=[
    'date_of_birth', 'datetime', 'monthyear',
])

DROP_COLUMNS = ['age_upon_outcome', 'monthyear']

df = df.drop(columns=DROP_COLUMNS)
df.to_csv(os.path.join(CWD, 'clean_data.csv'), index=False)

print("Done.")
