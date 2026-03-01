import requests
import json

API_URL = "http://127.0.0.1:8000/predict"

# ---------------- TEST CASES ----------------

test_cases = [
    # LOW RISK
    ("I forgot my PIN", "change_pin", "LOW_RISK"),
    ("I want to activate my card", "activate_my_card", "LOW_RISK"),
    ("I need a virtual card", "getting_virtual_card", "LOW_RISK"),

    # CRITICAL
    ("My card was stolen", "lost_or_stolen_card", "CRITICAL"),
    ("My card is compromised", "compromised_card", "CRITICAL"),

    # HIGH RISK
    ("I was charged twice", "transaction_charged_twice", "HIGH_RISK"),
    ("I did not receive my refund", "refund_not_showing_up", "HIGH_RISK"),

    # OUT OF DOMAIN
    ("Tell me about dinosaurs", "NO_INFORMATION_AVAILABLE", "OUT_OF_DOMAIN"),
    ("Who won the cricket match", "NO_INFORMATION_AVAILABLE", "OUT_OF_DOMAIN"),
]

# ---------------- TEST RUN ----------------

passed = 0
failed = 0

print("\n===== RUNNING INTENT TESTS =====\n")

for query, expected_intent, expected_risk in test_cases:

    response = requests.post(API_URL, json={"query": query})

    if response.status_code != 200:
        print(f"[ERROR] {query} -> HTTP {response.status_code}")
        failed += 1
        continue

    result = response.json()

    predicted_intent = result.get("intent")
    predicted_risk = result.get("risk_level")

    intent_match = predicted_intent == expected_intent
    risk_match = predicted_risk == expected_risk

    if intent_match and risk_match:
        print(f"[PASS] {query}")
        passed += 1
    else:
        print(f"[FAIL] {query}")
        print(f"   Expected: {expected_intent} / {expected_risk}")
        print(f"   Got:      {predicted_intent} / {predicted_risk}")
        failed += 1

print("\n===== TEST SUMMARY =====")
print(f"Passed: {passed}")
print(f"Failed: {failed}")