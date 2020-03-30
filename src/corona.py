# Libraries
from pathlib import Path  # Path manipulation
import os  # System functions
import json  # Library for working with .json files
import pandas as pd  # Dataframe Library
import numpy as np  # Vector-Matrix Manipulation Library
from tqdm import tqdm  # Progress bar library
import re  # Regular expresion Library
import matplotlib.pyplot as plt  # Graph making library
from matplotlib import style  # Style Library for matplotlib graphs

# Variables

data_folder = Path("../data")
folders = [data_folder / x / x for x in os.listdir(data_folder) if "." not in x]

# Functions

def save_incubation_times(filename, incubation_times):
    with open(filename, 'w') as f:
        f.write(str(len(incubation_times)) + '\n')
        for i in incubation_times:
            f.write(str(i) + '\n')


# Execution

docs = []
for folder in folders:
    for file in tqdm(os.listdir(folder)):

        file_path = folder / file
        j = json.load(open(file_path, "rb"))

        title = j['metadata']['title']

        try:
            abstract = j['abstract'][0]
        except IndexError:
            abstract = ""

        full_text = ""

        for text in j['body_text']:
            full_text += text['text'] + '\n\n'

        docs.append([title, abstract, full_text])

df = pd.DataFrame(docs, columns=['title', 'abstract', 'full_text'])

incubation = df[df['full_text'].str.contains('incubation')]
print(incubation.head())

texts = incubation['full_text'].values

incubation_times = []

for t in texts:
    for sentence in t.split(". "):
        if "incubation" in sentence and 'day' in sentence:
            single_day = re.findall(r" (?:\d{1,2}[.])?\d{1,2} [D,d]ay", sentence)
            # single_day = re.findall(r" \d{1,2} [D,d]ay", sentence)

            if len(single_day) == 1:
                num = single_day[0].split(" ")
                incubation_times.append(float(num[1]))

filename = "incubation.txt"
save_incubation_times(filename, incubation_times)

print(f"The mean projected incubation time is {np.mean(incubation_times)} days")
print(f"The median projected incubation time is {np.median(incubation_times)} days")
plt.hist(incubation_times, bins=20)
plt.ylabel("bin counts")
plt.xlabel("incubation time(days)")
plt.show()
