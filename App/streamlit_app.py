import streamlit as st
import pandas as pd
import chromadb

favicon = "exitico.ico"
exit_logo = "exit-flag_med_invert_sq-1-scaled.png"

# config page settings.
st.set_page_config(page_title="EXIT Bot", page_icon=favicon, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Exit Logo
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(exit_logo)

# Initialize session state variables
if 'exit_df' not in st.session_state:
    st.session_state.exit_df = None
    st.session_state.collection = None

# Function to ingest data and return DataFrame and ChromaDB collection
def ingest():
    exit_df = pd.read_csv('Exit_person_profiles.csv')
    cols = exit_df.columns
    exit_df['ID'] = range(1, len(exit_df) + 1)

    ids = exit_df['ID'].astype(str).values.tolist()

    # Convert pandas rows to a list of lists excluding header
    exit_list = exit_df.values.tolist()

    # Convert each row in the list of lists to a list of strings
    df_list_string = [', '.join(map(str, row)) for row in exit_list]

    # Import Chroma and instantiate a client.
    client = chromadb.Client()

    # Create a new Chroma collection
    collection = client.get_or_create_collection('exit_collection')

    # Embed and store the lines in the collection
    collection.add(
        ids=ids,
        documents=df_list_string,
        metadatas=[{"type": "support"} for _ in range(len(df_list_string))],
    )

    return exit_df, collection

# Function to perform search and display results
def search_function(prompt, collection, exit_df, result_type, location_filter=None, family_status_filter=None, expertise_filter=None):
    # Implement your search logic here based on the query, selected option, and state filter
    results = collection.query(query_texts=[prompt], n_results=5)

    if result_type == "Name Only":
        # Apply filters if provided
        if location_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Location '].str.contains(location_filter)].iloc[:, 0]
        elif family_status_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Family Status '].str.contains(family_status_filter)].iloc[:, 0]
        elif expertise_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Expertise '].str.contains(expertise_filter)].iloc[:, 0]
        else:
            # Display only the first column regardless of its name
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df.iloc[:, 0].loc[exit_df['ID'].astype(str).isin(results_ids)]
    else:
        # Apply filters if provided
        if location_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Location '].str.contains(location_filter)]
        elif family_status_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Family Status '].str.contains(family_status_filter)]
        elif expertise_filter:
            results_ids = [str(id) for id in results['ids'][0]]
            df = exit_df[exit_df['ID'].astype(str).isin(results_ids) & exit_df[' Expertise '].str.contains(expertise_filter)]
        else:
            df = exit_df[exit_df['ID'].astype(str).isin(results['ids'][0])]

    st.table(df)

# Streamlit app
st.title("Member Search App")

st.divider()

# Initialize collection outside the filter conditional statements
st.session_state.exit_df, st.session_state.collection = ingest()

# Radio buttons for selecting search option
result_type = st.radio(
    "Select Search Option:",
    ["Name Only", "Full Member Info"],
    index=1  # Set default selection to "Full Member Info"
)

# Text input for search query
search_query = st.text_area("Enter Search Query")

# Checkbox for location filter
filter_by_location = st.checkbox("Filter by Location")

# Dropdown for selecting location if filter is enabled
if filter_by_location:
    locations = st.sidebar.selectbox("Select Location", sorted(st.session_state.exit_df[' Location '].unique()))

# Checkbox for family status filter
filter_by_family_status = st.checkbox("Filter by Family Status")

# Dropdown for selecting family status if filter is enabled
if filter_by_family_status:
    family_statuses = st.sidebar.selectbox("Select Family Status", sorted(st.session_state.exit_df[' Family Status '].unique()))

# Checkbox for expertise filter
filter_by_expertise = st.checkbox("Filter by Expertise")

# Dropdown for selecting expertise if filter is enabled
if filter_by_expertise:
    expertises = st.sidebar.selectbox("Select Expertise", sorted(st.session_state.exit_df[' Expertise '].unique()))

# Search button
if st.button("Search"):
    # Pass filters if enabled
    location_filter = locations if filter_by_location else None
    family_status_filter = family_statuses if filter_by_family_status else None
    expertise_filter = expertises if filter_by_expertise else None
    search_function(search_query, st.session_state.collection, st.session_state.exit_df, result_type, location_filter, family_status_filter, expertise_filter)
