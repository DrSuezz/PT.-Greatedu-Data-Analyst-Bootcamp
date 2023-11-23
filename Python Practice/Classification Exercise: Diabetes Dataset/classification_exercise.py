# -*- coding: utf-8 -*-
"""Classification_Exercise.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s5HHSyY9M6oIhek-yTsNjoR94t2hjgyS

Dataset
https://drive.google.com/file/d/1Q7864_fB43EktRQQRFcJ04f1QRgCle2n/view?usp=sharing
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

from google.colab import drive
drive.mount('/content/gdrive')

# Load your CSV data
data = pd.read_csv('/content/gdrive/MyDrive/SIB Greatedu praktik/classi/diabetes - training.csv')
data.set_index("id", inplace=True)



data

# Assuming your target column is named 'target'
X = data.drop('Outcome', axis=1)
y = data['Outcome']

y

# Encode categorical variables if necessary
# If your dataset contains categorical variables, you may need to encode them.
# For simplicity, let's assume all features are numeric.

# Split the dataset into a training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

X_test

y_test

"""Menggunakan Classifier untuk prediksi"""

# K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)

# Decision Tree
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)

# Random Forest
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

# XGBoost
xgb_model = xgb.XGBClassifier()
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

actual = y_test  # Actual target values
# Create confusion matrices
knn_cm = confusion_matrix(actual, knn_pred)
dt_cm = confusion_matrix(actual, dt_pred)
rf_cm = confusion_matrix(actual, rf_pred)
xgb_cm = confusion_matrix(actual, xgb_pred)

# Convert confusion matrices to DataFrames
def confusion_matrix_to_dataframe(cm):
    labels = sorted(set(actual))
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)
    df_cm.index.name = 'Actual'
    df_cm.columns.name = 'Predicted'
    return df_cm

# Convert confusion matrices to DataFrames with labels
knn_cm_df = confusion_matrix_to_dataframe(knn_cm)
dt_cm_df = confusion_matrix_to_dataframe(dt_cm)
rf_cm_df = confusion_matrix_to_dataframe(rf_cm)
xgb_cm_df = confusion_matrix_to_dataframe(xgb_cm)

knn_cm

knn_cm_df

dt_cm_df

rf_cm_df

xgb_cm_df

"""Mengukur akurasi dari tiap metode untuk classifier"""

def evaluate(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    return cm, accuracy, precision, recall, f1


# Evaluate KNN
knn_cm, knn_accuracy, knn_precision, knn_recall, knn_f1 = evaluate(y_test, knn_pred)

# Evaluate Decision Tree
dt_cm, dt_accuracy, dt_precision, dt_recall, dt_f1 = evaluate(y_test, dt_pred)

# Evaluate Random Forest
rf_cm, rf_accuracy, rf_precision, rf_recall, rf_f1 = evaluate(y_test, rf_pred)

# Evaluate XGBoost
xgb_cm, xgb_accuracy, xgb_precision, xgb_recall, xgb_f1 = evaluate(y_test, xgb_pred)

knn_f1

dt_f1

rf_f1

xgb_f1

xgb_feature_importance = xgb_model.feature_importances_
feature_names = X.columns

xgb_feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': xgb_feature_importance})
xgb_feature_importance_df = xgb_feature_importance_df.sort_values(by='Importance', ascending=False)
xgb_feature_importance_df

# Load your new data from a CSV file
new_data = pd.read_csv('/content/gdrive/MyDrive/SIB Greatedu praktik/classi/diabetes - to_predict.csv')
new_data.set_index("id", inplace=True)
new_data

# Assuming your new data has the same features as your original data (except the target)

# Make predictions using the trained models
knn_predictions = knn.predict(new_data)
dt_predictions = dt.predict(new_data)
rf_predictions = rf.predict(new_data)
xgb_predictions = xgb_model.predict(new_data)


combined_data = new_data.copy()  # Copy the new dataset

# Add columns for predicted labels
combined_data['KNN_Predictions'] = knn_predictions
combined_data['DT_Predictions'] = dt_predictions
combined_data['RF_Predictions'] = rf_predictions
combined_data['XGB_Predictions'] = xgb_predictions

combined_data