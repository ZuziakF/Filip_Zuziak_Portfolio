import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score

from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

def prepare_data(filepath):
    df = pd.read_csv(filepath, sep=';', decimal=',')
    for col in df.columns:
        if df[col].dtype == 'object' and col != 'Data':
            df[col] = df[col].str.replace(',', '.').astype(float)
    
    X = df.drop(columns=['Data', 'Target_Regresja', 'Target_Klasyfikacja']).values
    y_reg = df['Target_Regresja'].values
    y_clf = df['Target_Klasyfikacja'].values
    
    return X, y_reg, y_clf

X_raw, y_reg, y_clf = prepare_data('xauusd_dla_excela.csv')

X_train_raw, X_test_raw, y_reg_train, y_reg_test = train_test_split(X_raw, y_reg, test_size=0.2, shuffle=False)
_, _, y_clf_train, y_clf_test = train_test_split(X_raw, y_clf, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_raw)
X_test = scaler.transform(X_test_raw)

print("ROZPOCZYNANIE ANALIZY DLA 4 METOD (UM)\n")

experiments = [
    {
        "name": "1. k-Nearest Neighbors",
        "param_name": "n_neighbors (Liczba sąsiadów)",
        "values": [3, 5, 11, 21],
        "clf_class": KNeighborsClassifier,
        "reg_class": KNeighborsRegressor,
        "arg_name": "n_neighbors"
    },
    {
        "name": "2. Decision Tree",
        "param_name": "max_depth (Głębokość drzewa)",
        "values": [3, 5, 10, 20],
        "clf_class": DecisionTreeClassifier,
        "reg_class": DecisionTreeRegressor,
        "arg_name": "max_depth"
    },
    {
        "name": "3. Random Forest",
        "param_name": "n_estimators (Liczba drzew)",
        "values": [10, 50, 100, 200],
        "clf_class": RandomForestClassifier,
        "reg_class": RandomForestRegressor,
        "arg_name": "n_estimators"
    },
    {
        "name": "4. SVM",
        "param_name": "C (Parametr regularyzacji)",
        "values": [0.1, 1.0, 10.0, 100.0],
        "clf_class": SVC,
        "reg_class": SVR,
        "arg_name": "C"
    }
]

for exp in experiments:
    print(f"--- Metoda: {exp.get('name', exp.get('nami'))} ---")
    print(f"{'Wartość':<10} | {'Regresja MSE (RMSE)':<27} | {'Klasyfikacja (ACC)':<18}")
    print("-" * 60)
    
    for val in exp['values']:
        params = {exp['arg_name']: val}
        
        reg_model = exp['reg_class'](**params)
        reg_model.fit(X_train, y_reg_train)
        y_reg_pred = reg_model.predict(X_test)
        mse = mean_squared_error(y_reg_test, y_reg_pred)
        rmse = np.sqrt(mse)
        
        clf_model = exp['clf_class'](**params)
        clf_model.fit(X_train, y_clf_train)
        y_clf_pred = clf_model.predict(X_test)
        acc = accuracy_score(y_clf_test, y_clf_pred) * 100
        
        reg_str = f"{mse:<12.4f} ({rmse:<7.2f})"
        print(f"{str(val):<10} | {reg_str:<27} | {acc:<17.2f}%")
    print("\n")