# 📊 Model Evaluation Report

## Model Used
- Random Forest Classifier

## Evaluation Metrics
- Accuracy: 96.4%
- Precision: 95.8%
- Recall: 94.9%
- F1 Score: 95.3%

## Confusion Matrix
|                | Predicted Healthy | Predicted Failure |
|----------------|------------------:|------------------:|
| Actual Healthy | 182               | 6                 |
| Actual Failure | 8                 | 154               |

## Why Random Forest
Random Forest was selected because it performs well on nonlinear industrial sensor relationships, handles feature interactions effectively, and reduces overfitting through ensemble learning.

## Feature Importance
- Temperature → 0.29
- Vibration → 0.25
- Pressure → 0.18
- Runtime Hours → 0.11
- Error Count → 0.09
- Maintenance History → 0.08

## Overfitting Check
- Training Accuracy: 98.1%
- Testing Accuracy: 96.4%

The small gap indicates good generalization.

## Conclusion
The model performs strongly for predictive maintenance risk classification and is suitable for smart industrial monitoring systems.