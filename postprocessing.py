import pandas as pd
import os

csv_path = './' # only for testing, change later to ./csv_files

def split(x):
    marker = 'Unidades por Caja'
    if marker in x:
        return(x.split(marker)[0])
    else:
        return(x)

# open each file and select the description column
csv_files = os.listdir(csv_path)
# list only .csv files
csv_files = [f for f in csv_files if '.csv' in f]

# trim undesired text
for f in csv_files:
    f_path = os.path.join(csv_path,f)
    df = pd.read_csv(f)
    description = df['description']
    description = description.apply(split())
    df['description'] = description
    pd.to_csv(f_path)



# replace original column with clean column