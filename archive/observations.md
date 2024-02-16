#### Sentiment Observations and Abnormalities

**Donald Trump**
Overall
- variance
    - little higher variance from January 2021 until July 2022 -> lower post count makes it more susceptible to variance
- reaction: almost always the same development in sentiment score -> similar reaction to events. GB reaction is a little stronger; this variance is explained with a smaller dataset. Take higher baseline of GB into consideration
- outliers
    - peaks: 
        - 2021-06-13 - 2021-06-14: mean sentiment score 0.21
        - 2021-10-03: sentiment score 0.15
        - 2020-06-14: sentiment score 0.15
        - christmas and new year should not be evaluated: 
            - 2019-12-25: sentiment score 0.11
            - 2022-01-01, Sentiment: 0.11
            - 2021-12-30, Sentiment: 0.10
    - low points:
        - 2019-08-04 - 2019-08-05: mean sentiment score mean -0.22
        - 2018-10-25: mean sentiment score -0.18 
        - 2020-06-01: mean sentiment score -0.18
        - 2020-01-05: mean sentiment score -0.18

Countries
- baseline
    - Trump has a higher baseline in Britain than in the US and vice versa for Johnson in the US -> presidents are more popular in other countries vs. their own one -> Johnson viewed more favorably in the US due to less direct impact on the lives of the American public -> less critical perspective
- variance
    - Trump has a higher variance in Britain than in the US and vice versa for Johnson in the US than Johnson. Possible explanation: less data about the political leader in the other country
- US and overall almost identical for trump
- outliers: same in both countries due to similar reactions
    - only US does not have the peak in 2021-06-14
    - 2020-01-05 GB has a strong negative reaction (sentiment score of -0.31), which is not the case in the US

- no reason found: 
    - The specific events causing the missing peak in the US on June 14, 2021, and the strong negative reaction in Britain on January 5, 2020, are not identified within the available data.

Cities
- The overall sentiments in Great Britain and the US also differ, emphasizing how national contexts shape public perception.
    - NYC and LA very similar, especially the end of 2020
    - London and Birmingham are also similar considering the latter's high variance
- outliers
    - in LA on 2020-12-27, Trump has a mean sentiment score of 0.12, but on the next day it is -0.28. 


**Boris Johnson**
Overall
- outliers
    - peaks
        - all significant peaks are (from 2018-11-21) until 2019-06-21
        - the lowest point comprise the following data point:
            - 2019-06-21: sentiment score 0.50
        - other events
            - 2018-11-23: sentiment score 0.36
            - 2018-11-21: sentiment score 0.32
            - 2019-03-19: sentiment score 0.32
            - 2019-01-31: sentiment score 0.29
            - 2018-12-30: sentiment score 0.29
            - 2019-01-11: sentiment score 0.28
            - 2019-04-24: sentiment score 0.28
            - 2019-05-12: sentiment score 0.28
            - 2019-01-16: sentiment score 0.28
    - low points
        - all significant low points are since 2020-11-20 (and until 2022-04-13)
        - the lowest point comprise the following data points:
            - 2021-07-12 - 2021-07-14: mean sentiment score -0.17
        - other events
            - 2021-06-28: sentiment score -0.19

    - no explanation found:
        - Further investigation is needed to determine the reason for the sentiment peak on June 14, 2021.
        - The exact events influencing the low sentiment scores on October 25, 2018, and June 1, 2020, remain unidentified within the available data.

Countries
- baseline:
    - it is unusual that Johnson is on average more popular than the general mean post in the US (with a mean sentiment score of 0.17 versus the 0.15 of the US). This is both the case for LA and NYC.  
