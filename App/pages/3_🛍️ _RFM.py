import pandas as pd
import plotly.express as px
import jdatetime
import streamlit as st

# Streamlit Page Configuration
st.set_page_config(page_title=" RFM Analysis", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart:  RFM Analysis")
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
# Define CSV File Path (Replace with your actual file path)
csv_file_path = "/home/ccp/Desktop/demo-app/Stores_Transactions .csv"

class RFMAnalysis:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.RFM = None
        self.max_date = None
    
    def preprocess_data(self):
        """Convert Shamsi to Gregorian and process transaction dates."""
        self.df["transaction_date"] = self.df["transaction_date"].apply(
            lambda x: jdatetime.datetime.strptime(x, "%Y-%m-%d").togregorian()
        )
        self.df["transaction_date"] = pd.to_datetime(self.df["transaction_date"])
        self.max_date = self.df['transaction_date'].max()
    
    def calculate_rfm(self):
        """Compute Recency, Frequency, and Monetary values."""
        R = self.df.groupby('user_id').agg({'transaction_date': 'max'})
        R['transaction_date'] = R['transaction_date'].apply(lambda x: (self.max_date - x).days + 1)
        
        F = self.df.groupby('user_id').agg({'transaction_id': 'nunique'})
        M = self.df.groupby('user_id').agg({'total_price': 'sum'})
        
        self.RFM = pd.concat([R, F, M], axis=1)
        self.RFM.columns = ['R', 'F', 'M']
    
    def assign_scores(self):
        """Assign quantile-based scores to F and M values."""
        self.RFM['F_score'] = pd.qcut(self.RFM['F'], q=5, labels=[1, 2, 3, 4, 5])
        self.RFM['M_score'] = pd.qcut(self.RFM['M'], q=5, labels=[1, 2, 3, 4, 5])
        self.RFM['RFM_Score'] = self.RFM['F_score'].astype(str) + self.RFM['M_score'].astype(str)
    
    def assign_segments(self):
        """Define customer segments based on RFM scores."""
        def segment(row):
            if row['RFM_Score'] in ['55', '54', '45']:
                return 'Champions'
            elif row['RFM_Score'] in ['44', '45', '54']:
                return 'Loyal Customers'
            elif row['RFM_Score'] in ['35', '43', '45']:
                return 'Potential Loyalists'
            elif row['RFM_Score'] in ['33', '23', '22', '21']:
                return 'Hibernating'
            else:
                return 'Lost Customers'
        
        self.RFM['Segment'] = self.RFM.apply(segment, axis=1)
    
    def plot_fm_iplot(self):
        """Create an interactive scatter plot using Plotly."""
        segment_colors = {
            'Champions': 'blue', 'Loyal Customers': 'green',
            'Potential Loyalists': 'yellow', 'Hibernating': 'orange', 'Lost Customers': 'red'
        }
        self.RFM['Color'] = self.RFM['Segment'].map(segment_colors).fillna('gray')
        RFM_reset = self.RFM.reset_index()
        
        fig = px.scatter(
            RFM_reset, x='F', y='M', color='Segment', color_discrete_map=segment_colors,
            title="Customer Segmentation Based on Frequency & Monetary Value",
            labels={'F': 'Frequency (Number of Purchases)', 'M': 'Monetary Value (Total Spend)'},
            hover_data={'Customer_ID': RFM_reset.index, 'F': True, 'M': True}
        )
        
        fig.update_layout(
            xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='LightGrey'),
            yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='LightGrey'),
            showlegend=True, legend_title="Customer Segments", template="plotly_white"
        )
        
        return fig
    
    def run_analysis(self):
        self.preprocess_data()
        self.calculate_rfm()
        self.assign_scores()
        self.assign_segments()
        return self.RFM, self.plot_fm_iplot()

# Run Analysis
rfm = RFMAnalysis(csv_file_path)
rfm_results, rfm_plot = rfm.run_analysis()

# Display Data
st.subheader("RFM Table")
st.dataframe(rfm_results.style.highlight_max(axis=0))

# Show Plot
st.subheader("Customer Segmentation Plot")
st.plotly_chart(rfm_plot)
