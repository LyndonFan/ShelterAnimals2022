import numpy as np
import pandas as pd

import datetime
import os
import sys

CWD = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(CWD, 'aac_shelter_outcomes.csv'), parse_dates=[
    'date_of_birth', 'datetime', 'monthyear',
])

df = df.drop(columns=['age_upon_outcome', 'monthyear'])
df['sex'] = df['sex_upon_outcome'].apply(
    lambda s: np.nan if pd.isna(s) else s.split(' ')[-1])
df['neutered'] = df['sex_upon_outcome'].apply(
    lambda s: np.nan if pd.isna(s) else ('Spayed' in s or 'Neutered' in s))

df.to_csv(os.path.join(CWD, 'clean_data.csv'), index=False)

print("Done.")
