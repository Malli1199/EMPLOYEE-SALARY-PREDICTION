import pandas as pd

print("⏳ Fetching the Adult Income dataset from public mirror...")
try:
    # URL pointing to the standard clean UCI Adult Dataset mirror
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    
    # Defining column names since the raw UCI file doesn't have a header row
    columns = [
        "age", "workclass", "fnlwgt", "education", "education-num", 
        "marital-status", "occupation", "relationship", "race", "gender", 
        "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
    ]
    
    # Load and save locally
    df = pd.read_csv(url, names=columns, skipinitialspace=True)
    df.to_csv("adult 3.csv", index=False)
    print("✅ Success! 'adult 3.csv' has been downloaded and saved to your root folder.")

except Exception as e:
    print(f"❌ Failed to download automatically. Error: {e}")
    print("Please download the 'Adult Income Dataset' CSV manually.")