- outliers

    - phases
        - positive sentiment
            - GB has a positive view on Johnson from 2018-11-23 until 2019-06-21. What events happened here, especially on the days: 2019-06-21, 2019-05-12, 2018-12-29, 2019-02-23, 2018-12-30, 2018-11-23, 2019-01-03, 2019-01-23, 2019-04-24, 2018-12-01? 

        - negative sentiment
            - US has a negative perception on Johnson from 2020-12-09 to 2021-04-18
            - GB a negative perception on Johnson from 2021-05-17 - 2021-07-14 (what happened in that timespan, especially on the days of 2021-07-12, 2021-06-28, 2021-07-13, 2021-07-14, 2021-05-17?)
            - GB a negative perception on Johnson from 2022-03-29 - 2022-05-16 (what happened in that timespan, especially on the days of 2022-04-03, 2022-04-13, 2022-04-15, 2022-03-29, 2022-05-16?)

    - it is odd that at a similar time, there is peak in GB and a low point in the US: 
        - In GB there is a strong peak on 2019-06-21 (with a sentiment score of 0.52) and in the US there is a low point on 2019-06-02 (with a mean sentiment score of -0.14). Are these dates correlated? Find possible explanations for it.
    - peaks
        - In US 2021-12-04 - 2021-12-05 with a mean sentiment score of 0.44
    - low points
        - near 2021-02 sentiment score of -0.2 in US
    what happened at these outliers?

Cities
- All cities of the same country and are characterized by a similar sentiment baseline and development
- Birmingham and London
    - variance: both have a stronger variance until 2019-07
    - Birmingham has a sudden shift of sentiment from 2020-01-10 with a sentiment score of 0.52 to the following day to -0.41
- outliers
    - peaks
        - Birmingham has a peak of sentiment on 2021-02-18 with a sentiment score of 0.55
    - low point
        - Only LA has a low point of -0.14 on 2019-06-02 -> responsible for US sentiment there


**Comparison of Presidents**
- variance: surprising that Trump has a relatively small variance. trump controversial political figure could have more fluctuation -> compound sentiment of his followers and the opposing group cancel out because of mean calculation
- baseline: Johnson has a slightly higher mean compound sentiment score
    - Trump: US (-0.06) GB (0.02)
    - Johnson: US (0.03) GB (0.17)
- Presidents significantly below general mean sentiment score (MSS) -> Scrutinous and negative media coverage creating; Controversial policies having a negative impact on people’s lives; Political scandals or legal issues

**Comparison of Location Baselines**
Countries
- GB has a higher baseline: GB 0.23 and US 0.15 - US is more negative than GB 
    - reasons
        - cultural differences in expression: Americans more direct -> easier for algorithm to detect negativity
        - politics: US political division & intensity of political climate -> more critical view of both domestic and international politicians

Cities
- cities in the same country similar: LA (0.16) NYC (0.14) London (0.23) Birmingham (0.24). Considering the public perception on the presidents, especially NYC and LA have a very similar mean sentiments (Mean Compound Sentiment by City.png) 
    - reasons
        - major urban centers, heavily influenced by national media narratives
        - nationwide issues or perceptions of these leaders overshadow local concerns -> uniform sentiment across different urban centers
    - political views do not completely align in BI & LO: Birmingham more rural than London (not a city of over a million inhabitants)

##### Non-Normalized Clustered High Post-Frequency Dates

**Donald Trump**

Overall
1. 2020-11-04 - 2020-11-08 (7761 + 5872 + 8198 + 11292 + 5804)
2. 2020-09-30 - 2020-10-02 (10210 + 6708)
3. 2021-01-06 - 2021-01-07 (8231 + 6127)
4. 2020-10-23 (5673)

GB
1. 2020-11-04 - 2020-11-08 (1994 + 1334 + 2000 + 3036 + 1334)
2. 2019-06-03 - 2019-06-04 (1636 + 1510)
3. 2021-01-06 - 2021-01-07 (1680 + 1126)
4. 2021-01-20 (888)

US
1. 2020-09-30 (9564) 
2. 2020-11-04 - 2020-11-08 (5767 + 4538 + 6198 + 8256 + 4470)
3. 2021-01-06 - 2021-01-07 (6551 + 5001)
4. 2010-10-02 (5841)
5. 2020-10-23 (5301)

