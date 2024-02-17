# Literature Research

The literature research string is comprised by the three criteria and their synonyms. The first criterion of sentiment analysis must be met because sentiment analysis is crucial to the topic. 

Additionally, one of the other two criteria of political leaders and the location-specific data is met in the search results because some relevant scientific papers might not mention one of the two topics in the title, abstract of keywords. Moreover, it was filtered for publications after 2017 because social media data is only useful with millions of posts, which is the case in recent years. The literature is evaluated by sequentially reading the title, abstract, and, finally, the full text to check if a source is relevant.

The search string resulted in 1,041 results, from which four were highly relevant (see algorithm below).  Other scientific papers were partially used to refine the methodology of data analysis and visualization and transferring insights into a political analysis.


```TITLE-ABS-KEY ( "sentiment analysis" OR "opinion mining" ) 
AND (
	( TITLE-ABS-KEY ( "Donald Trump" OR "Trump" OR 
        "Boris Johnson" OR "Johnson" ) ) 
    OR ( TITLE-ABS-KEY ( "location" OR "geospatial" OR 
    "regional" OR "geographic" OR "geo-tagged" ) ) 
)
AND PUBYEAR > 2017```