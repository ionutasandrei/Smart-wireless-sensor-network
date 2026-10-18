
import numpy as np
from sklearn.ensemble import IsolationForest


class EdgeAI:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        self.trained = False

    def train(self, data):
        """Antreneaza modelul pe datele senzorilor."""
        X = np.asarray(data, dtype=float)
        self.model.fit(X)
        self.trained = True

    def detect(self, co2, temp, light):
        """Detecteaza anomalii folosind trei senzori."""
        if not self.trained:
            raise RuntimeError("Modelul AI nu este antrenat.")

        X = np.array([[co2, temp, light]], dtype=float)
        prediction = self.model.predict(X)[0]

        return int(prediction == -1)
