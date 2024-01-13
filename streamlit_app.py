import streamlit as st

def search_function(query, option):
    # Implement your search logic here based on the query and selected option
    # For simplicity, let's just print the query and selected option for now
    print(f"Searching for '{query}' in '{option}'...")

# Streamlit app
st.title("Search App")

# Dropdown for selecting search option
search_option = st.selectbox("Select Search Option", ['expertise', 'personal', 'everything'])

# Radial select for employment status
membership_status = st.radio("Select Membership Status", ["Current", "Former"])


# Text input for search query
search_query = st.text_input("Enter Search Query")

# Search button
if st.button("Search"):
    search_function(search_query, search_option)
