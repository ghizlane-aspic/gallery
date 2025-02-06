import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def preprocess_data(self):
        if self.data is not None:
            # Example: Convert date column to datetime
            if 'date' in self.data.columns:
                self.data['date'] = pd.to_datetime(self.data['date'])
            # Handle missing values
            self.data = self.data.fillna(0)
        else:
            print("No data to preprocess.")