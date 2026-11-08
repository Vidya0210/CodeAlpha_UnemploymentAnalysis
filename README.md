# 📊 Unemployment Analysis During COVID-19 in India

An interactive data analytics dashboard built using **Python, Streamlit, Pandas and Plotly** to explore unemployment trends in India during the COVID-19 period.

The project analyzes unemployment rates, employment estimates and labour participation across different Indian states and rural and urban areas.

## 🚀 Project Overview

The COVID-19 pandemic significantly affected employment and economic activities across India.

This project uses unemployment datasets to explore employment trends, compare regional differences and visualize the impact of the pandemic through an interactive dashboard.

## 🎯 Project Objectives

- Analyze unemployment trends over time.
- Compare rural and urban unemployment rates.
- Identify states with higher average unemployment rates.
- Analyze average employment across states.
- Compare labour participation rates among states.
- Explore employment-related patterns during the COVID-19 period.

## 🛠️ Technologies Used

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Data analysis and processing   |
| Pandas     | Data cleaning and manipulation |
| NumPy      | Numerical operations           |
| Matplotlib | Data visualization             |
| Seaborn    | Statistical visualization      |
| Plotly     | Interactive charts             |
| Streamlit  | Interactive dashboard          |

## 📈 Dashboard Features

The dashboard includes:

1. **Unemployment Rate by Year and Month** – Visualizes unemployment trends over time.
2. **Unemployment Rate by Area** – Compares rural and urban unemployment rates.
3. **Average Employed by States** – Displays average employment estimates for states.
4. **Average Unemployment Rate by States** – Identifies states with higher unemployment rates.
5. **Average Employed by Area** – Compares rural and urban employment estimates.
6. **Top 5 Labour Participation States** – Highlights states with the highest average labour participation rates.

### Interactive Features

- State selection filter.
- Date selection filter.
- Rural and urban area filter.
- Key Performance Indicator (KPI) cards.
- Interactive Plotly visualizations.
- Filtered dataset viewer.
- CSV download option.

## 📂 Project Structure

```text
CodeAlpha_UnemploymentAnalysis/
│
├── data/
│   ├── Unemployment in India.csv
│   └── Unemployment_Rate_upto_11_2020.csv
│
├── outputs/
│   ├── cleaned_unemployment_india.csv
│   └── cleaned_unemployment_2020.csv
│
├── main.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vidya0210/CodeAlpha_UnemploymentAnalysis.git
```

### 2. Navigate to the project folder

```bash
cd CodeAlpha_UnemploymentAnalysis
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the data cleaning script

```bash
python main.py
```

This generates the cleaned datasets inside the `outputs/` directory.

### 5. Launch the interactive dashboard

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your web browser, usually at:

```text
http://localhost:8501
```

## 📊 Key Insights

The dashboard helps explore:

- Changes in unemployment rates over the available observation period.
- Differences between rural and urban unemployment.
- State-wise variations in unemployment.
- Differences in average employment estimates across states.
- Labour participation patterns across regions.

**Note:** The dashboard displays averages calculated from the available dataset observations. These values should not be interpreted as official national employment totals.

## 📚 Dataset

The project uses two unemployment datasets:

- `Unemployment in India.csv`
- `Unemployment_Rate_upto_11_2020.csv`

The datasets contain information such as:

- Region
- Date
- Frequency
- Estimated Unemployment Rate (%)
- Estimated Employed
- Estimated Labour Participation Rate (%)
- Area

The dashboard currently uses the cleaned first dataset for its six visualizations. The second dataset is retained for additional 2020 analysis.

## 🎓 Internship Information

**Program:** CodeAlpha Data Science Internship  
**Task:** Task 2 – Unemployment Analysis with Python  
**Domain:** Data Science

## 👩‍💻 Author

**Vidyalakshmee Beerappa Habagonde**

Computer Science and Engineering Student  
Interested in Data Science, Python, Data Analytics and Machine Learning.

## ⭐ Acknowledgement

Thanks to CodeAlpha for providing the opportunity to work on this Data Science project and improve practical data analytics skills.

---

_Built with Python, Streamlit, Pandas and Plotly._
