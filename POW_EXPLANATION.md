# Indian Credit Card Brand Intelligence — PoW Guide

## 1. What is this PoW?

PoW means **Proof of Work**.

This project demonstrates how an analyst can take customer-review data and
social-listening mentions, clean and analyse them as separate modules, create
business summaries, and present the findings through Excel and PowerPoint.

The customer-review module compares pure credit-card review data for:

- HDFC Bank
- SBI Card
- ICICI Bank

Axis Bank is not included in the customer-review module because a verified,
downloadable pure credit-card review dataset was not found for it. A separate
Twitter-listening module does include Axis Bank mentions.

This is a demonstration workflow, not a complete enterprise social-listening
platform.

---

## 2. Business objective

The objective is to understand what customers discuss about Indian credit-card
issuers and whether those discussions are positive, neutral or negative.

The analysis focuses on:

1. Review volume by issuer
2. Sentiment distribution by issuer
3. Common customer topics
4. Negative review themes
5. Comparison of issuer-level review patterns
6. A repeatable reporting process for Marketing Strategy teams
7. A separate historical social-listening view with dates and engagement

The two datasets are intentionally not appended together. A customer review
and a Twitter mention are different types of evidence and should not be
treated as one population.

---

## 3. Dataset used

The current analysis uses the published GitHub dataset:

