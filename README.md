# Data Cleaning & Visualization Project

**Prepared for:** Akshay  
**Project type:** Internship task — Data Cleaning & Visualization  
**Dataset:** Synthetic sample retail sales data created for demonstration (not real customer data).

## Objective
Clean a raw sales dataset, handle missing values and duplicate rows, identify and treat outliers, and communicate findings through visualizations.

## Tools
- Python
- Pandas
- NumPy
- Matplotlib

## Project structure
```text
Akshay_Data-Cleaning-Visualization-Project/
├── dataset/
│   └── raw_sales_data.csv
├── outputs/
│   ├── cleaned_sales_data.csv
│   └── product_sales_summary.csv
├── visualizations/
│   ├── sales_by_product.png
│   ├── sales_by_region.png
│   └── daily_sales_trend.png
├── data_cleaning_visualization.py
├── data_cleaning_visualization.ipynb
├── requirements.txt
└── README.md
```

## Cleaning steps
1. Load and inspect the raw CSV.
2. Check missing values and duplicate rows.
3. Remove exact duplicate rows.
4. Fill missing categorical values with `Unknown`.
5. Fill missing numeric values with the median.
6. Recalculate `Sales = Quantity × Unit_Price` to keep the data consistent.
7. Use the interquartile range (IQR) rule to detect and cap sales outliers.
8. Save the cleaned dataset and product summary.

## Visualizations
- Total sales by product
- Total sales by region
- Daily sales trend

## How to run
1. Install Python 3.10 or later.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python data_cleaning_visualization.py
   ```

The script writes cleaned data and summary files into `outputs/` and charts into `visualizations/`.

## Important notes
- The included dataset is synthetic sample data made for learning and demonstration.
- The outlier treatment is a simple demonstration choice. For real datasets, investigate outliers before changing them.
- Review the output and update this README with your own observations before submitting the internship task.
