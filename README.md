[![Python 3.10](https://img.shields.io/badge/python-3.10.8-blue)](https://www.python.org/downloads/release/python-31013/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 
<!-- ![GitHub version](https://img.shields.io/github/v/release/lgiesen/twitter-sentiment-analysis-politicians?color=green&include_prereleases) -->

## Contextualization

This repository contains the code but not the data for a seminar thesis in the module Urban Analytics conducted at the University of Münster in the winter semester of 2023/2024.
This seminar thesis explores the influence of geographic location on public perceptions of the political leaders Donald Trump and Boris Johnson between 2018 and 2022 through a detailed analysis of Twitter/X posts from Los Angeles, New York City, Birmingham, and London. 


## Objectives and Key Results
It demonstrates that local cultural, economic, and political contexts significantly affect public sentiment, with a notable homogeneity within countries that highlights the national context's impact. Key events, including elections and scandals, were found to provoke vital, often critical, reactions, particularly within the leaders' home countries, indicating that significant occurrences have the power to transcend geographical boundaries. This research contributes to urban analytics by highlighting the importance of geographic context in shaping political perceptions, offering valuable insights into how global political events are locally interpreted and responded to.

## Repository Structure

- **/spam_detection**: Contains code that filters spam posts.
- **/results**: Contains the analysis output and intermediate results used across files, including sentiment scores, post counts, and visualizations that highlight the research findings.
- **/visualizations**: Contains visualizations used for the comparative and event analysis.
- **/seminar_thesis**: Contains the seminar thesis file.
- **/presentations**: Contains interim presentations in the context of the seminar.
- **/archive**: Contains archived files, which are not central to the research question and the scope of the seminar thesis.

## Files Description

- **Foundational Files**
    - **.env**: Reused local variables specific to your OS.
    - **config.py**: Reused global variables.
    - **requirements.txt**: Lists all Python libraries required to run the scripts.
- **Central Files**
    - **Data Preparation**
        - **data_collection.py**: The main script orchestrates the data collection, preprocessing, sentiment analysis, and visualization processes.
        - **preprocessing.py**: Script that calculates selects and preprocesses the data.
        - **get_mean_count.py**: Script that calculates the mean non-normalized post counts.
        - **get_average_sentiment.py**: Script that calculates the overall mean compound sentiment score.
    - **Analysis**
        - **data_overview.ipynb**: The data is aggregated and explored to get an initial overview of the data.
        - **analysis_events.ipynb**: Event analysis using the normalized post count (NPC) and compound sentiment score (CSS) is performed here.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](https://github.com/lgiesen/twitter-sentiment-analysis-politicians/blob/main/LICENSE) file for details.

## Usage

Prerequisite: You need to have the data provided by the chair of Information Systems at the University of Münster.
1. Adjust the `.env` file to match the filepath to the data and root directory.
2. Execute the code from `preprocessing.py` to generate the dataset.
3. Execute and adjust the code from the jupyter notebooks (suffix `.ipynb`) to your liking.
4. Analyse the results.