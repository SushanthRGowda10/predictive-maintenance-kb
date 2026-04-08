# ✅ Test Cases

| Test ID | Input Condition | Expected Output |
|---|---|---|
| TC01 | Normal sensor values | Healthy |
| TC02 | High vibration | Medium Risk |
| TC03 | High temp + vibration | High Risk |
| TC04 | Negative input | Validation Error |
| TC05 | Missing value | Safe default handling |
| TC06 | Runtime > threshold | Warning |
| TC07 | Pump with high pressure | Failure Likely |

## Result
All test cases passed successfully.