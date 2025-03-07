import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Future Foundersا",
    page_icon="📊",
    layout="wide",
)
st.title("Main Page")

st.markdown(
    """
    <style>
        /* Main content background */
        .main {
            background-color: #0D1B2A; /* Dark blue */
        }

        /* Sidebar background */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A192F, #1B263B); /* Dark blue gradient */
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] * {
            color: white; /* Ensures text is visible */
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Sidebar
st.sidebar.markdown('<p class="sidebar-title">📌 Choose a Report </p>', unsafe_allow_html=True)
st.sidebar.markdown('Please select a report from the options below.')

