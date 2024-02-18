
# Twitter Sentiment Analysis of Politicians

This repository contains the code and data for a seminar thesis conducted at the University of Münster, focused on analyzing the influence of geographic location on public perceptions of political leaders Donald Trump and Boris Johnson from 2018 to 2022. Utilizing Twitter data, this research investigates how local cultural, economic, and political contexts affect public sentiment.

## Objective and Research Question

The thesis aims to understand the dynamics of public perception by analyzing Twitter data related to Donald Trump and Boris Johnson, exploring the political discourse surrounding these figures before, during, and after their term in office. It seeks to fill the research gap by conducting an event-based comparative analysis of the normalized post count (NPC) and compound sentiment score (CSS) across different geographic locations, aiming to discern how geographic location influences public sentiment and attention towards these political leaders.

## Key Results

- Geographic location significantly influences public sentiment towards political leaders, with notable homogeneity within countries.
- National contexts significantly affect public perception, overshadowing local concerns.
- Key events, including elections and scandals, provoke significant, often critical, public reactions, especially within the leaders' home countries.
- Donald Trump and Boris Johnson garnered more attention and criticism domestically, indicating the national relevance of political figures significantly affects public discourse.

## Repository Structure

- **/spam_detection**: Contains code that filters spam posts.
- **/results**: Contains the analysis output and intermediate results used across files, including sentiment scores, post counts, and visualizations that highlight the research findings.
- **/visualizations**: Contains visualizations used for the comparative and event analysis.
- **/seminar_thesis**: Contains the seminar thesis file.
- **/presentations**: Contains interim presentations in the context of the seminar.
- **/archive**: Contains archived files, which are not central to the research question and the scope of the seminar thesis.

## Files Description

- **data_overview.ipynb**: The data is aggregated and explored to get an initial overview of the data.
- **analysis_events.ipynb**: Event analysis using the normalized post count (NPC) and compound sentiment score (CSS) is performed here.
- **main.py**: The main script that orchestrates the data collection, preprocessing, sentiment analysis, and visualization processes.
- **get_average_sentiment.py**: Script that calculates the overall mean compound sentiment score.
- **get_mean_count.py**: Script that calculates the mean non-normalized post counts.
- **preprocessing.py**: Script that calculates selects and preprocesses the data.
- **requirements.txt**: Lists all Python libraries required to run the scripts.

## Usage

Instructions on how to set up the environment, execute the scripts, and interpret the results are provided in the `/docs` folder.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
