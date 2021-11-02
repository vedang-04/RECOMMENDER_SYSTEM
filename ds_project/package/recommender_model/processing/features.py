import cv2
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from package.image_classification_model.config.core import config


def _im_resize(df, n, target_size):
    im = cv2.imread(df.iloc[n].image_name) / config.model_config.rescaling_factor
    im = cv2.resize(im, (target_size, target_size))
    return im


class CreateDataset(BaseEstimator, TransformerMixin):
    def __init__(self, target_size):
        self.target_size = target_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        tmp = np.zeros((len(X), self.target_size, self.target_size, 3), dtype="float32")

        for n in range(0, len(X)):
            im = _im_resize(X, n, self.target_size)
            tmp[n] = im

        return tmp
