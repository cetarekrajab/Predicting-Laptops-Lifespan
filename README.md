# Predicting-Laptops-Lifespan

A Python-based end-to-end data science project analyzing hardware longevity. Features automated data preprocessing pipelines, predictive machine learning models, and an interactive Power BI dashboard to deliver actionable sustainability and performance insights.

---

## 📂 Project Structure

* **data/**: Contains raw and cleaned datasets (`device_sustainability.csv`, `device_sustainability_deduped.csv`, `final.csv`).
* **dashboard/**: Stores layout screenshots (`d1.png` to `d3.png`) and the Power BI report file (`Laptop_Lifespan_Analysis.pbix`).


* **models/**: Houses serialized machine learning models and scalers (`best_model.pkl`, `best_model_without_year.pkl`, `scaler.pkl`, `scaler_without_year.pkl`).
* **output/**: Stores generated result images (`result1.png` through `result6.png`).
* **reports/**: Includes project documentation such as the `Industrial Training Report.pdf`.
* **src/**: Holds Python source code files (`pipeline.py`, `predecting.py`, `training.py`, `training2.py`, `visualizations.py`).
* **visualizations/**: Contains generated EDA charts and statistical plots (from `01_avg_lifespan.png` to `10_correlation_heatmap.png`).
* **Configuration Files**: Root-level `README.md` and `requirements.txt`.

---

## 📊 Key Highlights

* **Data Engineering & ML (`Python`)**: Automated cleaning, preprocessing, and feature engineering pipelines, with serialized machine learning models for predictive longevity forecasting.
* **Business Intelligence (`Power BI`)**: Features an interactive reporting suite (`Laptop_Lifespan_Analysis.pbix`) built on structured model components to visualize sustainability metrics.


* **Exploratory Data Analysis**: Generates comprehensive visual outputs and statistical correlations mapping operational parameters to device sustainability.

---

## 🛠️ Tech Stack

* **Languages:** Python, DAX, M
* **Libraries:** Pandas, Scikit-learn, Matplotlib, Seaborn
* **BI Tool:** Power BI
