import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import jdatetime

st.set_page_config(page_title="Time-Based Pattern Analysis", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Time-Based Pattern Analysis")

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



def get_day_of_week_persian(shamsi_date):
    shamsi_date = shamsi_date.replace('-', '/')
    persian_date = jdatetime.datetime.strptime(shamsi_date, "%Y/%m/%d")
    persian_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekday_num = persian_date.weekday()
    return persian_days[weekday_num]

def get_shamsi_month(shamsi_date):
    year, month, day = map(int, shamsi_date.split('-'))
    return month

def get_season(transaction_date):
    month = int(transaction_date.split("-")[1])
    if month in [1, 2, 3]:
        return "Spring"
    elif month in [4, 5, 6]:
        return "Summer"
    elif month in [7, 8, 9]:
        return "Autumn"
    else:
        return "Winter"

class TransactionVisualizer:
    def __init__(self, df):
        self.df = self.preprocess_data(df)
    
    def preprocess_data(self, df):
        df["day_of_week"] = df["transaction_date"].apply(lambda x: get_day_of_week_persian(x))
        df["hour"] = pd.to_datetime(df["transaction_time"].astype(str)).dt.hour
        df["month"] = df["transaction_date"].apply(lambda x: get_shamsi_month(x))
        df["season"] = df["transaction_date"].apply(lambda x: get_season(x))
        return df
    
    def transactions_per_hour(self):
        transactions_per_hour = self.df.groupby("hour")["transaction_id"].nunique()
        
        fig = px.bar(
            transactions_per_hour,
            x=transactions_per_hour.index,
            y=transactions_per_hour.values,
            title="📊 Transactions per hour",
            labels={"x": "Hour", "y": "Number of Transactions"},
            color=transactions_per_hour.values,
            color_continuous_scale="Blues",
            text=transactions_per_hour.values
        )
        
        self._update_layout(fig, "Hour")
        return fig
    
    def transactions_per_day(self):
        transactions_per_day = self.df.groupby("day_of_week")["transaction_id"].nunique()
        
        fig = px.bar(
            transactions_per_day,
            x=transactions_per_day.index,
            y=transactions_per_day.values,
            title="📊 Transactions Per Day of the Week",
            labels={"x": "Day of the Week", "y": "Number of Transactions"},
            color=transactions_per_day.values,
            color_continuous_scale="Blues",
            text=transactions_per_day.values
        )
        
        self._update_layout(fig, "Day of the Week")
        return fig
    
    def spending_per_month(self):
        spending_per_month = self.df.groupby("month")["total_price"].sum()
        
        fig = px.line(
            spending_per_month,
            x=spending_per_month.index,
            y=spending_per_month.values,
            title="📈 Monthly Spending Trend",
            labels={"x": "Month", "y": "Total Spending"},
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["dodgerblue"]
        )
        
        self._update_layout(fig, "Month")
        return fig
    
    def peak_shopping_hours(self):
        transactions_per_hour = self.df.groupby("hour")["transaction_id"].nunique()
        
        fig = px.line(
            transactions_per_hour,
            x=transactions_per_hour.index,
            y=transactions_per_hour.values,
            title="⏰ Peak Shopping Hours",
            labels={"x": "Hour of the Day", "y": "Number of Transactions"},
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["dodgerblue"]
        )
        
        self._update_layout(fig, "Hour of the Day")
        return fig
    
    def _update_layout(self, fig, x_label):
        fig.update_layout(
            title_x=0.5,
            xaxis=dict(title=x_label),
            yaxis=dict(title="Transactions"),
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0.1)',
            margin=dict(l=40, r=40, t=60, b=40)
        )

df = pd.read_csv("/home/ccp/Desktop/demo-app/Stores_Transactions .csv")  
visualizer = TransactionVisualizer(df)

st.title("Transaction Analysis Dashboard")

st.sidebar.header("Visualization Options")
option = st.sidebar.selectbox(
    "Choose a visualization:",
    [
        "Transactions per Hour",
        "Transactions per Day",
        "Spending per Month",
        "Peak Shopping Hours"
    ]
)

if option == "Transactions per Hour":
    st.subheader("Transactions Per Hour")
    st.plotly_chart(visualizer.transactions_per_hour())

elif option == "Transactions per Day":
    st.subheader("Transactions Per Day")
    st.plotly_chart(visualizer.transactions_per_day())

elif option == "Spending per Month":
    st.subheader("Spending Per Month")
    st.plotly_chart(visualizer.spending_per_month())

elif option == "Peak Shopping Hours":
    st.subheader("Peak Shopping Hours")
    st.plotly_chart(visualizer.peak_shopping_hours())
