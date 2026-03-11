
#  Google Play Store Analytics Dashboard

An interactive data analysis and recommendation system built with Python and Streamlit to explore the Google Play Store dataset. This project includes comprehensive Exploratory Data Analysis (EDA), machine learning-based clustering, and a smart app recommendation engine.

##  Features

- **EDA Analysis**: Visualizes key metrics like total apps, categories, reviews, and average ratings using Plotly.
- **Clustering Insights**: Groups apps into meaningful categories (e.g., "Popular Free", "Top Free", "Paid Moderate") based on engagement and installs.
- **App Recommendation System**: A Recommendation System Content-based with simularty  to find apps based on category, type (Free/Paid), and minimum rating.
- **Data Visualizations**: Interactive histograms, boxplots, and heatmaps created with Seaborn and Matplotlib during the initial analysis.

##  Tech Stack

- **Language**: Python
- **Dashboard**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Machine Learning**: Scikit-learn (KMeans clustering, StandardScaler)

##  Project Structure

- `app.py`: The main Streamlit application file.
- `eda_notebook.ipynb`: Jupyter notebook containing the initial data cleaning and analysis.
- `clean_apps.csv`: The processed dataset used by the dashboard.
- `requirements.txt`: List of Python dependencies.

