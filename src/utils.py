import pandas as pd

def load_data(filepath):
    try:
        data = pd.read_excel(filepath)
        return data
    except Exception as e:
        return None
