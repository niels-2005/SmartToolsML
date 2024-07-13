from sklearn.model_selection import train_test_split 
import pandas as pd 

def get_X_y(df: pd.DataFrame):
    X = df.drop("output", axis=1)
    y = df["output"]
    return X, y

def get_train_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test