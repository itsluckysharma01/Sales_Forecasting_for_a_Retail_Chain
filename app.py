from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import os
app = Flask(__name__)

# Load the model and data
try:
    rf_model = joblib.load('random_forest_sales_model.pkl')
    print("Model loaded successfully!")
except:
    rf_model = None
    print("Model not found. Please run the notebook first to train and save the model.")

# Load dataset - Try local file first, fallback to URL
try:
    df = pd.read_csv('sales_forecasting_dataset_SmartEd_Project.csv')
    print("Loaded data from local file")
except FileNotFoundError:
    print("Local file not found, loading from URL...")
    df = pd.read_csv('https://raw.githubusercontent.com/itsluckysharma01/Datasets/refs/heads/main/sales_forecasting_dataset_SmartEd_Project.csv')

# Data preprocessing
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.month_name()
df['Quarter'] = df['Date'].dt.quarter
df['Week_of_Year'] = df['Date'].dt.isocalendar().week
df['Day_of_Month'] = df['Date'].dt.day
df['Is_Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday']).astype(int)

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['Season'] = df['Month'].apply(get_season)

# Encode categorical variables for predictions
from sklearn.preprocessing import LabelEncoder

le_size = LabelEncoder()
le_location = LabelEncoder()
le_day = LabelEncoder()
le_season = LabelEncoder()

df['Store_Size_Encoded'] = le_size.fit_transform(df['Store_Size'])
df['Location_Encoded'] = le_location.fit_transform(df['Store_Location_Type'])
df['Day_Encoded'] = le_day.fit_transform(df['Day_of_Week'])
df['Season_Encoded'] = le_season.fit_transform(df['Season'])

@app.route('/')
def home():
    """Home page with dashboard overview"""
    # Calculate key metrics
    total_sales = df['Daily_Sale'].sum()
    total_revenue = df['Revenue'].sum()
    avg_daily_sales = df['Daily_Sale'].mean()
    total_stores = df['Store_ID'].nunique()
    total_products = df['Product_ID'].nunique()
    
    # Best performing store
    best_store = df.groupby('Store_ID')['Revenue'].sum().idxmax()
    
    return render_template('index.html',
                         total_sales=f"{total_sales:,.0f}",
                         total_revenue=f"${total_revenue:,.2f}",
                         avg_daily_sales=f"{avg_daily_sales:,.0f}",
                         total_stores=total_stores,
                         total_products=total_products,
                         best_store=best_store)

@app.route('/analytics')
def analytics():
    """Analytics page with detailed visualizations"""
    return render_template('analytics.html')

