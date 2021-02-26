import pandas as pd
import os

def split(x):
    marker = 'Unidades por Caja'
    if marker in str(x):
        return(x.split(marker)[0])
    else:
        return(x)

def cell2list(df):
    # convert elements in column img_names to a list
    chrs_to_replace = ["[", "]", "'"]
    img_names = df['img_names']
    for c in chrs_to_replace:
        try:
            img_names = df['img_names'].map(lambda x: x.replace(c,''))
        except:
            pass
    df['img_names'] = img_names
    return(df)

def clean_description(f_path):
    # trim undesired text
    df = pd.read_csv(f_path)
    description = df['description']
    description = description.map(split)
    df['description'] = description
    return(df)
    
def main(csv_path):
    # open each file and select the description column
    csv_files = os.listdir(csv_path)
    # list only .csv files
    csv_files = [f for f in csv_files if '.csv' in f]
    # define the output file csv filename and path
    complete_csv = '00_product_list_test.csv'

    if complete_csv in csv_path:
        print(f'There is an existing file of the complete product list: {complete_csv}')
        exit()

    for f in csv_files:
        # csv file path
        f_path = os.path.join(csv_path,f)
        df = clean_description(f_path)
        df = cell2list(df)
        #df.to_csv(, mode='a', index=False, header=False)
    
    ''' 
    product_list = pd.read_csv(csv_path, header=None)
    product_list.rename(mapper=['Nombre', 'Categoria', 'Referencia', 'Descripcion', 'URL', 'Imagen'], axis=1)
    product_list.to_csv(csv_path, index=False)
    '''

csv_path = './' # only for testing, change later to ./csv_files
main(csv_path)