import pandas as pd


transactions = pd.read_csv("transactions.csv")
settlements = pd.read_csv("settlements.csv")

# Convert to datetime
transactions["date"] = pd.to_datetime(transactions["date"], dayfirst=True)
settlements["settlement_date"] = pd.to_datetime(settlements["settlement_date"], dayfirst=True)

# -----------------------------
# 2. Missing Settlements
# -----------------------------
missing_settlements = transactions[
    ~transactions["transaction_id"].isin(settlements["transaction_id"])
]

# -----------------------------
# 3. Extra Settlements
# -----------------------------
extra_settlements = settlements[
    ~settlements["transaction_id"].isin(transactions["transaction_id"])
]

# -----------------------------
# 4. Duplicate Settlements
# -----------------------------
duplicate_settlements = settlements[
    settlements.duplicated(subset=["transaction_id"], keep=False)
]

# -----------------------------
# 5. Merge Data
# -----------------------------
merged = pd.merge(
    transactions,
    settlements,
    on="transaction_id",
    how="inner",
    suffixes=("_txn", "_settle")
)

# -----------------------------
# 6. Rounding Issues
# -----------------------------
rounding_issues = merged[
    (merged["amount_txn"] - merged["amount_settle"]).abs() > 0.01
]

# -----------------------------
# 7. Cross-Month Settlements
# -----------------------------
cross_month = merged[
    merged["date"].dt.month != merged["settlement_date"].dt.month
]

# -----------------------------
# 8. Save Results to CSV 
# -----------------------------
missing_settlements.to_csv("missing_settlements.csv", index=False)
extra_settlements.to_csv("extra_settlements.csv", index=False)
duplicate_settlements.to_csv("duplicate_settlements.csv", index=False)
rounding_issues.to_csv("rounding_issues.csv", index=False)
cross_month.to_csv("cross_month.csv", index=False)

# -----------------------------
# 9. Print Summary
# -----------------------------
print("\n===== RECONCILIATION REPORT =====\n")

print(f"Missing Settlements: {len(missing_settlements)}")
print(f"Extra Settlements: {len(extra_settlements)}")
print(f"Duplicate Settlements: {duplicate_settlements['transaction_id'].nunique()}")
print(f"Rounding Issues: {len(rounding_issues)}")
print(f"Cross-Month Settlements: {len(cross_month)}")

print("\n✅ Detailed reports saved as CSV files.")