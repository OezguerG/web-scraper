import os
from clean import Cleaner
import run_spider
from visualize import BoxOfficeVisualizer
from dotenv import load_dotenv
from processor import MovieDataProcessor
from scraping.scraper_data import BoxOfficeScraper

# Chat-GPT 10-11 (loads env variables, these are collable with os.getenv)
load_dotenv(dotenv_path='data_paths.env')
scrape_out_path = os.getenv("SCRAPE_OUTPUT_PATH")
result_path = os.getenv("FULL_SCRAPE_OUTPUT_PATH")
result_cleaned_path = os.getenv("CLEANED_DF_OUTPUT_PATH")
vis_path = os.getenv("VISUALISATION_PATH")
vis_genre_cluster_path = os.getenv("VISUALISATION_CLUSTER_PATH")
vis_rel_turnover_path = os.getenv("VISUALISATION_BUDGET_GROSSING_RATIO_PATH")
vis_budget_comp_path = os.getenv("VISUALISATION_BUDGET_COMPARISON_PATH")
vis_lucrative_path = os.getenv("LUCRATIVE_PATH")
vis_lucrative_mean_path = os.getenv("LUCRATIVE_MEAN_PATH")
vis_lucrative_mean_year_path = os.getenv("LUCRATIVE_MEAN_YEAR_PATH")                                                     

while True:
    choice = input("1: scrape movie links, 2: scrape movie data, 3: build dataframe, 4: clean dataframe, 5: make graph, 6: exit, 7: test | (1, 2, 3, 4, 5, 6, 7): ").strip()   
    try:
        if choice == "1":
            run_spider.run_spider()
            
        elif choice == "2":
            scraper = BoxOfficeScraper(600)
            budgets_df = scraper.scrape_budget_genre_from_webpaths(f"{scrape_out_path}/movie_links.json")
            budgets_df.to_csv(f"{scrape_out_path}/movie_budgets_and_genres.csv", index=False)
            print(f"Budgets and Genres written into: {scrape_out_path}")
            
            grossing_df = scraper.scrape_grossings_as_df()
            grossing_df.to_csv(f"{scrape_out_path}/movie_grossings.csv", index=False)
            print(f"Grossings written into: {scrape_out_path}")

        elif choice == "3":
            movie_rankings = MovieDataProcessor.merge_data(f"{scrape_out_path}/movie_grossings.csv", f"{scrape_out_path}/movie_budgets_and_genres.csv")
            MovieDataProcessor.export_to_csv(movie_rankings, f"{result_path}")
            print(f"Exported combined data to: {result_path}/")
                       
        elif choice == "4":
            Cleaner.clean_data(result_path, result_cleaned_path)
            
        elif choice == "5":
            movie_visual = BoxOfficeVisualizer(result_cleaned_path)
            
            movie_visual.visualize_genre_cluster(vis_genre_cluster_path, "Box Office: Worldwide Gross vs Budget", "Budget ($) ", "Worldwide Lifetime Gross ($)")
            print(f"\nExported visualized of data to: {vis_genre_cluster_path}")
            
            movie_visual.visualize_genre_relative_comparison(vis_rel_turnover_path, "Percentage Increase in Earnings relative to Budget", "Budget ($)", "Percent Increase Budget Return (%)")
            print(f"Exported visualized of data to: {vis_rel_turnover_path}")
            
            movie_visual.visualize_budget_comparison(vis_budget_comp_path, "Show Budget for top 500 Movies in 5 Chunks", "Chunks (100 highest Großing per Chunk descending)", "Mean Budget ($)", 100, 4, bar_plt=True, color=False)
            print(f"Exported visualized of data to: {vis_budget_comp_path}")
            
            movie_visual.visualize_genre_most_lucrative(vis_lucrative_path, "Turnover Per Movie", "Genre", "Turnover ($)")
            print(f"Exported visualized of data to: {vis_lucrative_path}")
            
            movie_visual.visualize_genre_most_lucrative_mean(vis_lucrative_mean_path, "Difference in Turnover Mean per Genre", "Genre", "Mean Turnover ($)", bar_plt=True)
            print(f"Exported visualized of data to: {vis_lucrative_mean_path}")
            
            movie_visual.visualize_year_most_lucrative_mean(vis_lucrative_mean_year_path, "Difference in Turnover Mean per Year", "Year", "Mean Turnover ($)", color=False, connect=True)
            print(f"Exported visualized of data to: {vis_lucrative_mean_year_path}\n")
            
        elif choice == "6":
            print("exiting...\n")
            break
        
        elif choice == "7":
            print()
        
        else:
            print("Invalid input\n")
            
    except Exception as e:
        print(f"\n An error occurred: \n {e} \n")
        exit(1)