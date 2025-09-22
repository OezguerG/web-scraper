from pathlib import Path

import matplotlib
from processor import MovieDataProcessor
from matplotlib import patches
import pandas as pd
import matplotlib.pyplot as plt



class BoxOfficeVisualizer:
    def __init__(self, data_path):
        self.genre_dic = {}
        self.data_path = data_path
        
        
    def visualize_genre_cluster(self, output_path, title, x_title, y_title, bar_plt = False, color = True, connect = False):     
        if not Path(self.data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
    
        df = pd.read_csv(self.data_path)
        df_helper = BoxOfficeVisualizer._create_helper_columns(df)


        x_data = df_helper['Budget']
        y_data = df_helper['Worldwide Lifetime Gross']
        df_helper.to_csv("output/test.csv")
        self._setup_plot(df_helper, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)
        
    def visualize_genre_relative_comparison(self, output_path, title, x_title, y_title, bar_plt = False, color = True, connect = False):
        if not Path(self.data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
    
        df = pd.read_csv(self.data_path)

        df_percent = MovieDataProcessor.get_percent_difference_columns(df, "Budget", "Worldwide Lifetime Gross")
        df_helper = BoxOfficeVisualizer._create_helper_columns(df)
        
        x_data = df_percent['Budget']
        y_data = df_percent['Percent']

        self._setup_plot(df_helper, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)
        
    def visualize_budget_comparison(self, output_path, title, x_title, y_title, chunk_size, chunks, bar_plt = False, color = True, connect = False):
        if not Path(self.data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
    
        df = pd.read_csv(self.data_path)
        section_end = chunk_size * chunks
        if (section_end > len(df)):
            raise Exception("Wanted Chunk sizes dont match the df")
        
        df_helper = BoxOfficeVisualizer._create_helper_columns(df)
        df_cut = MovieDataProcessor.get_budget_chunks_difference(df_helper, "Budget", chunk_size, chunks)
        
        df_cut = df.iloc[:section_end,].copy()
        x_data = df_cut['Chunks']
        y_data = df_cut['Budget diff Mean']
        self._setup_plot(df, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)
        
        
    def visualize_genre_most_lucrative(self, output_path, title, x_title, y_title, bar_plt = False, color = True, connect = False):
        if not Path(self.data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
    
        df = pd.read_csv(self.data_path)

        df_total_diff = MovieDataProcessor.get_total_difference_columns(df, "Budget", "Worldwide Lifetime Gross")
        df_helper = BoxOfficeVisualizer._create_helper_columns(df_total_diff)

        x_data = df_helper['First_Two_Letters']
        y_data = df_helper['Total Gross Diff']
        
        self._setup_plot(df_helper, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)
        
        
    def visualize_genre_most_lucrative_mean(self, output_path, title, x_title, y_title, bar_plt = False, color = True, connect = False):
        if not Path(self.data_path).exists():
            raise FileNotFoundError("CSV file was not found or path incorrect.")
    
        df = pd.read_csv(self.data_path)
        
        df_helper = BoxOfficeVisualizer._create_helper_columns(df)
        df_helper = MovieDataProcessor.get_total_difference_columns(df_helper, "Budget", "Worldwide Lifetime Gross")
        df_helper = MovieDataProcessor.get_total_difference_mean_per_genre(df_helper, "First_Two_Letters", "Total Gross Diff")

        x_data = df_helper['First_Two_Letters']
        y_data = df_helper['Total Gross Diff Mean'] 
        
        self._setup_plot(df_helper, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)
        
        
    def visualize_year_most_lucrative_mean(self, output_path, title, x_title, y_title, bar_plt = False, color = True, connect = False):
        if not Path(self.data_path).exists():
               raise FileNotFoundError("CSV file was not found or path incorrect.")
        
        df = pd.read_csv(self.data_path)
            
        df_helper = BoxOfficeVisualizer._create_helper_columns(df)
        df_total_diff = MovieDataProcessor.get_total_difference_columns(df_helper, "Budget", "Worldwide Lifetime Gross")
        df_diff_mean = MovieDataProcessor.get_total_difference_mean_per_year(df_total_diff, "Year")
        df_diff_mean = df_diff_mean.sort_values(by='Year')

        x_data = df_diff_mean['Year']
        y_data = df_diff_mean['Total Gross Diff Mean']
            
        self._setup_plot(df_diff_mean, title, x_title, y_title, x_data, y_data, output_path, bar_plt, color, connect)

    
    def _setup_plot(self, df, titel, x_titel, y_titel, x_data, y_data, output_path, bar_plt = False, color = True, connect = False):
        plt.figure(figsize=(22, 18))
        if color == True:
            df = self._setup_column_genre_color(df)
            if bar_plt == True:
                plt.bar(x_data, y_data, color=df['Color'])
            else:
                plt.scatter(x_data, y_data, c=df['Color'])
        else:
            if bar_plt == True:
                plt.bar(x_data, y_data, color="grey")
            elif connect == True:
                plt.plot(x_data, y_data, marker='o', linestyle='-', color='steelblue')   
            else: 
                plt.scatter(x_data, y_data)
               
        plt.title(titel)
        plt.xlabel(x_titel)
        plt.ylabel(y_titel)

        if color == True: 
            unique_genres = df['First_Two_Genre'].unique()
            # Chat-GPT  131 - 132
            handles = [patches.Patch(color=self.genre_dic.get(genre, 'gray'), label=genre) for genre in unique_genres]
            plt.legend(handles=handles, title="Genres")
        
        plt.savefig(output_path)

        plt.close()
        
    def _setup_column_genre_color(self, df):  
        genre_list = df['First_Two_Genre'].unique().tolist()
        color_list = BoxOfficeVisualizer._get_colors(len(genre_list))

        for idx, genre in enumerate(genre_list):
            self.genre_dic[genre] = color_list[idx]
            
        df['Color'] = df['First_Two_Genre'].apply(lambda x: self.genre_dic.get(x, 'gray'))
        
        return df
    
    @staticmethod   
    def _get_colors(genre_size, gap = 3):
        # Chat-Gpt from...
        total = genre_size + gap
        cmap = matplotlib.colormaps.get_cmap('hsv')
        color_list = [cmap(i / total) for i in range(genre_size)]
        return color_list
        # ... till
        
    @staticmethod    
    def _create_helper_columns(df):
        df['First_Two_Genre'] = df['Genre'].apply(lambda x: " ".join(sorted(x.split(" ")[0:2])))
        # Chat-GPT 162
        df['First_Two_Letters'] = df['First_Two_Genre'].apply(lambda x: "".join([word[:2] for word in x.split(" ")]))
        return df