NYC
1. 2020-09-30 (4879) 
2. 2020-11-04 - 2020-11-08 (2620 + 2223 + 2814 + 3904 + 2219)
3. 2021-01-06 - 2021-01-07 (3292 + 2491)
4. 2020-10-23 (2766)
5. 2010-10-02 (2581)

LA
1. 2020-09-30 - 2020-10-02 (4685 + 4685)
2. 2020-11-04 - 2020-11-07 (3147 + 2315 + 3384 + 4352)
3. 2021-01-06 - 2021-01-07 (3259 + 2510)
4. 2020-10-02 (3260)
5. 2020-10-23 (2535)
6. 2020-06-01 (2274)

London
1. 2020-11-04 - 2020-11-08 (1680 + 1107 + 1673 + 2559 + 1117)
2. 2021-01-06 - 2021-01-07 (1411 + 954)
3. 2019-06-03 - 2019-06-04 (1381 + 1287)
4. 2021-01-08 (775) - outlier

Birmingham
1. 2020-11-04 - 2020-11-07 (314 + 227 + 327 + 477)
2. 2021-01-06 - 2021-01-07 (269 + 172)
3. 2019-06-03 - 2019-06-04 (255 + 223)
4. 2020-11-08 (217) 
5. 2021-01-20 (140)


**Boris Johnson**

Overall
1. 2020-05-24 - 2020-05-25 (2526 + 1737)
2. 2019-07-23 - 2019-07-24 (2212 + 1637)
3. 2020-05-10 (1958)
4. 2020-04-06 (1724)
5. 2019-12-12 - 2019-12-13 (1492 + 1701)
6. 2019-09-24 (1646)
7. 2020-10-31 (1620)

GB
1. 2020-05-24 - 2020-05-25 (2463 + 1491)
2. 2019-07-23 - 2019-07-24 (1988 + 1637)
3. 2020-05-10 (1898)
The rest is roughly on a similar level:
4. 2020-10-31 (1556)
5. 2020-04-06 (1553)
6. 2019-12-13 (1526)
7. 2019-09-24 (1460)
8. 2022-06-06 (1323)

US: completely different to GB. Different dates etc.
1. 2019-04-10 (288)
2. 2020-04-06 (171)
3. 2019-09-24 (236)
4. 2019-07-23 (224)
5. 2020-07-23 (198)
6. 2019-12-12 - 2019-12-13 (177 + 175)
7. 2019-10-06 (168)
8. 2019-02-14 (157)
9. 2019-05-20 (152)

LA
1. 2019-04-10 (209)
2. 2020-07-23 (120)
3. 2020-12-27 (104)
4. 2019-02-14 (101)
5. 2019-07-23 (97)
6. 2019-02-05 + 2019-02-07 (94 + 96)
7. 2020-02-16 (91)
8. 2018-10-29 (90)
9. 2019-10-06 (89)


Johnson NYC: US cities differ completely
1. 2019-09-22 + 2019-09-24 (97 + 174)
2. 2019-07-23 - 2019-07-24 (95 + 127)
3. 2019-12-12 - 2019-12-13 (102 + 97)
4. 2020-06-30 (101)
5. 2019-10-12 (98)
6. 2020-04-07 (96)
7. 2019-03-12 (95)  

London
1. 2020-05-24 - 2020-05-25 (1964 + 1349)
2. 2019-07-23 (1602)
3. 2020-05-10 (1533)
4. 2019-12-13 (1277)
5. 2019-09-24 (1272)
6. 2019-07-24 (1251)
7. 2020-10-31 (1251)
8. 2020-04-06 (1221)
9. 2019-12-12 (1106)
    

Birmingham: 2019-06-21 - 2019-06-23 relevant in BI, but not in LO; 2019-09-24, 2019-07-24, 2020-04-06, 2019-12-12 in LO, but not BI
1. 2019-06-21 - 2019-06-23 (696 + 341 + 385)
2. 2020-05-24 - 2020-05-25 (499 + 299)
3. 2019-07-23 (386)
4. 2020-05-10 (365)
5. 2020-04-06 (332)
6. 2020-10-31 (305)
7. 2019-08-28 (284)

