# Dataset and PoW Decisions

Date: 21 October 2026

## Objective

Create a reproducible proof of work for customer-review and sentiment analysis
of Indian credit-card issuers using a directly downloadable, already-published
dataset rather than scraping restricted websites.

## Dataset selected

Selected source:

`https://github.com/kyasanur/Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews`

Downloaded source file:

`data/source/sentiment_reviews_credit_data.csv`

The source contains 3,074 credit-card review records with bank name, review
text, sentiment score, topic, and derived text statistics. The project imports
only the target issuers present in the source:

- HDFC Bank: 256 records
- SBI Card: 1,600 records
- ICICI Bank: 223 records

The source contains no Axis Bank records. Axis Bank has therefore been excluded
from the current analysis instead of being fabricated or filled with synthetic
records.

## Why this source was chosen

- It is explicitly about credit-card online reviews.
- It includes customer-review text.
- It includes a numeric sentiment score.
- It includes HDFC, SBI and ICICI credit-card records.
- It is downloadable without scraping a live website.

## Rejected source

`data/source/BankReviews.xlsx` was downloaded from:

`https://github.com/GurpreetKaur28/Analysing-Bank-Reviews-Complaints`

It was rejected for the main analysis because its 505 records describe US
mortgage companies, not Indian credit-card issuers. It must not be relabelled
as HDFC, SBI, ICICI or Axis data.

## Changes made

### Data

- Added `scripts/import_credit_card_dataset.py`.
- Converted the published source into the project's standard `raw_data.csv`
  schema.
- Added `source_url` for provenance.
- Added `source_sentiment_score` to preserve the original score.
- Added `source_topic` to preserve the source topic.
- Standardized issuer names to `HDFC Bank`, `SBI Card` and `ICICI Bank`.
- Set card name to `Multiple cards / unspecified` because the source does not
  provide a reliable card-level value for every record.
- Left publication date and engagement blank/zero because the source does not
  provide reliable values for this project.

### Analysis

- Sentiment labels now derive from the source score:
  - score greater than `0.1`: Positive
  - score less than `-0.1`: Negative
  - otherwise: Neutral
- Duplicate review text is removed during cleaning.
- Topics are assigned with the existing transparent keyword baseline.
- The dashboard and deck now describe the actual published dataset rather than
  the former synthetic demo fixture.

### Outputs

Regenerated:

- `data/cleaned_data.csv`
- `outputs/summary_tables.xlsx`
- `outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`
- `outputs/Indian_Credit_Card_Brand_Intelligence_PoW.pptx`
- `outputs/charts/mentions.png`
- `outputs/charts/sentiment.png`
- `outputs/charts/topic_sentiment.png`

## Reproducibility

Run:

```powershell
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/import_credit_card_dataset.py
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/pow_pipeline.py
```

## Limitations and decisions still needed

1. Confirm the source repository's reuse license before external publication.
2. Add a permitted Axis Bank review source if four-issuer comparison is
   mandatory.
3. Validate a manual sample of topic and sentiment labels.
4. Avoid claiming that the dataset represents all Indian cardholders.
5. Replace missing dates and engagement with source fields only when they can
   be verified.

## Analysis audit and updates — 21 October 2026

### Quality findings

The cleaned analysis contains 1,771 records after exact review-text
deduplication:

- SBI Card: 1,368 records (77.2%)
- HDFC Bank: 212 records (12.0%)
- ICICI Bank: 191 records (10.8%)

This is materially imbalanced. The dashboard now treats mention counts as
source-volume share, not market share, and recommendations avoid comparing raw
counts across issuers.

The source sentiment distribution is:

- Positive: 1,105 (62.4%)
- Neutral: 642 (36.2%)
- Negative: 24 (1.4%)

Because the negative class is very small, negative-topic rankings are
directional only. They should not be presented as statistically reliable
complaint prevalence.

The source provides no usable publication dates or engagement values after
import. These fields remain explicitly unavailable rather than being filled
with fabricated values.

### New analysis features

- Added a `Bank_Profile` summary with issuer volume, positive/neutral/negative
  shares and average source sentiment score.
- Added `Topic_Sentiment` counts for topic-level analysis.
- Added `Negative_Examples` with review IDs, issuers, topics and source scores.
- Added a `Quality` sheet with record counts, duplicate removal, missingness,
  negative-class size and issuer concentration.