[Sentiment Analysis on Credit Cards using Online Reviews](https://github.com/kyasanur/Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews)

The source file is stored locally at:

`data/source/sentiment_reviews_credit_data.csv`

The source contains credit-card review text, issuer name, topic information and
sentiment scores.

### Final record count

After cleaning and exact duplicate removal:

| Issuer | Records |
|---|---:|
| SBI Card | 1,368 |
| HDFC Bank | 212 |
| ICICI Bank | 191 |
| **Total** | **1,771** |

All records in the final analysis have:

```text
record_type = credit_card_review
```

Banking-app reviews and general bank commentary are excluded from the current
analysis because the requirement is to use pure credit-card reviews.

### Separate Twitter-listening module

The project also uses the published `twitterfiles.csv` file from the same
repository:

[Twitter dataset source](https://github.com/kyasanur/Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews)

The source contains 3,196 historical Indian Twitter records from
19 January 2022 to 19 March 2022, with issuer labels, dates, retweets,
favourites and sentiment scores. It includes SBI, HDFC, Axis and ICICI.

The Twitter module filters to India-based issuer rows whose text contains a
credit-card or card-benefit term, removes blank text and duplicate text, and
standardizes issuer names. The current filtered result contains 2,084 unique
relevant mentions:

| Issuer | Filtered unique mentions |
|---|---:|
| SBI Card | 566 |
| HDFC Bank | 700 |
| Axis Bank | 506 |
| ICICI Bank | 312 |
| **Total** | **2,084** |

These are social-listening mentions, not necessarily customer reviews. The
Twitter dataset is analysed separately and is not merged into
`analysis_data.csv`.

---

## 4. Why the dataset is not perfectly balanced

The source contains many more SBI Card reviews than HDFC Bank or ICICI Bank
reviews.

This is not corrected by randomly deleting SBI records. All valid SBI records
are retained so that no available source information is discarded.

As a result:

- SBI Card has the highest raw review count.
- Raw counts represent source volume, not market share.
- Issuer percentages must be shown together with sample sizes.
- Comparisons should be described as directional.

The correct interpretation is:

> “This source contains more SBI Card reviews than HDFC Bank and ICICI Bank.
> Therefore, raw volume comparisons reflect the dataset composition and should
> not be interpreted as market share.”

---

## 5. Data processing workflow

The workflow has two stages.

### Stage A — Import and standardize source data

Script:

`scripts/import_credit_card_dataset.py`

This script:

1. Reads the published source CSV.
2. Selects HDFC Bank, SBI Card and ICICI Bank credit-card records.
3. Standardizes issuer names.
4. Creates a common project schema.
5. Preserves the original source sentiment score.
6. Preserves the original source topic.
7. Adds provenance information.
8. Labels every imported row as `credit_card_review`.
9. Removes blank review text.
10. Removes duplicate review text.
11. Writes the full standardized source to:

   `data/raw_data.csv`

12. Writes the pure, deduplicated analysis data to:

   `data/analysis_data.csv`

### Stage B — Analyse and generate outputs

Script:

`scripts/pow_pipeline.py`

This script:

1. Reads `data/analysis_data.csv`.
2. Validates required columns.
3. Cleans whitespace and missing values.
4. Parses dates where available.
5. Removes exact duplicate review text.
6. Assigns project topics.
7. Converts source sentiment scores into sentiment labels.
8. Creates summary tables.
9. Creates charts.
10. Creates the Excel dashboard.
11. Creates the PowerPoint deck.

---

## 6. Data schema

The cleaned data uses these important columns:

| Column | Meaning |
|---|---|
| `record_id` | Unique project record identifier |
| `bank_name` | Issuer name |
| `card_name` | Card name if available |
| `source` | Dataset/source description |
| `record_type` | Type of record; currently `credit_card_review` |
| `published_date` | Review date if provided by the source |
| `review_text` | Customer review text |
| `engagement` | Engagement value if available |
| `source_url` | Source repository URL |
| `source_sentiment_score` | Original source sentiment score |
| `source_topic` | Original source topic |
| `topic` | Project topic classification |
| `sentiment` | Project sentiment label |

The current source does not provide reliable publication dates or engagement
values for all records. These values are not fabricated.

---

## 7. Sentiment methodology

The source already provides a numeric sentiment score.

The project converts it into three simple labels:

| Source score | Label |
|---|---|
| Greater than `0.1` | Positive |
| Between `-0.1` and `0.1` | Neutral |
| Less than `-0.1` | Negative |

This makes the results easier to use in an Excel dashboard and presentation.

The labels should be treated as directional because:

- The source scoring method is inherited from the published dataset.
- Sarcasm and context may not be captured.
- Some reviews are short or grammatically incomplete.
- Manual validation has not yet been completed for every record.

---

## 8. Topic methodology

The analysis uses the source topic labels where available and maps them into
business-friendly categories:

| Source topic | Project topic |
|---|---|
| `reward` | Rewards |
| `benefit` | Benefits |
| `offer` | Benefits |
| `fuel` | Cashback |
| `credit` | Fees |
| `spending` | Benefits |
| `card` | Benefits |

If a source topic cannot be mapped, the pipeline uses a transparent keyword
fallback based on terms related to:

- Cashback
- Rewards
- Fees
- Benefits
- Customer service

---

## 9. Summary analysis created

The pipeline creates:

### Issuer-level analysis

- Review count by issuer
- Positive share by issuer
- Neutral share by issuer
- Negative share by issuer
- Average source sentiment score

### Topic analysis

- Topic frequency
- Topic frequency by issuer
- Topic-level sentiment
- Negative topic counts

### Quality analysis

- Input record count
- Cleaned record count
- Duplicate count
- Issuer count
- Missing date percentage
- Missing engagement percentage
- Negative review count
- Largest issuer share

---

## 10. Excel dashboard

File:

[Indian_Credit_Card_Brand_Intelligence_PoW.xlsx](./outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx)

The workbook contains:

### `Data`

Cleaned record-level data.

### `Overall`

High-level KPIs such as total records, issuer count, topic count and sentiment
shares.

### `Mentions`

Review count by issuer.

### `Sentiment`

Positive, neutral and negative percentage mix by issuer.

### `Topics`

Topic counts by issuer.

### `Bank_Profile`

Issuer-level review volume and sentiment metrics.

### `Topic_Sentiment`

Sentiment counts by topic.

### `Complaints`

Negative review counts by issuer and topic.

### `Negative_Examples`

Record-level examples of negative reviews.

### `Quality`

Data-quality and coverage checks.

### `Dashboard`

Presentation-friendly dashboard area with three embedded Excel charts:

- Review volume by issuer
- Sentiment mix by issuer
- Topic-level sentiment

The charts are linked to the workbook summary sheets, so the final workbook can
be used as the main presentation and analysis file without opening separate
PNG chart files.

### `Pivot_Tables`

Pivot-style summary tables for:

- Issuer volume
- Issuer sentiment percentages
- Issuer topics
- Topic-level sentiment

These are generated from the cleaned data by Python. They are intentionally
visible summary tables rather than native Excel PivotTable objects, making the
workbook portable and reproducible with the current Python tooling.

---

## 11. PowerPoint presentation

File:

[brand_intelligence_deck.pptx](./outputs/brand_intelligence_deck.pptx)

The deck contains nine slides:

1. Title and objective
2. Research questions
3. Data and methodology
4. Dataset profile and quality
5. Share of voice proxy
6. Sentiment comparison
7. Topic-level comparison
8. Key findings and recommendations
9. Limitations and next steps

The deck explicitly states that source volume is not market share and that the
issuer coverage is uneven.

---

## 12. Current findings should be presented carefully

The project can support statements such as:

- “SBI Card has the largest number of reviews in this source.”
- “The source contains more SBI Card records than HDFC Bank or ICICI Bank.”
- “Sentiment shares differ across issuers in this sample.”
- “Benefits, fees and rewards are recurring themes in the review data.”

Avoid statements such as:

- “SBI Card owns the largest market share.”
- “HDFC customers are more satisfied than ICICI customers nationally.”
- “These results represent all Indian credit-card customers.”
- “The negative-review rate is the actual complaint rate.”

---

## 13. Limitations

The main limitations are:

1. Axis Bank is not included.
2. Issuer sample sizes are uneven.
3. The source does not provide reliable dates for all records.
4. Engagement values are unavailable or incomplete.
5. Card names are not reliably available for every record.
6. Sentiment labels are inherited from the source score.
7. Topic classification requires manual validation.
8. The source repository's redistribution rights must be confirmed before
   public distribution.
9. The dataset may not represent the full Indian credit-card market.
10. The results are directional and exploratory.
11. Twitter mentions and customer reviews use different populations and must
    not be combined into one denominator.

---

## 14. How to run the project

From the project folder:

```powershell
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/import_credit_card_dataset.py
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/pow_pipeline.py
```

The first command rebuilds the standardized pure credit-card data.

The second command regenerates:

- `data/cleaned_data.csv`
- `outputs/summary_tables.xlsx`
- `outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`
- `outputs/brand_intelligence_deck.pptx`
- `outputs/charts/mentions.png`
- `outputs/charts/sentiment.png`
- `outputs/charts/topic_sentiment.png`

The final Excel workbook is:

[Indian_Credit_Card_Brand_Intelligence_PoW.xlsx](./outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx)

The record-level data is on the `Data` sheet. The `Dashboard` sheet contains
the embedded charts, and `Pivot_Tables` contains the analysis summaries.

To build the separate historical Twitter-listening module, run:

```powershell
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/analyze_twitter_listening.py
```

This creates:

- `data/twitter_listening_data.csv`
- `outputs/Indian_Credit_Card_Social_Listening_PoW.xlsx`
- `outputs/charts/twitter_mentions.png`

The Twitter workbook contains `Data`, `Mentions`, `Sentiment`,
`Monthly_Mentions`, `Engagement`, `Quality` and `Dashboard` sheets. Its
dashboard shows issuer mention volume, monthly mentions and average
engagement, with explicit axis labels.

---

## 15. Recommended next steps

For a stronger professional submission:

1. Confirm the source license and redistribution permissions.
2. Find an approved pure credit-card review source for Axis Bank.
3. Add more pure credit-card reviews for HDFC Bank and ICICI Bank.
4. Collect or preserve reliable review dates.
5. Add engagement fields where legally available.
6. Manually validate at least 50 sentiment and topic labels.
7. Add confidence intervals or sample-size notes to issuer comparisons.
8. Refresh the analysis using a recent, consistently collected source.
9. Add a tracker for monthly refreshes.
10. Present the current project as a proof of analytical workflow, not as a
    definitive market study.

---

## 16. One-minute explanation for an interview

> “I built a reproducible proof of work for Indian credit-card brand
> intelligence. I used a published review dataset, standardized the issuer and
> review fields, removed duplicates, retained only pure credit-card reviews,
> converted source sentiment scores into positive, neutral and negative labels,
> mapped topics such as rewards, fees, benefits and cashback, and generated
> summary tables, an Excel dashboard and a nine-slide PowerPoint. I retained
> all available SBI records instead of deleting them to force balance, so I
> clearly disclose the sample-size imbalance and avoid interpreting raw volume
> as market share. I also added a separate historical Twitter-listening
> module with dates and engagement, keeping social mentions separate from
> customer reviews because they answer different business questions.”
