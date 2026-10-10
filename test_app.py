import unittest

from app import app

HIGH_RISK_PATIENT = {
    "Age": 70,
    "Gender": "Male",
    "Height_cm": 168,
    "Weight_kg": 105,
    "BP": "High",
    "Cholesterol": 280,
    "Glucose": 200,
    "Smoking": "Yes",
    "ExerciseLevel": "Low",
    "BMI": 37.2
}

LOW_RISK_PATIENT = {
    "Age": 25,
    "Gender": "Female",
    "Height_cm": 165,
    "Weight_kg": 55,
    "BP": "Normal",
    "Cholesterol": 130,
    "Glucose": 80,
    "Smoking": "No",
    "ExerciseLevel": "High",
    "BMI": 20.2
}


class TestPredictionApplication(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_high_risk_prediction(self):
        response = self.client.post("/predict", json=HIGH_RISK_PATIENT)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "HIGH RISK")

    def test_low_risk_prediction(self):
        response = self.client.post("/predict", json=LOW_RISK_PATIENT)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["prediction"], "LOW RISK")

    def test_missing_field_validation(self):
        response = self.client.post(
            "/predict",
            json={"Age": 50, "Gender": "Male"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.get_json())

    def test_invalid_category_validation(self):
        bad_patient = dict(LOW_RISK_PATIENT)
        bad_patient["Gender"] = "Unknown"

        response = self.client.post("/predict", json=bad_patient)

        self.assertEqual(response.status_code, 400)
        self.assertIn("allowed_values", response.get_json())


if __name__ == "__main__":
    unittest.main()
