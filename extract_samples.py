import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='extract_samples.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset
try:
    data = pd.read_csv("web_attacks_balanced.csv")
except FileNotFoundError:
    logging.error("web_attacks_balanced.csv not found.")
    print("Error: web_attacks_balanced.csv not found.")
    exit(1)

# Verify dataset
if 'Label' not in data.columns:
    logging.error("'Label' column not found in dataset.")
    print("Error: 'Label' column not found in dataset.")
    exit(1)

EXPECTED_FEATURES = 83
feature_columns = data.drop("Label", axis=1).columns

# Extract one valid sample per label
demo_data = {}
for label in data["Label"].unique():
    label_data = data[data["Label"] == label]
    logging.info(f"Processing label: {label}, samples available: {len(label_data)}")
    if len(label_data) == 0:
        logging.warning(f"No samples found for label {label}")
        print(f"Warning: No samples found for label {label}")
        continue
    # Try up to 5 samples to find a valid one
    for i in range(min(5, len(label_data))):
        sample = label_data.iloc[i].drop("Label")
        if len(sample) == EXPECTED_FEATURES and not sample.isna().any():
            demo_data[label] = sample.values.tolist()
            logging.info(f"Valid sample found for {label} at index {i}")
            break
        else:
            logging.warning(f"Invalid sample for {label} at index {i}: {len(sample)} features, NaN: {sample.isna().any()}")
    else:
        logging.error(f"No valid sample found for {label} after checking {min(5, len(label_data))} samples")
        print(f"Warning: No valid sample found for {label} (all samples have incorrect feature count or NaN values)")

# Print demo data
print("DEMO_DATA = {")
for label, values in demo_data.items():
    print(f"    \"{label}\": [")
    print("        " + ", ".join(f"{v}" for v in values[:40]) + ",")
    print("        " + ", ".join(f"{v}" for v in values[40:]) + "")
    print("    ],")
print("}")