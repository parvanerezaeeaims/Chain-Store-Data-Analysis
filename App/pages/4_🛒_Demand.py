import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import jdatetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go
import plotly.subplots as sp

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



# Function to convert Shamsi to Gregorian
def convert_shamsi_to_gregorian(shamsi_date):
    year, month, day = map(int, shamsi_date.split('-'))
    g_date = jdatetime.date(year, month, day).togregorian()
    return g_date

# Load data
transaction_data = pd.read_csv(r'/home/ccp/Desktop/task1/App/Stores_Transactions .csv')  # Update with actual path

# Streamlit UI
st.title("Product Demand Forecasting using SARIMA")
store_name = st.selectbox("Select a Store", transaction_data['store'].unique())
product_name = st.selectbox("Select a Product", transaction_data[transaction_data['store'] == store_name]['product_name'].unique())

# Filter data
df = transaction_data[(transaction_data['store'] == store_name) & (transaction_data['product_name'] == product_name)]
df['transaction_date'] = df['transaction_date'].apply(convert_shamsi_to_gregorian)
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df = df.sort_values("transaction_date")
df['month'] = df['transaction_date'].dt.to_period('M')
monthly_demand = df.groupby('month')['quantity'].sum()
monthly_demand.index = monthly_demand.index.to_timestamp()

# Decompose time series
if len(monthly_demand) >= 6:
    decomposition = seasonal_decompose(monthly_demand, model='additive', period=3)
else:
    st.warning("Not enough data points for seasonal decomposition. Need at least 6 observations.")


# Stationarity check
diff_demand = monthly_demand.diff().dropna()
result = adfuller(diff_demand)
stationarity_msg = "The series is stationary" if result[1] < 0.05 else "The series is non-stationary, apply differencing"

# Display Decomposition Components
fig = sp.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                       subplot_titles=('Trend Component', 'Seasonal Component', 'Residual Component', 'Original Data'))
fig.add_trace(go.Scatter(x=decomposition.trend.index, y=decomposition.trend, mode='lines', name='Trend'), row=1, col=1)
fig.add_trace(go.Scatter(x=decomposition.seasonal.index, y=decomposition.seasonal, mode='lines', name='Seasonality'), row=2, col=1)
fig.add_trace(go.Scatter(x=decomposition.resid.index, y=decomposition.resid, mode='lines', name='Residuals'), row=3, col=1)
fig.add_trace(go.Scatter(x=monthly_demand.index, y=monthly_demand, mode='lines', name='Original Data'), row=4, col=1)
fig.update_layout(title='Decomposition of Time Series', height=800, showlegend=True)
st.plotly_chart(fig)



# SARIMA Model
model = SARIMAX(monthly_demand, order=(2, 1, 2), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit()




# Forecast next 12 months
forecast = model_fit.forecast(steps=12)
st.subheader('Forecasted Values for the Next 12 Months')
st.write(forecast)


