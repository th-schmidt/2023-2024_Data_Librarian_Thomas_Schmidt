#learn more about streamlit: https://docs.streamlit.io/

import streamlit as st
import pyterrier as pt
import pandas as pd
import pickle
import os

os.environ["JAVA_HOME"] = "./jdk/Contents/Home/" # Set JAVA env variable


if not pt.started():
    pt.init()

def init():
    index = pt.IndexFactory.of("./makerspace_index_mult/data.properties")
    st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
    st.session_state["data"] = pickle.load(open("./bibsonomy_clean_data/makerspace_vr.pkl", "rb"))
    st.session_state["lexicon"] = index.getLexicon()


def print_results(entries):
    result_num = 1
    fields_to_show = ['text', 'year', 'author', 'url', 'abstract', 'tags']
    if len(entries) >= 1:
        for entry in entries:
            st.write(f'Result **{result_num}** of **{len(entries)}**')
            
            for field in fields_to_show:
                if field == "text":
                    st.title(entry[0][field])
                elif field == 'author' or field == 'tags':
                    if isinstance(entry[0][field], list):
                        st.write(f"**{field.capitalize()}:** \t {', '.join(entry[0][field]).strip()}")
                    else:
                        st.write(f"{field.capitalize()}: \t {entry[0][field]}")
                elif field == 'url':
                    if len(entry[0][field]) <= 1:
                        st.write(f"**{field.upper()}:** \t {entry[0]['docno']}")
                    else:
                        st.write(f"**{field.upper()}:** \t {entry[0][field]}")
                else:
                    st.write(f"**{field.capitalize()}:** \t {entry[0][field]}")
            st.write(f"**:blue[Score: {entry[1]}]**")
            st.divider()
            result_num += 1
    else:
        st.write(f'No entries found.')
        st.write(f'Please adjust your search criteria. :pray:')


def search(query, search_limit, year_range, abstract_flag, url_flag):
    res = st.session_state["engine"].search(query)[:search_limit]
    
    filtered_entries = []
    
    for _, row in res.iterrows():
        score = round(row['score'], 2)
        entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]

        if entry['year'] >= year_range[0] and entry['year'] <= year_range[1]:
            include_entry = True
            if abstract_flag:
                include_entry = include_entry and entry['abstract'] != None
            if url_flag:
                include_entry = include_entry and len(entry['url']) > 1
            if include_entry:
                filtered_entries.append((entry, score))
            
    print_results(filtered_entries)


def top_search_terms():
    tf_dict = {}
    for x in st.session_state["lexicon"]:
        tf_dict[x.getKey()] = x.getValue().frequency
    tf_dict_sorted = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    df_terms = pd.DataFrame(tf_dict_sorted, columns=['Term', 'Count'])
    st.title(f'Top 100 Search Terms')
    st.table(data=df_terms[:100])


if not "engine" in st.session_state:
    init()

### Sidebar: Searching
st.sidebar.title(f'**Search**')
query = st.sidebar.text_input(f'**Query:**', value='makerspace')

# Sidebar filter section
with st.sidebar.expander('Filters'):
    year_range = st.select_slider(label='**Time period**', options=list(range(1980, 2025)), value=(1980, 2024))
    search_limit = st.slider(label="**Number of Search Results**", min_value=1, max_value=500, value=250)
    abstract_flag = st.checkbox(label='Show only results with abstracts', value=False)
    url_flag = st.checkbox(label='Show only results with unique URLs', value=False)

st.sidebar.button("Search", on_click=search, args=(query, search_limit, year_range, abstract_flag, url_flag))
st.sidebar.divider()

### Sidebar: Statistics
st.sidebar.title(f'**Statistics**')
st.sidebar.button("Top Search Terms", on_click=top_search_terms)
