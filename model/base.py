import joblib
import numpy as np
import os
import pandas as pd

from dataclasses import dataclass
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from typing import Any, Callable, List, Optional


class Dataset:
    data: pd.DataFrame
    dataset_name: str
    features: List[str]
    target: str
    test_size: float
    x_test: pd.DataFrame = None
    x_train: pd.DataFrame = None
    y_test: pd.DataFrame = None
    y_train: pd.DataFrame = None

    def __init__(self, data: pd.DataFrame, dataset_name: str, target: str, storage_path: Optional[str],
                 test_size: Optional[float] = 0.3):
        self.data = data
        self.dataset_name = dataset_name
        self.target = target
        features = self.data.columns.tolist()
        features.remove(self.target)
        self.features = features
        self.test_size = test_size
        self.x_train, self.x_test, self.y_train, self.y_test = self.save_split(storage_path)

    def save_split(self, path: Optional[str]) -> tuple[Optional[pd.DataFrame], ...]:
        if path:
            x = self.data[self.features]
            y = self.data[self.target]
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=self.test_size)
            now = datetime.now()
            name = f'{now.year}.{now.month}.{now.day}_{now.hour}-{now.minute}-{now.second}_'
            pd.concat([x_train, y_train], axis=1).to_excel(f'{path}/{name}train_{self.dataset_name}.xlsx')
            pd.concat([x_test, y_test], axis=1).to_excel(f'{path}/{name}test_{self.dataset_name}.xlsx')
            return x_train, x_test, y_train, y_test
        return None, None, None, None


@dataclass
class Model:
    base_estimator: Any
    estimator_id: int
    estimator_name: str
    params: dict


class Preprocessing:
    cat: list
    dataset: pd.DataFrame
    column_transformer: ColumnTransformer
    fill_func: Callable
    fill_values: dict
    num: list
    to_binarize: Optional[np.array] = None

    def __init__(self, dataset: pd.DataFrame, fill_func: Callable = np.mean):
        self.dataset = dataset
        self.num = self.dataset.select_dtypes(['int64', 'float64']).columns.tolist()
        self.cat = self.dataset.select_dtypes(['object', 'string']).columns.tolist()
        self.fill_func = fill_func
        self.column_transformer = ColumnTransformer([
            ('ohe', OneHotEncoder(handle_unknown="ignore"), self.cat),
            ('scaling', StandardScaler(), self.num)
        ])
        self.to_binarize = np.array(self.dataset.columns)[
            (self.dataset.isna().sum() / self.dataset.shape[0] > 0.5).values]
        self.fill_values = dict(self.fill_func(self.dataset[self.num]))

    def fit_transform(self, x_train: pd.DataFrame) -> pd.DataFrame:
        x_train[self.cat] = x_train[self.cat].astype(str)
        x_train[self.num] = x_train[self.num].astype(float)
        x_train[self.to_binarize] = x_train[self.to_binarize].isna().astype(int)
        x_train[self.num] = x_train[self.num].fillna(value=self.fill_values)
        x_train[self.cat] = x_train[self.cat].fillna(-1000)
        x_train = self.column_transformer.fit_transform(x_train)
        return x_train

    def transform(self, x_test: pd.DataFrame) -> pd.DataFrame:
        x_test[self.cat] = x_test[self.cat].astype(str)
        x_test[self.num] = x_test[self.num].astype(float)
        x_test[self.to_binarize] = x_test[self.to_binarize].isna().astype(int)
        x_test[self.cat] = x_test[self.cat].fillna(-1)
        x_test[self.num] = x_test[self.num].fillna(value=self.fill_values)
        x_test = self.column_transformer.transform(x_test)
        return x_test


class Pipe:
    dataset: Dataset
    estimator: Any
    model: Model
    params: Optional[dict] = None
    preprocessing: Preprocessing

    def __init__(self, dataset: Dataset, model: Model):
        self.dataset = dataset
        self.model = model
        self.preprocessing = Preprocessing(self.dataset.x_train)

    def fit(self, params: Optional[dict] = None, path: Optional[str] = None):
        x_train = self.preprocessing.fit_transform(self.dataset.x_train)
        if params:
            estimator = self.model.base_estimator(**params)
            self.params = params
        else:
            estimator = self.model.base_estimator()
        self.estimator = estimator.fit(x_train, self.dataset.y_train)
        self.save_model(path)

    def save_model(self, path: Optional[str] = None):
        if not path:
            path = os.getcwd() + '/res/estimated_models'
        now = datetime.now()
        filename = f'{now.year}.{now.month}.{now.day}_{now.hour}-{now.minute}-{now.second}_{self.model.estimator_name}'
        joblib.dump(self, path + '/' + filename + '_model.pkl')

    def predict(self, path: Optional[str] = None):
        x_test = self.preprocessing.transform(self.dataset.x_test)
        y_predict = self.estimator.predict(x_test)
        self.save_predict(y_predict, path)

    def save_predict(self, prediction: pd.Series, path: Optional[str] = None):
        if not path:
            path = os.getcwd() + '/res/prediction'
        now = datetime.now()
        filename = f'{now.year}.{now.month}.{now.day}_{now.hour}-{now.minute}-{now.second}_{self.model.estimator_name}'
        pd.Series(prediction).to_excel(path + '/' + filename + '_predictions.xlsx')


base_estimators = {
    1: Lasso,
    2: LinearRegression,
    3: Ridge
}
