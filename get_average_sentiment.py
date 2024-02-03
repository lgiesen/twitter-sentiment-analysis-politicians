import json

import pandas as pd

from main import get_data

(root, data_path, presidents, cities, countries, years, colors) = get_data()

def get_mean(filepath, col='Compound'):
    data = pd.read_pickle(filepath)
    mean = data[col].mean()
    return mean

def load_mean_count(json_filename, col=None):
    try:
        with open(f'results/{json_filename}.json', 'r') as file:
            data = json.load(file)
        # data = pd.read_json(f'results/{json_filename}', typ='series')
        return data[col] if col else data
    except json.JSONDecodeError as e:
        print(f"Error reading {json_filename}: {e}")
        # Handle the error or return a default value
        return None
    except FileNotFoundError as e:
        print(f"File not found {json_filename}: {e}")
        return None

if __name__ == '__main__':
    (root, data_path, presidents, cities, countries, years, colors) = get_data()
    # means = pd.DataFrame(index=(presidents.append('All')), columns=(cities + countries + ['Total']))
    means = pd.DataFrame(index=(presidents), columns=(cities + countries))

    for president in presidents:
        for city in cities:
            mean_city = get_mean(f'{data_path}{president}-{city}.pkl')
            means.at[president, city] = mean_city
        for country in countries:
            mean_city = get_mean(f'{data_path}{president}-{country}.pkl')
            means.at[president, country] = mean_city

    means.at['All','Total'] = load_mean_count('mean_count', 'overall_mean')
    for city in cities:
        means.at['All',city] = load_mean_count(f'{city}_mean_count', 'overall_mean')
    for country in countries:
        means.at['All',country] = load_mean_count('country_mean_count')[country]
    for president in presidents:
        data = pd.read_pickle(f'{data_path}{president}.pkl')
        means.at[president, 'Total'] = data['Compound'].mean()
    
    filepath = f'results/mean_compound'
    means.to_pickle(f'{filepath}.pkl')
    means.to_csv(f'{filepath}.csv')