- Updated the Excel dashboard and summary workbook to include all audit tables.
- Updated the presentation with actual issuer volume and sentiment results.
- Added explicit warnings about source imbalance, missing Axis coverage and the
  sparse negative class.
- Updated the generated date to 21 October 2026.

### Decision-grade interpretation

The current PoW can demonstrate data cleaning, provenance handling, sentiment
analysis, topic structuring, dashboarding and presentation skills. It cannot
support a definitive competitive-market conclusion because:

1. Axis Bank is absent.
2. SBI Card is overrepresented.
3. The source sentiment distribution is strongly positive.
4. Dates and engagement are unavailable.
5. The source repository does not expose an explicit reuse license in its root
   files.

The recommended wording in any interview presentation is:

> “In this published credit-card review sample, HDFC and SBI have higher
> positive-share percentages than ICICI. The sample is imbalanced and contains
> very few negative reviews, so this is a directional signal rather than a
> market estimate.”

### Next required work

1. Confirm permission/license for the source before sharing the CSV.
2. Add an approved Axis Bank review source or change the project title to a
   three-issuer analysis.
3. Manually label a validation sample, especially the 24 negative reviews and
   a random sample of positive/neutral records.
4. Obtain a second, more recent source with dates and engagement.
5. Re-run the analysis after source balancing or report confidence intervals
   and sample sizes alongside issuer percentages.

## GitHub balancing update — 21 October 2026

### Supplemental sources found

Two additional public GitHub datasets were reviewed and downloaded:

