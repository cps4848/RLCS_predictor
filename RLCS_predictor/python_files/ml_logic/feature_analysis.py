import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def get_correlation(data):
    # Apply Standard Scaler

    data = data.drop(columns=['team name_1', 'team name_2', 'replay title', 'date', 'map'])

    scaler = StandardScaler()

    scaled_df = scaler.fit_transform(data)
    scaled_df = pd.DataFrame(scaled_df, columns=data.columns)

    # Showing the Correlation Matrix

    correlation_matrix = data.corr()
    column_names = correlation_matrix.columns
    f, ax = plt.subplots(figsize=(50, 50))
    print(sns.heatmap(correlation_matrix, xticklabels=column_names, yticklabels=column_names,cmap= "bwr", annot=True, annot_kws={"size":17}))
