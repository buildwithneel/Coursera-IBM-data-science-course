# SpaceX Falcon 9 First Stage Landing Prediction: Model Evaluation Report

## 1. Executive Summary & Problem Formulation
- **Objective:** Train, evaluate, and tune supervised machine learning classifiers to predict whether the Falcon 9 first stage booster will land successfully (`Class = 1`) or be expended / lost (`Class = 0`).
- **Business Impact:** Reusable first stages save SpaceX approximately $40M to $50M per launch ($62M list price vs. ~$165M competitors). Predicting recovery feasibility informs mission bidding, insurance premiums, and recovery fleet dispatch.
- **Dataset Splitting:** 
  - Total Samples: 90 launches
  - Training Set: 72 launches (80%)
  - Held-out Test Set: 18 launches (20%)
  - Stratification applied to ensure equal class proportions in both partitions.
  - Leakage Prevention: `StandardScaler` fitted strictly on the training partition and transformed on test data.

## 2. Supervised Learning Models Evaluated
1. **Logistic Regression (L2 regularized)**: Baseline linear probabilistic classifier.
2. **Support Vector Machine (SVM)**: Optimal margin hyperplane classifier evaluating linear, radial basis (RBF), and sigmoid kernels.
3. **Decision Tree Classifier**: Non-linear, interpretable tree-based partitioning.
4. **K-Nearest Neighbors (KNN)**: Non-parametric distance-based instance classifier.

## 3. Comparative Evaluation Results

| Model Architecture | 10-Fold CV Train Accuracy | Test Accuracy | Precision (Class 1) | Recall (Class 1) | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 85.00% | 83.33% | 0.800 | 1.000 | 0.889 | 0.833 |
| **Support Vector Machine** | 86.43% | 77.78% | 0.750 | 1.000 | 0.857 | 0.931 |
| **Decision Tree** | 83.57% | 77.78% | 0.786 | 0.917 | 0.846 | 0.708 |
| **K-Nearest Neighbors** | 86.43% | 83.33% | 0.800 | 1.000 | 0.889 | 0.771 |

## 4. Best Performing Model: K-Nearest Neighbors
- **Optimal Hyperparameters:** `{"algorithm": "auto", "n_neighbors": 3, "p": 1}`
- **Held-Out Test Accuracy:** **83.3%**
- **F1-Score:** **0.889**
- **Test Confusion Matrix (N=18):**
  - True Negatives (Correctly predicted failure): `3`
  - False Positives (Incorrectly predicted success): `3`
  - False Negatives (Incorrectly predicted failure): `0`
  - True Positives (Correctly predicted success): `12`

## 5. Detailed Classification Reports

### Logistic Regression
```text
              precision    recall  f1-score   support

 Failure (0)       1.00      0.50      0.67         6
 Success (1)       0.80      1.00      0.89        12

    accuracy                           0.83        18
   macro avg       0.90      0.75      0.78        18
weighted avg       0.87      0.83      0.81        18

```

### Support Vector Machine
```text
              precision    recall  f1-score   support

 Failure (0)       1.00      0.33      0.50         6
 Success (1)       0.75      1.00      0.86        12

    accuracy                           0.78        18
   macro avg       0.88      0.67      0.68        18
weighted avg       0.83      0.78      0.74        18

```

### Decision Tree
```text
              precision    recall  f1-score   support

 Failure (0)       0.75      0.50      0.60         6
 Success (1)       0.79      0.92      0.85        12

    accuracy                           0.78        18
   macro avg       0.77      0.71      0.72        18
weighted avg       0.77      0.78      0.76        18

```

### K-Nearest Neighbors
```text
              precision    recall  f1-score   support

 Failure (0)       1.00      0.50      0.67         6
 Success (1)       0.80      1.00      0.89        12

    accuracy                           0.83        18
   macro avg       0.90      0.75      0.78        18
weighted avg       0.87      0.83      0.81        18

```


## 6. Analytical Insights & Limitations
1. **Class Imbalance Consideration**: With a 66.7% success baseline across the dataset, predicting the majority class naively yields ~66.7% accuracy. Our best tuned classifiers achieved superior predictive accuracy and high precision/recall on test data.
2. **Key Predictive Signals**:
   - `GridFins` and `Legs` deployment capability.
   - `FlightNumber` / chronological flight progression (learning curve effects).
   - Reused booster experience (`ReusedCount`, `Flights`).
   - Specific target orbit profiles (e.g. LEO/ISS vs heavy GTO).
3. **Dataset Size Limitations**: With 90 total launches, the test partition contains 18 samples. While 10-fold cross validation stabilizes variance, future expansion as SpaceX launches hundreds more missions will enhance generalization on rare failure modes.
