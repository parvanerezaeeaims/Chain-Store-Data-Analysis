import streamlit as st
import pandas as pd
import plotly.express as px  
import streamlit as st

# Set page config
st.set_page_config(page_title="Transaction Analysis", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #001f3f; /* Dark Blue Background */
            color: white;
        }
        h1 {
            color: white !important;
        }
        /* Change label color */
        label {
            color: white !important;
        }
        /* Change dropdown text color */
        div[data-baseweb="select"] > div {
            color: black !important; /* Text inside dropdown */
            background-color: white !important; /* Dropdown background */
        }
    </style>
    """,
    unsafe_allow_html=True
)



df= pd.read_csv(r"/home/ccp/Desktop/task1/Stores_Transactions .csv")
# Get unique values for selection
unique_dates = df["transaction_date"].unique()
unique_stores = df["store"].unique()

# Streamlit UI
st.title("Transaction Analysis")

# Dropdown for store selection
selected_store = st.selectbox("Select a Store", unique_stores)

# Dropdown for interval selection (start and end date)
selected_start_date = st.selectbox("Select Start Date", unique_dates)
selected_end_date = st.selectbox("Select End Date", unique_dates, index=len(unique_dates)-1)

# Filter data based on selection
filtered_df = df[(df["transaction_date"] >= selected_start_date) &
                 (df["transaction_date"] <= selected_end_date) &
                 (df["store"] == selected_store)]

total_price_sum = filtered_df["total_price"].sum()
total_unique_users = filtered_df["user_id"].nunique()
total_transactions = filtered_df.shape[0]


# Create columns for metrics
col1, col2, col3 = st.columns(3)

# Style each column with a dark blue background using HTML and CSS
with col1:
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 8px;">
            <h3 style="color: white;">Total Price</h3>
            <p style="color: white; font-size: 18px;">{:,}</p>
        </div>
    """.format(total_price_sum), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 8px;">
            <h3 style="color: white;">Unique Users</h3>
            <p style="color: white; font-size: 18px;">{}</p>
        </div>
    """.format(total_unique_users), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 8px;">
            <h3 style="color: white;">Total Transactions</h3>
            <p style="color: white; font-size: 18px;">{}</p>
        </div>
    """.format(total_transactions), unsafe_allow_html=True)


# Display results
st.write("### Filtered Transactions")
st.dataframe(filtered_df)
# Add a horizontal separator
st.markdown("""---""")

# Group the data  
df_grouped = df.groupby(by=['store', 'product_name', "transaction_date"])['total_price'].sum().reset_index(name='sum')  

# Create the sunburst chart  
fig = px.sunburst(df_grouped, path=['store', 'product_name', "transaction_date"], values='sum', title='Nested Pie Chart')  

# Streamlit application  
st.title('Sales Data Visualization')  
st.plotly_chart(fig)  