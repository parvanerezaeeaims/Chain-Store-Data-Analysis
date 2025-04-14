# Chain Store Data Analysis

## 📌 Overview
This project focuses on analyzing sales transactions from multiple chain stores to extract valuable insights. The analysis includes data preprocessing, exploratory data analysis (EDA), market basket analysis (Apriori algorithm), and demand forecasting.

## 🚀 Features
- **Sales Performance Analysis** – Identify best-selling products and peak sales periods.
- **Customer Behavior Analysis** – Understand purchasing patterns.
- **Market Basket Analysis** – Using the Apriori algorithm for product recommendations.
- **Time-Series Forecasting** – Predict future sales trends.
- **Store-wise Comparison** – Compare sales performance across different store locations.

## 📊 Dataset Description
The dataset consists of sales transaction records with the following columns:

| Column Name        | Description |
|--------------------|-------------|
| `user_id`         | Unique identifier for customers |
| `transaction_id`  | Unique transaction number |
| `transaction_date` | Date of the transaction (Shamsi/Gregorian) |
| `transaction_time` | Time of purchase |
| `store`           | Store location |
| `product_name`    | Name of the product |
| `quantity`        | Number of items purchased |
| `unit_price`      | Price per unit |
| `total_price`     | Price per product (unit price × quantity) |
| `total_amount`    | Total amount spent in a transaction |
| `total_items`     | Total number of products bought |

## 🛠 Installation & Setup
To set up and run the project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/parvanerezaeeaims/chain-store-analysis.git

# Navigate to the project folder
cd chain-store-analysis



# Run the analysis
streamlit run Homepage.py
```



## 📈 Results & Visualizations
The analysis produces insights such as:
- **RFM**
![Alt text]([./images/RFM.png](https://github.com/parvanerezaeeaims/Chain-Store-Data-Analysis/blob/main/Images/RFM.png))
- **Apriori**
![Alt text]([./Images/Apriori.png](https://github.com/parvanerezaeeaims/Chain-Store-Data-Analysis/blob/main/Images/Apriori.png))
- **Time base pattern analysis**
![Alt text]([./images/Time-base-pattern.png](https://github.com/parvanerezaeeaims/Chain-Store-Data-Analysis/blob/main/Images/Time-base-pattern.png))
- **Transaction analysis**
![Alt text]([./images/Transaction.png](https://github.com/parvanerezaeeaims/Chain-Store-Data-Analysis/blob/main/Images/Transaction.png))
- **Demand forcasting**
![Alt text]([./images/demand.png](https://github.com/parvanerezaeeaims/Chain-Store-Data-Analysis/blob/main/Images/demand.png))

## 🤝 Contributing
Contributions are welcome! To contribute:

```bash
# Create a new branch
git checkout -b feature-new-analysis

# Commit changes
git commit -m "Added new EDA feature"

# Push to GitHub
git push origin feature-new-analysis

# Create a Pull Request (PR)
```



