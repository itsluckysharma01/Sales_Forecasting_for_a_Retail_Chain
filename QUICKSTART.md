# 🚀 Quick Start Guide - Sales Forecasting Flask App

## Step 1: Prepare the Model

Before running the Flask application, you need to train and save the model:

1. Open `Sales_Forecasting_for_a_Retail_Chain.ipynb` in Jupyter
2. Run all cells in the notebook
3. This will create `random_forest_sales_model.pkl` file

**OR** you can run the last cell in the notebook that saves the model.

## Step 2: Install Dependencies

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

This will install:

- Flask
- pandas
- numpy
- scikit-learn
- joblib
- plotly

## Step 3: Run the Application

### Option A: Using Batch File (Windows)

Simply double-click on `run_app.bat`

### Option B: Using Command Line

```bash
python app.py
```

## Step 4: Access the Application

Open your web browser and go to:

```
http://localhost:5000
```

## 📱 Navigate the App

### 1. Dashboard (Home)

- View total sales, revenue, and other KPIs
- See quick action buttons
- Get system overview

### 2. Analytics

- **Sales Trend**: Daily sales over time
- **Monthly Sales**: Average sales by month
- **Store Performance**: Top 10 stores by revenue
- **Seasonal Analysis**: Sales distribution by season
- **Promotion Impact**: Effect of promotions on sales
- **Weekend Analysis**: Weekend vs weekday comparison

### 3. Predict

Fill out the form with:

- Store and Product IDs
- Store size and location
- Date information (month, quarter, season)
- Promotion and holiday status
- Day of the week

Click "Predict Sales" to get the forecast!

### 4. Insights

- View top performing stores
- See best performing products
- Discover peak sales months
- Understand promotion effectiveness
- Get strategic recommendations

### 5. About

- Learn about the project
- View technology stack
- Understand the ML model
- See system features

## 🛑 Stop the Server

Press `Ctrl + C` in the terminal to stop the Flask server.

## 💡 Tips

1. **Model Required**: Always ensure the model file exists before running
2. **Port Change**: If port 5000 is busy, edit `app.py` and change the port
3. **Browser**: Works best on modern browsers (Chrome, Firefox, Edge)
4. **Mobile**: Fully responsive - works on phones and tablets too!

## ❓ Common Issues

### "Model not loaded" error

**Solution**: Run the Jupyter notebook to create the model file

### Port already in use

**Solution**: Change port in `app.py`:

```python
app.run(debug=True, port=5001)  # Change to 5001 or any available port
```

### Module not found error

**Solution**: Install requirements:

```bash
pip install -r requirements.txt
```

## 🎉 Enjoy!

Your Sales Forecasting System is now ready to use. Explore the features and make data-driven decisions!

---

For detailed documentation, see `FLASK_README.md`
