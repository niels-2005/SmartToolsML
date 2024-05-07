import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor, ExtraTreesRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import (
    make_scorer,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

pipelines = [
    Pipeline([("scaler", StandardScaler()), ("reg", LinearRegression())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", LinearRegression())]),
    Pipeline([("scaler", RobustScaler()), ("reg", LinearRegression())]),
    Pipeline([("scaler", StandardScaler()), ("reg", AdaBoostRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", AdaBoostRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", AdaBoostRegressor())]),
    Pipeline([("scaler", StandardScaler()), ("reg", ExtraTreesRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", ExtraTreesRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", ExtraTreesRegressor())]),
    Pipeline([("scaler", StandardScaler()), ("reg", Ridge())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", Ridge())]),
    Pipeline([("scaler", RobustScaler()), ("reg", Ridge())]),
    Pipeline([("scaler", StandardScaler()), ("reg", Lasso())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", Lasso())]),
    Pipeline([("scaler", RobustScaler()), ("reg", Lasso())]),
    Pipeline([("scaler", StandardScaler()), ("reg", ElasticNet())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", ElasticNet())]),
    Pipeline([("scaler", RobustScaler()), ("reg", ElasticNet())]),
    Pipeline([("scaler", StandardScaler()), ("reg", SVR())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", SVR())]),
    Pipeline([("scaler", RobustScaler()), ("reg", SVR())]),
    Pipeline([("scaler", StandardScaler()), ("reg", RandomForestRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", RandomForestRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", RandomForestRegressor())]),
    Pipeline([("scaler", StandardScaler()), ("reg", GradientBoostingRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", GradientBoostingRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", GradientBoostingRegressor())]),
    Pipeline([("scaler", StandardScaler()), ("reg", KNeighborsRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", KNeighborsRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", KNeighborsRegressor())]),
    Pipeline([("scaler", StandardScaler()), ("reg", DecisionTreeRegressor())]),
    Pipeline([("scaler", MinMaxScaler()), ("reg", DecisionTreeRegressor())]),
    Pipeline([("scaler", RobustScaler()), ("reg", DecisionTreeRegressor())]),
]


def compare_pipelines(
    X_train: np.ndarray,
    y_train: np.ndarray,
    cv,
    metric: str = "MSE",
    plot_comparison: bool = True,
    return_df: bool = False,
) -> pd.DataFrame:
    """
    Compares multiple machine learning pipelines on the given training data using cross-validation and optionally plots the comparison for a specified metric. Optionally returns a DataFrame containing the results.

    Args:
        X_train (np.ndarray): The training input samples.
        y_train (np.ndarray): The target labels for the training input samples.
        cv (object): Cross-validation splitting strategy, such as KFold or StratifiedKFold.
        metric (str): Scoring metric to evaluate the models. Default is 'MSE'.
        plot_comparison (bool): If True, plot the metric comparison as a horizontal bar chart.
        return_df (bool): If True, returns a DataFrame containing the evaluation results.

    Returns:
        pd.DataFrame or None: Returns a DataFrame with the pipeline descriptions, metrics, and scores if return_df is True, otherwise returns None.

    Example usage:
        from sklearn.model_selection import KFold
        cv = KFold(n_splits=5)
        metrics = ["MSE", "MAE", "R2"]
        for met in metrics:
            df = compare_pipelines(X_train, y_train, cv=cv, metric=met, plot_comparison=True, return_df=True)
    """
    scorer = {
        "MSE": make_scorer(mean_squared_error, greater_is_better=False),
        "MAE": make_scorer(mean_absolute_error, greater_is_better=False),
        "R2": make_scorer(r2_score),
    }[metric]

    pipeline_descriptions = []
    scores = []

    for idx, pipeline in enumerate(pipelines):
        step_names = " | ".join([type(step[1]).__name__ for step in pipeline.steps])
        cv_scores = cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring=scorer
        ).mean()
        pipeline_descriptions.append(step_names)
        scores.append(cv_scores)
        print(f"Pipeline {idx + 1}: {step_names}, {metric}: {cv_scores:.4f}")

    if plot_comparison:
        zipped_lists = zip(scores, pipeline_descriptions)
        sorted_pairs = sorted(zipped_lists, reverse=True, key=lambda x: x[0])
        sorted_scores, sorted_names = zip(*sorted_pairs)

        plt.figure(figsize=(10, 8))
        bars = plt.barh(sorted_names, sorted_scores, color="skyblue")
        for bar in bars:
            plt.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.4f}",
                va="center",
            )
        plt.xlabel(f"{metric.capitalize()}")
        plt.title(f"{metric} Performance Comparison")
        plt.xlim(min(sorted_scores), max(sorted_scores) if metric != "R2" else 1)
        plt.gca().invert_yaxis()
        plt.show()

    if return_df:
        results_df = pd.DataFrame(
            {"Pipeline": pipeline_descriptions, "Metric": metric, "Score": scores}
        )
        return results_df
    return None