1. [ICICI sentiment analyzer](https://github.com/Bharatsoni19/icici-sentiment-analyzer)
   - `P6_App_Reviews.csv`
   - 500 records
   - Review text, 1–5 star rating and month
   - Classified as `banking_app_review`, not card-specific review

2. [HDFC Sentiment Analysis](https://github.com/Sumendhs01/HDFC_Sentiment_Analysis)
   - `new_sentimental.xlsx`
   - 100 records
   - English text and Positive/Neutral/Negative labels
   - Classified as `bank_commentary`; the repository describes manually collected
     bank/news text and does not establish that every record is a customer or
     credit-card review

The files are retained under `data/source/` with source URLs recorded in the
standardized data.

### Data integration changes

- Added `record_type` to distinguish:
  - `credit_card_review`
  - `banking_app_review`
  - `bank_commentary`
- Added `source_period` where the source provided a month.
- Converted ICICI star ratings to the common sentiment-score scale:
  - `(stars - 3) / 2`
- Preserved HDFC's published sentiment labels as scores:
  - Positive = `1.0`
  - Neutral = `0.0`
  - Negative = `-1.0`
- Added `data/analysis_data.csv` as the full unique analysis sample.
- `scripts/pow_pipeline.py` now uses `analysis_data.csv` when available.
- The full combined source remains in `data/raw_data.csv`.

### Full-sample result

The combined source contains 2,679 records:

- SBI Card credit-card reviews: 1,600
- ICICI Bank: 223 credit-card reviews plus 500 app reviews
- HDFC Bank: 256 credit-card reviews plus 100 bank-commentary records

After exact review-text deduplication, all unique records are now retained,
including every available SBI Card record. The full analysis sample contains
1,905 records:

- SBI Card: 1,368 credit-card reviews
- ICICI Bank: 226 records
- HDFC Bank: 311 records

No valid SBI observations are discarded. The product mix still differs, so HDFC
and ICICI supplemental records must not be described as pure credit-card
reviews.

### Updated interpretation rule

Use the full sample for transparency and retain all SBI observations. For issuer
comparisons, report record counts, within-issuer percentages and record type.
Do not call the output market share, customer satisfaction score or card-only
sentiment benchmark until comparable card-level data exists for all issuers.

### Files added or changed

- Added `data/source/ICICI_App_Reviews.csv`
- Added `data/source/HDFC_Reviews.xlsx`
- Added `data/analysis_data.csv`
- Updated `data/raw_data.csv`
- Updated `data/cleaned_data.csv`
- Updated `scripts/import_credit_card_dataset.py`
- Updated `scripts/pow_pipeline.py`
- Regenerated the Excel dashboard, summary workbook, charts and PowerPoint

### Remaining work

1. Verify redistribution rights for both GitHub sources.
2. Replace HDFC bank commentary with customer/card reviews if possible.
3. Replace ICICI app reviews with card-level reviews if possible.
4. Add an Axis Bank source with the same product scope.
5. Manually validate sentiment labels and record type on a sample.

## Full SBI sample decision — 21 October 2026

The analysis no longer downsamples SBI Card. The previous 226-per-issuer
sample was removed because it discarded valid SBI observations. The importer
now writes every non-empty, exact-deduplicated record to `analysis_data.csv`.
This preserves the full SBI sample and makes the data-loss decision explicit.

The consequence is issuer imbalance: SBI has substantially more records than
HDFC and ICICI. The dashboard and presentation warn that raw mention counts are
source-volume measures, not market share. Comparisons should use within-issuer
percentages and include sample sizes.

## Additional GitHub source audit — 21 October 2026

### ICICI source added

Added:

`data/source/ICICI_Bank_reviews_github.csv`

Repository:

`https://github.com/vivek2005Bot/Sentiment-Analysis-On-Fintech-Application-Reviews`

The file contains 1,000 ICICI banking-app review records with review text,
1–5 score, timestamp, thumbs-up count and app-version fields. It is imported as
`record_type = banking_app_review`, not as credit-card review. Star scores are
converted to the common sentiment scale using `(score - 3) / 2`. Dates and
thumbs-up counts are retained where available.

Exact review-text deduplication is applied across all sources, so the same
review is not counted twice when it appears in both ICICI files.

### HDFC search result

The HDFC file in the same fintech repository,
`Pvt_Banks/HDFC_Bank_reviews.csv`, is only a 4-byte empty/header file and
contains no review records. It was downloaded for verification but is not
included in the analysis. No additional valid HDFC review file was found in
the GitHub search pass beyond the existing 100-record HDFC commentary source.

### Resulting data decision

The importer now retains all available unique source records, including the
additional ICICI app reviews and all SBI reviews. ICICI has more app-review
coverage, but HDFC remains limited. This improves ICICI coverage without
pretending that app reviews are card reviews. The deck and workbook should
continue to show `record_type` and source mix before interpreting comparisons.

After this update, the full unique analysis contains 2,593 records:

- SBI Card: 1,368
- ICICI Bank: 1,014
- HDFC Bank: 311

ICICI's increase comes from 688 unique records from the additional GitHub app
file after cross-source deduplication. The current comparison is therefore
better covered for ICICI but remains source- and product-mixed, with HDFC still
the least represented issuer.

## Pure credit-card analysis decision — 21 October 2026

The analytical dataset must contain only pure credit-card reviews. Therefore:

- `record_type = credit_card_review` is the only record type included in
  `analysis_data.csv` and downstream outputs.
- ICICI banking-app reviews are excluded from analysis.
- HDFC bank/news commentary is excluded from analysis.
- All SBI credit-card records are retained.
- Excluded source files remain under `data/source/` for provenance only; they do
  not affect the current dashboard, summary tables or presentation.

The pure credit-card analysis contains:

- SBI Card: 1,368
- HDFC Bank: 212
- ICICI Bank: 191
- Total: 1,771 unique reviews

This is not issuer-balanced, but it is product-consistent. Raw counts remain
source-volume counts rather than market share. Comparisons should show sample
sizes and within-issuer percentages.

## Excel dashboard update — 21 October 2026

The final workbook is:

`outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`

The record-level dataset is on the `Data` sheet. It contains 1,771 data rows
plus the header and matches `data/cleaned_data.csv`.

The `Dashboard` sheet now contains three embedded Excel charts:

1. Review volume by issuer (source-volume proxy)
2. Sentiment mix by issuer (%)
3. Topic-level sentiment

The `Pivot_Tables` sheet contains generated pivot-style summaries for issuer
volume, issuer sentiment, issuer topics and topic-level sentiment. These are
visible summary tables generated from Python rather than native Excel
PivotTable objects; this keeps the workbook reproducible with the current
tooling.

The chart inputs were checked against the cleaned CSV:

- SBI Card: 1,368
- HDFC Bank: 212
- ICICI Bank: 191
- Total: 1,771

The workbook is now the main presentation-ready analysis file. The separate
PNG charts remain as exportable assets, but they are not required to present
the dashboard.
