from pathlib import Path
import pandas as pd

class Cleaner:
    
    @staticmethod
    def clean_data(data_path, output_path):
        if not Path(data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
        
        df = pd.read_csv(data_path) 

        df = df.dropna()\
            .drop(columns=["Domestic Lifetime Gross", "Domestic %", "Foreign Lifetime Gross", "Foreign %", "Title_y"])\
            .rename(columns={"Title_x": "Title"})\
            .reset_index(drop=True)

        cleaned_df = Cleaner._clean_money_data(df, "Worldwide Lifetime Gross", "Budget")
        print(f"Cleaned money data...")
        
        cleaned_df.to_csv(output_path)
        print(f"Cleaned dataframe saved into: {output_path}")
        
    @staticmethod
    def _clean_money_data(df, *col_names):
        for col_name in col_names:       
            df[col_name] = df[col_name].str.replace("[$,]", "", regex=True).astype(int)
        return df

    @staticmethod   
    def _clean_percent_data(df, *col_names):
        for col_name in col_names:       
            df[col_name] = df[col_name].str.replace("[%]", "", regex=True).astype(float)
        return df