##### Post Count Observations and Abnormalities

**General**
- After one or at maximum 4 days (usually 1-2), Twitter does not talk about scandals as much $\rightarrow$  News seem to become irrelevant after a couple of days and then irrelevant after that
- Birmingham has a higher variance (calc values or show bar graphs) than other cities -> maybe because of smaller dataset 

**Donald Trump**

Overall (trump-normalized_tweet_count.png)
- peaks
    - 3 considerate peaks at the end of the presidency (20 January 2017 – 20 January 2021) (TODO: check exact numbers)
        1. 2020-11-04 - 2020-11-08 (7761 + 5872 + 8198 + 11292 + 5804)
        2. 2020-09-30 - 2020-10-02 (10210 + 6708)
        3. 2021-01-06 - 2021-01-07 (8231 + 6127)
    - less significant peaks (not in thesis)
        4. 2020-10-23 (5673)
        5. optional TODO: check more than the 10 most significant days

Countries (trump-countries-normalized_tweet_count.png)
- US has a slightly higher baseline compared to GB (maybe because it is their president -> TODO: CALC overall MEAN)
- mostly the same outliers (= reaction to events), e. g. 2021-01-06 - 2021-01-07
- sometimes different intensity of reaction:
    - GB strong reaction 2019-06-03 - 2019-06-04 (and slightly less extreme in 2019-12), but no noticable difference in the the post count from the US. Same in 2022-07, but maybe because higher variance in GB because of smaller dataset
    - US stronger reaction (more posts) from 2020-11-04 - 2020-11-08 (attention: this is the day which has the highest non-normalized post count in GB, but not in US. Nevertheless, this is an observation in the normalized data)

Cities (trump-cities-normalized_tweet_count.png)
- primarily Birmingham is responsible for the GB peak in 2019-06-03 - 2019-06-04 and 2020-11-04 - 2020-11-08
- London is primarily responsible for the GB peak in 2021-01-06 - 2021-01-07
- very similar baseline of all cities (TODO: clip visualization at 7.5e-09 and check if i still think the same because the Birmingham peak could make the difference seem small)
- NYC and LA are very similar; Birmingham has a slightly higher baseline than London (TODO: CALC MEAN BASELINE)

**Boris Johnson**

Overall (johnson-normalized_tweet_count.png)
- more posts from 2019-06 - 2020-01
- many peaks: TODO: check what happened
    1. 2020-05-24 - 2020-05-25 (2526 + 1737)
    2. 2019-07-23 - 2019-07-24 (2212 + 1637)
    3. 2020-05-10 (1958)
    4. 2020-04-06 (1724)
    5. 2019-12-12 - 2019-12-13 (1492 + 1701)
    6. 2019-09-24 (1646)
    7. 2020-10-31 (1620)
    more: check post 1400+ (not in thesis)
    
Countries (johnson-countries-normalized_tweet_count.png)
- US has few posts about Johnson; Only GB has a higher baseline and variance than US; GB is almost exclusively responsible for the overall post count about Johnson
- Considering the non-normalized post counts, it is clear that the post count development in the US is completely different to the one in GB.
- (not in thesis) TODO: check difference between overall and country because it looks unusual when you compare the non-normalized with the normalized one
- Phases
    - Since 2021-11 until end of data: high variance and higher baseline in GB
    - 2019-07 - 2020-01 higher baseline (and 2020-04 - 2020-07) -> covid lockdown?

Cities (johnson-cities-normalized_tweet_count.png)
- Birmingham significantly higher baseline (same as with president Trump)
- LA & NYC are very similar again (in US/larger city -> national media more important)
- In non-normalized graph (not in thesis):
    - US cities differ completely. Maybe normalization was too strong?
    - 2019-06-21 - 2019-06-23 relevant in BI, but not in LO; 2019-09-24, 2019-07-24, 2020-04-06, 2019-12-12 in LO, but not BI