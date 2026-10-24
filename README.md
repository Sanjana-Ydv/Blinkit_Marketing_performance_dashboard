# Marketing_performance_dashboard
A data analytics dashboard that tracks and compares marketing campaign performance across channels, built as the SkillOrbit Data Analytics Capstone Project.

Live dashboard: https://marketingperformancedashboard-nycdhmh5l2x2rj8ew5d3m5.streamlit.app/

# Objective
1. Analyze marketing campaign data
2. Track engagement metrics (CTR, conversion rate)
3. Monitor campaign performance (ROI, ROAS)
4. Compare marketing channels
5. Generate reports and business insights

# Dataset
Blinkit marketing performance dataset from Kaggle (5,400 campaign records, March 2023 to November 2024).
# Columns: campaign ID, campaign name, date, target audience, channel, impressions, clicks, conversions, spend, revenue.

# Workflow
1. Data Collectin: Downloaded the dataset from Kaggle
2. Data cleaning: Checked missing values and duplicates, converted dates, renamed columns, validated values (no clicks above impressions, no negative spend)
3. KPI analysis: Calculated CTR, conversion rate, cost per click, cost per conversion, ROAS, and ROI
4. Dashboard: Built an interactive Streamlit dashboard with filters, KPI cards, and charts
5. Insights and reports: Business insights and downloadable CSV reports

# Key Findings
* The original `roas` column did not match revenue / spend in 5,374 of 5,400 rows, so ROAS was recalculated.

* Email had the highest ROI (about 105%) and App the lowest (about 92%).
* Referral Program was the best campaign by ROI (about 103%).
* Differences between channels and campaigns are small, so they should be treated as hints, not firm conclusions.

# Project Files
=================FILES=======================|================PURPOSES==================
---------------------------------------------|---------------------------------------
 `app.py`                                    | Streamlit dashboard 
 `requirements.txt`                          | Python libraries needed 
 `cleaned_data.csv`                          | Cleaned data used by the dashboard 
 `blinkit_marketing_performance.csv`         | Original dataset 
 `Marketing_Performance_Major_Project.ipynb` | Cleaning and KPI analysis notebook 

# Run Locally
             pip install-r requirements.txt
             streamlit run app.py

# Tech Stack
Python, Pandas, Plotly, Streamlit, Google Colab, GitHub

# BY:
SANJANA_YADAV

 NOTE: I would like to thank SkillOrbit and Unlox Academy for this project opportunity. I had also used Claude (AI Assistance) for guidance during the project, as this is my first experience with all these. I ran the analysis, deployed the dashboard and finalized the PPT and this report by myself. 
