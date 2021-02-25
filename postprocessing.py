import pandas as pd
import os

csv_path = './' # only for testing, change later to ./csv_files

# open each file and select the description column
csv_files = os.listdir(csv_path)
# list only .csv files
csv_files = [f for f in csv_files if '.csv' in f]

# trim undesired text
for f in csv_files:
    df = pd.read_csv(f)
    description = df['description']
    description = description.apply(lambda x: x.split('Unidades por Caja')[0])
    df['description'] = description
    save_path = os.path.join(csv_path, f)
    df.to_csv(save_path, index=False)

# replace original column with clean column