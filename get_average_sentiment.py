import pandas as pd
from main import get_data
def get_mean(filepath, col='Compound'):
    data = pd.read_pickle(filepath)
    mean = data[col].mean()
    return mean

def main(outpath):
    means = pd.DataFrame(indexes=presidents, columns=(cities + countries))
    mean = get_mean(filepath)
    means
    means.to_pickle(outpath)


if __name__ == '__main__':
    (root, data_path, presidents, cities, countries, years, colors) = get_data()
    main(filepath=f'{data_path}{president}/{filename}.pkl', )