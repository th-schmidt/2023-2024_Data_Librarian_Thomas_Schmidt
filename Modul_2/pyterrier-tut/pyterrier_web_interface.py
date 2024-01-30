#learn more about streamlit: https://docs.streamlit.io/

import streamlit as st
import pyterrier as pt
import pickle
import os

os.environ["JAVA_HOME"] = "./jdk/Contents/Home/"

if not pt.started():
    pt.init()

def init():
    index = pt.IndexFactory.of("./makerspace_index_mult/data.properties")
    st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
    st.session_state["data"] = pickle.load(open("./bibsonomy_clean_data/makerspace_vr.pkl", "rb"))
    

def search(query):
    res = st.session_state["engine"].search(query)
    fields_to_show = ['text', 'tags', 'url', 'author', 'abstract']

    for _, row in res.iterrows():
        score = round(row['score'], 2)
        entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]

        for field in fields_to_show:
            if field == "text":
                st.title(entry[field])
            elif field == 'author' or field == 'tags':
                if isinstance(entry[field], list):
                    st.write(f"{field.capitalize()}: \t {', '.join(entry[field])}")
                else:
                    st.write(f"{field.capitalize()}: \t {entry[field]}")
            elif field == 'url':
                if len(entry[field]) <= 1:
                    st.write(f"{field.upper()}: \t {entry['docno']}")
                else:
                    st.write(f"{field.upper()}: \t {entry[field]}")
            else:
                st.write(f"{field.capitalize()}: \t {entry[field]}")

        st.write(f"Score: {score}")
        st.divider()


if not "engine" in st.session_state:
    init()

query = st.sidebar.text_input("Query")
st.sidebar.button("Search", on_click=search, args=(query,))