import streamlit as st
import pandas as pd
import csv
import chromadb

def ingest():
    exit_df = pd.read_csv('Exit_person_profiles.csv')
    cols = exit_df.columns
    exit_df['ID'] = range(1, len(exit_df) + 1)

    ids=exit_df['ID'].values.tolist()
    list2 = []
    for num in ids:
        list2.append(f"{str(num)}")
    ids=list2
    # convert pandas rows to a list of lists excluding header
    exit_list = exit_df.values.tolist()
    # Convert each row in the list of lists to a list of strings
    exit_list = [[str(x) for x in row] for row in exit_list]
    df_list_string = []
    for row in exit_list:
        df_list_string.append(', '.join(row))

    # Import Chroma and instantiate a client. The default Chroma client is ephemeral, meaning it will not save to disk.


    client = chromadb.Client()

    # Create a new Chroma collection 
    collection = client.get_or_create_collection('exit_collection')

    # Embed and store the lines in the colleciton
    collection.add(
        ids=ids,  # IDs are just strings
        documents=df_list_string,
        metadatas=[{"type": "support"} for _ in range(len(df_list_string))
        ],
    )
    return (exit_df, collection)

def search_function(prompt, collection):
    # Implement your search logic here based on the query and selected option
    results = collection.query(
    query_texts=[prompt],
    n_results=5)
    df = exit_df[exit_df['ID'].astype(str).isin(results['ids'][0])] 
    # For simplicity, let's just print the query and selected option for now
    st.dataframe(df)

# Streamlit app
st.title("Search App")

# Dropdown for selecting search option
search_option = st.selectbox("Select Search Option", ['All Info', 'Name Only'])

# Text input for search query
search_query = st.text_input("Enter Search Query")
first_run = True
# Search button
if st.button("Search"):
    if first_run:
        exit_df, collection = ingest()
    search_function(search_query, collection)
    first_run = False
