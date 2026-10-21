# Indian Credit Card Brand Intelligence PoW

This is a two-day proof-of-work package comparing HDFC Bank, SBI Card, ICICI Bank
and Axis Bank across public credit-card discussion themes.

## Important data note

The current `data/raw_data.csv` is derived from the published
[Sentiment Analysis on Credit Cards using Online Reviews](https://github.com/kyasanur/Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews)
repository. It contains review text and source sentiment scores for HDFC Bank,
ICICI Bank and SBI Card. It contains no Axis Bank records, so Axis is not
included in the current comparison. The source repository does not expose an
explicit license in its root files; verify reuse rights before external
redistribution.

## Run

```powershell
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/import_credit_card_dataset.py
C:/Users/KshitijLaptop/scoop/shims/python3.exe scripts/pow_pipeline.py
```

The pipeline creates:

- `data/cleaned_data.csv`
- `outputs/summary_tables.xlsx`
- `outputs/Indian_Credit_Card_Brand_Intelligence_PoW.xlsx`
- `outputs/brand_intelligence_deck.pptx`
- `outputs/charts/*.png`

The analysis uses the source sentiment score for sentiment labels and a
transparent keyword-based topic baseline. For production work, replace or
augment it with a validated social-listening taxonomy and manually review a
sample of classifications.

## Input schema

`record_id`, `bank_name`, `card_name`, `source`, `published_date`,
`review_text`, and optional `engagement`.

## Suggested presentation disclaimer

> Demonstration workflow using synthetic records; conclusions are illustrative
> until validated against an approved social-listening export.
