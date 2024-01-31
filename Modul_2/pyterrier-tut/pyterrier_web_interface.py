#learn more about streamlit: https://docs.streamlit.io/

import streamlit as st
import pyterrier as pt
import numpy as np
import pickle
import os

os.environ["JAVA_HOME"] = "./jdk/Contents/Home/" # Set JAVA env variable


if not pt.started():
    pt.init()

def init():
    index = pt.IndexFactory.of("./makerspace_index_mult/data.properties")
    st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
    st.session_state["data"] = pickle.load(open("./bibsonomy_clean_data/makerspace_vr.pkl", "rb"))


def search(query, search_limit):
    
    res = st.session_state["engine"].search(query)[:search_limit]
    fields_to_show = ['text', 'tags', 'url', 'author', 'abstract']
    result_num = 1

    for _, row in res.iterrows():
        score = round(row['score'], 2)
        entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]
        
        st.write(f'Result **{result_num}** of **{len(res)}**')
        
        for field in fields_to_show:
            if field == "text":
                st.title(entry[field])
            elif field == 'author' or field == 'tags':
                if isinstance(entry[field], list):
                    st.write(f"**{field.capitalize()}:** \t {', '.join(entry[field]).strip()}")
                else:
                    st.write(f"{field.capitalize()}: \t {entry[field]}")
            elif field == 'url':
                if len(entry[field]) <= 1:
                    st.write(f"**{field.upper()}:** \t {entry['docno']}")
                else:
                    st.write(f"**{field.upper()}:** \t {entry[field]}")
            else:
                st.write(f"**{field.capitalize()}:** \t {entry[field]}")

        st.write(f"**:red[Score: {score}]**")
        st.divider()
        
        result_num += 1


if not "engine" in st.session_state:
    init()

query = st.sidebar.text_input("**Query**")
slider_value = st.sidebar.slider(label="**Number of Search Results**", min_value=1, max_value=500, value=100)
st.sidebar.button("Search", on_click=search, args=(query, slider_value))
