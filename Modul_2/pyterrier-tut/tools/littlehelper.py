import requests
import pandas as pd

def df_from_bibsonomy_query(query, limit=1000):
    """
    Create a DataFrame by querying BibSonomy for specific search terms.

    Args:
        query (str or list of str): The search query or a list of search queries to retrieve data for.
        limit (int, optional): The maximum number of items to retrieve for each query. Defaults to 1000.

    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved data from BibSonomy, with an additional 'search_string' column
        that indicates the corresponding search query for each row.
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
    return df
