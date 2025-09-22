from pathlib import Path
import pandas as pd


class MovieDataProcessor:

    @staticmethod
    def merge_data(grossings_csv, budgets_csv):
        if not Path(grossings_csv).exists() or not Path(budgets_csv).exists():
            raise FileNotFoundError("One or both input CSV files were not found.")
        
        df1 = pd.read_csv(grossings_csv)
        df2 = pd.read_csv(budgets_csv)         
        
        df1 = df1.sort_values("Rank")
        df2 = df2.sort_values("Rank")
        
        df_combined = pd.merge(df1, df2, on='Rank', how='left')
        return df_combined

    @staticmethod   
    def export_to_csv(df, filepath):
        # df.set_index("Rank", inplace=True)
        df.to_csv(filepath)
    
    @staticmethod    
    def get_entries_for_column(df, column_name):
        return df[column_name].unique().tolist()
    
    @staticmethod
    def get_budget_chunks_difference(df, budget, chunk_size, chunks):
        
        df['Budget diff Mean'] = 0.0
        df['Chunks'] = ""
        for i in range(1, chunks + 1):
            section_start = chunk_size * (i-1)
            section_end = min(chunk_size * i, len(df))
            mean = df[budget][section_start:section_end].mean()
            df.loc[section_start:section_end - 1, 'Budget diff Mean'] = mean
            df.loc[section_start:section_end - 1, 'Chunks'] = f"Chunk {i}"
        return df
    
    @staticmethod
    def get_percent_difference_columns(df, budget, grossing):
        df['Percent'] = round((((df[grossing] - df[budget]) / df[budget]) * 100).astype(float), 2)
        return df
    
    @staticmethod
    def get_total_difference_columns(df, budget, grossing):
        df['Total Gross Diff'] = df[grossing] - df[budget]
        return df
    
    @staticmethod
    def get_total_difference_mean_per_genre(df, genre, diff):
        genre_means = df.groupby(genre)[diff].mean()
        df['Total Gross Diff Mean'] = df[genre].map(genre_means)
        return df
    
    @staticmethod
    def get_total_difference_mean_per_year(df, year):
        year_means = df.groupby(year)['Total Gross Diff'].mean()
        df['Total Gross Diff Mean'] = df[year].map(year_means)
        return df
        
    @staticmethod
    def count_genre_occurring_per_year(df, genre, year):
        df['Parent Genre'] = df[genre].apply(lambda x: " ".join(x.split()[:2]))
        genre_count_by_year = df.groupby([year, 'Parent Genre']).size().reset_index(name='Genre Count')
        df = df.merge(genre_count_by_year, how='left', on=[year, 'Parent Genre'])
        return df
    
    @staticmethod
    def explode_genre(df, genre):
        df[genre] = df[genre].str.split(" ")
        df = df.explode(genre).reset_index(drop=True)
        return df