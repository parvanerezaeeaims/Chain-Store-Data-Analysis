import streamlit as st
import pandas as pd
from apyori import apriori







class AprioriAnalysis:
    def __init__(self, data, min_support, min_confidence, min_lift):
        self.data = data
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.min_lift = min_lift
        self.result = None

    def preprocess_data(self):
        data_temp = self.data.copy()
        data_temp['product_name'] = data_temp['product_name'] + ','
        grouped = data_temp.groupby(['user_id', 'transaction_date']).agg({'product_name': 'sum'})
        records = []
        for line in grouped['product_name']:
            items = line.split(',')
            temp = [item.strip() for item in items if item.strip() != '']
            records.append(temp)
        return records

    def run_apriori(self, records):
        return apriori(records, min_support=self.min_support, min_confidence=self.min_confidence, min_lift=self.min_lift)

    def get_association_rules(self):
        records = self.preprocess_data()
        result = self.run_apriori(records)

        # Prepare the result table
        table = []
        for res in result:
            for item in res[2]:
                table.append([
                    ', '.join(list(item.items_base)),
                    ', '.join(list(item.items_add)),
                    res[1],            # Support
                    item.confidence,   # Confidence
                    item.lift         # Lift
                ])
        
        # Return the result as a DataFrame
        headers = ["Items Base", "Items Add", "Support", "Confidence", "Lift"]
        return pd.DataFrame(table, columns=headers)


def display_apriori_results():
    # Set up the page configuration
    st.set_page_config(page_title="Task1:", page_icon="📊", layout="wide")
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
    st.sidebar.title("⚡ Apriori Algorithm")
    st.sidebar.markdown("""
        <div style='border: 2px solid #ddd; padding: 15px; border-radius: 8px; background-color: #001f3f; color: white;'>
            <h3 style='font-size:16px;'>🔹 min_support = 0.0005</h3>
            <h3 style='font-size:16px;'>🔹 min_lift = 1.1</h3>
            <h3 style='font-size:16px;'>🔹 min_confidence = 0.007</h3>
        </div>
    """, unsafe_allow_html=True)

    # Load the dataset
    df = pd.read_csv(r"/home/ccp/Desktop/task1/Stores_Transactions .csv")

    # Display the first few rows of the dataset
    with st.expander("📌 View Dataset Overview", expanded=True):
        st.write(df.head(10))

    # Initialize AprioriAnalysis with the dataset and parameters
    apriori_analysis = AprioriAnalysis(df, min_support=0.0005, min_confidence=0.007, min_lift=1.1)

    # Run Apriori analysis and display the result
    result = apriori_analysis.get_association_rules()

    if not result.empty:
        st.success("✅ Association rules found!")
        st.dataframe(result.style.set_properties(**{
            'background-color': '#f9f9f9',
            'border': '1px solid #ddd',
            'border-radius': '8px'
        }))
    else:
        st.warning("⚠️ No association rules found with the given parameters.")


# Call the display_apriori_results function to run the Streamlit app
display_apriori_results()
