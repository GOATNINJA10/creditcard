# Indian Credit Card Brand Intelligence PoW

This is a two-day proof-of-work package for Indian credit-card brand
intelligence. It contains two separate analytical modules:

1. A pure customer-review analysis for HDFC Bank, SBI Card and ICICI Bank.
2. A historical Twitter social-listening analysis for HDFC Bank, SBI Card,
   ICICI Bank and Axis Bank.

The modules are kept separate because customer reviews and social-media
mentions are different types of evidence.

## Important data note

The customer-review module is derived from the published
[Sentiment Analysis on Credit Cards using Online Reviews](https://github.com/kyasanur/Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews)
repository. It contains pure credit-card review text and source sentiment
scores for HDFC Bank, ICICI Bank and SBI Card. The final review analysis has
1,771 deduplicated records:

- SBI Card: 1,368
- HDFC Bank: 212
- ICICI Bank: 191

The repository's `twitterfiles.csv` is used separately as a historical
social-listening source. After India, relevance and duplicate filtering, it
contains 2,084 unique credit-card-related Twitter mentions:

- HDFC Bank: 700
- SBI Card: 566
- Axis Bank: 506
- ICICI Bank: 312

The source repository does not expose an explicit license in its root files;
verify reuse rights before external redistribution. The Twitter records are
mentions, not necessarily customer reviews.

## Run

```powershell
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/import_credit_card_dataset.py
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/pow_pipeline.py
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/analyze_twitter_listening.py
```

The customer-review pipeline creates:

- `data/cleaned_data.csv`
- `outputs/summary_tables.xlsx`
- `outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`
- `outputs/brand_intelligence_deck.pptx`
- `outputs/charts/*.png`

The Twitter-listening pipeline creates:

- `data/twitter_listening_data.csv`
- `outputs/Indian_Credit_Card_Social_Listening_PoW.xlsx`
- `outputs/charts/twitter_mentions.png`

The customer-review analysis uses the published source sentiment score and
source topics where available, with a transparent keyword fallback. The
Twitter analysis maps the source score into positive, neutral and negative
labels and includes dates, retweets, favourites and calculated engagement.
For production work, validate the taxonomy and manually review a sample of
classifications.

## Input schema

`record_id`, `bank_name`, `card_name`, `source`, `published_date`,
`review_text`, and optional `engagement`.

The Twitter output uses the same core fields and additionally retains
`retweet_count`, `favorite_count`, `source_sentiment_score`, `sentiment` and
`month`.

## Final workbook guide

### Customer-review workbook

`outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`

- `Data`: record-level pure credit-card reviews
- `Dashboard`: KPI cards and review charts
- `Pivot_Tables`: supporting summary tables
- Other sheets: issuer, sentiment, topic, complaint and quality summaries

### Twitter social-listening workbook

`outputs/Indian_Credit_Card_Social_Listening_PoW.xlsx`

- `Data`: filtered unique Twitter mentions
- `Dashboard`: issuer volume, monthly trend and engagement charts
- `Monthly_Mentions`: date-based issuer summary
- `Engagement`: retweet and favourite metrics
- `Quality`: filtering and coverage checks

## Suggested presentation disclaimer

> Demonstration workflow using published GitHub review and historical Twitter
> data. The review and social-listening modules use different populations,
> conclusions are directional, and reuse rights should be confirmed before
> external redistribution.
