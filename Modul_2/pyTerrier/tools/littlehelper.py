import requests
import pandas as pd
import re

from pathlib import Path


def df_from_bibsonomy_query(query, limit=1000, to_json=False, output_dir=Path('.'), output_filename=None):
    """
    Retrieves data from Bibsonomy based on a specified query and converts it into a pandas DataFrame. 

    Parameters:
    - query (str or list of str): The search term(s) to query in Bibsonomy. Can be a single string or a list of strings.
    - limit (int, optional): The maximum number of items to retrieve for each query. Defaults to 1000.
    - to_json (bool, optional): If True, the resulting DataFrame is saved as a JSON file. Defaults to False.
    - output_dir (Path, optional): The directory where the JSON file will be saved. Defaults to the current directory.
    - output_filename (str, optional): The name of the JSON file to save the results in. If not specified, a default name based on the query will be used.

    Returns:
    pandas.DataFrame: A DataFrame containing the retrieved data from Bibsonomy.

    Notes:
    - The function first validates the query format. If the query is not a string or list of strings, an error message is displayed.
    - Data from Bibsonomy is fetched for each query term, and the results are combined into a single DataFrame.
    - If 'to_json' is True, the DataFrame is saved as a JSON file in the specified directory with the given filename.
    - The function prints the number of items retrieved for each query and the file path if data is saved as JSON.
    """
    # Check datatype of query
    if not isinstance(query, list):
        if isinstance(query, str):
            query = [query]
        else:
            print('Please provide a valid query (string or list of strings).')
            
    # Query bibsonomy
    dfs = []
    for q in query:
        url = f"https://www.bibsonomy.org/json/search/{q.replace(' ', '%20')}?duplicates=merged&items={limit}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['items'])
            df['search_string'] = q
            print(f"Query: '{q}'. Number of items retrieved: {len(df)}")
            dfs.append(df)
        else:
            print(f'{response.status_code}: {url} is not available.')
            
    # Concat DataFrames
    df = pd.concat(dfs, ignore_index=True)
    
    # If to_json == True save df as .json 
    if to_json == True:
        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir(parents=True)
        if output_filename is not None:
            if not output_filename.endswith('.json'):
                output_filename = Path(f"{output_dir}/{output_filename.replace(' ', '_').lower()}.json")
            else:
                output_filename = output_dir.joinpath(output_filename.replace(' ', '_').lower())
        else:
            output_filename = output_dir.joinpath(f'bibsonomy_{query[0]}.json')
        df.to_json(output_filename, orient='records')
        print(f'\nSaved data to "{output_filename}"')
        
    return df
