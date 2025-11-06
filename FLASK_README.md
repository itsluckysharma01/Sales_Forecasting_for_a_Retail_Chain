# Sales Forecasting Flask Web Application

An interactive web application for retail sales forecasting using machine learning and data analytics.

## 🚀 Features

- **Interactive Dashboard**: Real-time sales metrics and KPIs
- **Advanced Analytics**: Dynamic visualizations using Plotly
- **ML Predictions**: Random Forest-based sales forecasting
- **Business Insights**: Data-driven recommendations
- **Responsive Design**: Works seamlessly on all devices

## 📋 Prerequisites

- Python 3.8 or higher
- Trained Random Forest model (`random_forest_sales_model.pkl`)

## 🛠️ Installation

1. **Clone or navigate to the project directory**:

   ```bash
   cd Sales_Forecasting_for_a_Retail_Chain
   ```

2. **Install required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the model file exists**:
   - Run the Jupyter notebook `Sales_Forecasting_for_a_Retail_Chain.ipynb` to train and save the model
   - The model will be saved as `random_forest_sales_model.pkl`

## 🎯 Running the Application

1. **Start the Flask server**:

   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:

   ```
   http://localhost:5000
   ```

3. **Explore the application**:
   - **Dashboard** (`/`): Overview of key metrics
   - **Analytics** (`/analytics`): Interactive visualizations
   - **Predict** (`/predict`): Make sales predictions
   - **Insights** (`/insights`): Business recommendations
   - **About** (`/about`): System information

## 📁 Project Structure

```
Sales_Forecasting_for_a_Retail_Chain/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── random_forest_sales_model.pkl   # Trained ML model
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Dashboard page
│   ├── analytics.html             # Analytics page
│   ├── predict.html               # Prediction page
│   ├── insights.html              # Insights page
│   └── about.html                 # About page
│
└── static/                         # Static files
    └── css/
        └── style.css              # Custom CSS styles
```

## 🔧 API Endpoints

### Frontend Routes

- `GET /` - Dashboard
- `GET /analytics` - Analytics page
- `GET /predict` - Prediction form
- `GET /insights` - Business insights
- `GET /about` - About page

### API Routes

- `GET /api/sales_trend` - Sales trend data
- `GET /api/monthly_sales` - Monthly sales data
- `GET /api/store_performance` - Store performance data
- `GET /api/seasonal_analysis` - Seasonal analysis data
- `GET /api/promotion_impact` - Promotion impact data
- `GET /api/weekend_analysis` - Weekend vs weekday data
- `POST /api/predict` - Make sales prediction

## 📊 Making Predictions

To make a prediction, fill out the form on the Predict page with:

- Store ID and Product ID
- Store size and location type
- Date information (month, quarter, season, etc.)
- Promotion and holiday status
- Day of week

The model will return predicted daily sales based on these parameters.

## 🎨 Technologies Used

### Backend

- **Flask**: Web framework
- **scikit-learn**: Machine learning
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

### Frontend

- **Bootstrap 5**: UI framework
- **Plotly.js**: Interactive charts
- **Font Awesome**: Icons
- **JavaScript**: Client-side logic

## 📝 Notes

- The application loads data from the online dataset URL
- Model predictions require all form fields to be filled
- Charts are generated dynamically using Plotly
- All visualizations are interactive and responsive

## 🐛 Troubleshooting

**Model not found error**:

- Run the Jupyter notebook first to train and save the model
- Ensure `random_forest_sales_model.pkl` is in the project root

**Port already in use**:

- Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Import errors**:

- Reinstall requirements: `pip install -r requirements.txt --upgrade`

## 📧 Support

For questions or issues, please refer to the About page in the application.

---

**Built with ❤️ for SmartEd Project**