@app.route('/api/sales_trend')
def sales_trend():
    """API endpoint for sales trend data"""
    daily_trend = df.groupby('Date')['Daily_Sale'].sum().reset_index()
    
    fig = px.line(daily_trend, x='Date', y='Daily_Sale',
                  title='Daily Sales Trend Over Time',
                  labels={'Daily_Sale': 'Total Daily Sales', 'Date': 'Date'})
    fig.update_traces(line_color='#2E86C1', line_width=2)
    fig.update_layout(hovermode='x unified', template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/monthly_sales')
def monthly_sales():
    """API endpoint for monthly sales data"""
    monthly_data = df.groupby('Month_Name')['Daily_Sale'].mean().reindex(
        ['January', 'February', 'March', 'April', 'May', 'June',
         'July', 'August', 'September', 'October', 'November', 'December'])
    
    fig = px.bar(x=monthly_data.index, y=monthly_data.values,
                 title='Average Sales by Month',
                 labels={'x': 'Month', 'y': 'Average Daily Sales'},
                 color=monthly_data.values,
                 color_continuous_scale='Viridis')
    fig.update_layout(showlegend=False, template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/store_performance')
def store_performance():
    """API endpoint for store performance data"""
    store_data = df.groupby('Store_ID').agg({
        'Revenue': 'sum',
        'Daily_Sale': 'sum'
    }).sort_values('Revenue', ascending=False).head(10).reset_index()
    
    fig = px.bar(store_data, x='Store_ID', y='Revenue',
                 title='Top 10 Stores by Revenue',
                 labels={'Revenue': 'Total Revenue', 'Store_ID': 'Store ID'},
                 color='Revenue',
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/seasonal_analysis')
def seasonal_analysis():
    """API endpoint for seasonal analysis"""
    seasonal_data = df.groupby('Season')['Daily_Sale'].mean().reset_index()
    
    fig = px.pie(seasonal_data, values='Daily_Sale', names='Season',
                 title='Sales Distribution by Season',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/promotion_impact')
def promotion_impact():
    """API endpoint for promotion impact analysis"""
    promo_data = df.groupby('Promotion')['Daily_Sale'].mean().reset_index()
    promo_data['Promotion'] = promo_data['Promotion'].map({0: 'No Promotion', 1: 'With Promotion'})
    
    fig = px.bar(promo_data, x='Promotion', y='Daily_Sale',
                 title='Impact of Promotions on Sales',
                 labels={'Daily_Sale': 'Average Daily Sales', 'Promotion': 'Promotion Status'},
                 color='Daily_Sale',
                 color_continuous_scale='Greens')
    fig.update_layout(showlegend=False, template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/weekend_analysis')
def weekend_analysis():
    """API endpoint for weekend vs weekday analysis"""
    weekend_data = df.groupby('Is_Weekend')['Daily_Sale'].mean().reset_index()
    weekend_data['Day_Type'] = weekend_data['Is_Weekend'].map({0: 'Weekday', 1: 'Weekend'})
    
    fig = px.bar(weekend_data, x='Day_Type', y='Daily_Sale',
                 title='Weekend vs Weekday Sales Comparison',
                 labels={'Daily_Sale': 'Average Daily Sales', 'Day_Type': 'Day Type'},
                 color='Daily_Sale',
                 color_continuous_scale='Oranges')
    fig.update_layout(showlegend=False, template='plotly_white')
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/predict')
def predict_page():
    """Prediction page"""
    stores = sorted(df['Store_ID'].unique().tolist())
    products = sorted(df['Product_ID'].unique().tolist())
    store_sizes = df['Store_Size'].unique().tolist()
    locations = df['Store_Location_Type'].unique().tolist()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    return render_template('predict.html',
                         stores=stores,
                         products=products,
                         store_sizes=store_sizes,
                         locations=locations,
                         days=days)

@app.route('/api/predict', methods=['POST'])
def make_prediction():
    """API endpoint for making sales predictions"""
    if rf_model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 400
    
    try:
        data = request.json
        
        # Encode categorical variables
        store_size_encoded = le_size.transform([data['store_size']])[0]
        location_encoded = le_location.transform([data['location']])[0]
        day_encoded = le_day.transform([data['day_of_week']])[0]
        season_encoded = le_season.transform([data['season']])[0]
        
        # Prepare features
        features = [[
            int(data['store_id']),
            int(data['product_id']),
            int(data['promotion']),
            int(data['holiday']),
            store_size_encoded,
            location_encoded,
            day_encoded,
            int(data['month']),
            int(data['quarter']),
            int(data['is_weekend']),
            season_encoded,
            int(data['week_of_year']),
            int(data['day_of_month'])
        ]]
        
        # Make prediction
        prediction = rf_model.predict(features)[0]
        
        return jsonify({
            'predicted_sales': round(prediction, 2),
            'message': 'Prediction successful!'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/insights')
def insights():
    """Insights and recommendations page"""
    # Top performing stores
    top_stores = df.groupby('Store_ID').agg({
        'Revenue': 'sum',
        'Daily_Sale': 'mean'
    }).sort_values('Revenue', ascending=False).head(5).reset_index()
    
    # Top performing products
    top_products = df.groupby('Product_ID').agg({
        'Revenue': 'sum',
        'Daily_Sale': 'mean'
    }).sort_values('Revenue', ascending=False).head(5).reset_index()
    
    # Best months
    best_months = df.groupby('Month_Name')['Daily_Sale'].mean().sort_values(ascending=False).head(3)
    
    # Promotion effectiveness
    promo_effect = df.groupby('Promotion')['Daily_Sale'].mean()
    promo_increase = ((promo_effect[1] - promo_effect[0]) / promo_effect[0] * 100) if len(promo_effect) > 1 else 0
    
    return render_template('insights.html',
                         top_stores=top_stores.to_dict('records'),
                         top_products=top_products.to_dict('records'),
                         best_months=best_months.index.tolist(),
                         promo_increase=round(promo_increase, 2))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)