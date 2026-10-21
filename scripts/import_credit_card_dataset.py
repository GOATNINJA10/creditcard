from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "source" / "sentiment_reviews_credit_data.csv"
ICICI_PATH = ROOT / "data" / "source" / "ICICI_App_Reviews.csv"
ICICI_GITHUB_PATH = ROOT / "data" / "source" / "ICICI_Bank_reviews_github.csv"
HDFC_PATH = ROOT / "data" / "source" / "HDFC_Reviews.xlsx"
OUTPUT_PATH = ROOT / "data" / "raw_data.csv"
BALANCED_PATH = ROOT / "data" / "analysis_data.csv"
SOURCE_URL = (
    "https://github.com/kyasanur/"
    "Sentiment-Analysis-on-Credit-Cards-using-Online-Reviews"
)
ICICI_URL = "https://github.com/Bharatsoni19/icici-sentiment-analyzer"
ICICI_GITHUB_URL = "https://github.com/vivek2005Bot/Sentiment-Analysis-On-Fintech-Application-Reviews"
HDFC_URL = "https://github.com/Sumendhs01/HDFC_Sentiment_Analysis"


def main() -> None:
    source = pd.read_csv(SOURCE_PATH)
    source = source[source["bank_name"].isin(
        [
            "State Bank of India Credit Card",
            "HDFC Bank Credit Card",
            "ICICI Bank Credit Card",
        ]
    )].copy()
    source["bank_name"] = source["bank_name"].replace(
        {
            "State Bank of India Credit Card": "SBI Card",
            "HDFC Bank Credit Card": "HDFC Bank",
            "ICICI Bank Credit Card": "ICICI Bank",
        }
    )
    source["review_text"] = source["reviews"].fillna("").astype(str).str.strip()
    source["source"] = "Published GitHub credit-card review dataset"
    source["record_type"] = "credit_card_review"
    source["card_name"] = "Multiple cards / unspecified"
    source["published_date"] = pd.NaT
    source["engagement"] = 0
    source["source_url"] = SOURCE_URL
    source["source_sentiment_score"] = pd.to_numeric(source["sentiment"], errors="coerce")
    source["source_topic"] = source["topic"].fillna("").astype(str)
    source.insert(0, "record_id", [f"CC{i:04d}" for i in range(1, len(source) + 1)])
    source["source_period"] = ""
    icici = pd.read_csv(ICICI_PATH)
    icici["bank_name"] = "ICICI Bank"
    icici["card_name"] = "Unspecified / banking app"
    icici["source"] = "Published GitHub ICICI app review dataset"
    icici["record_type"] = "banking_app_review"
    icici["review_text"] = icici["Review_Text"].fillna("").astype(str).str.strip()
    icici["source_url"] = ICICI_URL
    icici["source_sentiment_score"] = (pd.to_numeric(icici["Stars"], errors="coerce") - 3) / 2
    icici["source_topic"] = ""
    icici["published_date"] = pd.NaT
    icici["engagement"] = 0
    icici["source_period"] = icici["Month"].fillna("").astype(str)
    icici = icici[["bank_name", "card_name", "source", "record_type", "published_date",
                   "review_text", "engagement", "source_url", "source_sentiment_score",
                   "source_topic", "source_period"]]

    icici_github = pd.read_csv(ICICI_GITHUB_PATH)
    icici_github["bank_name"] = "ICICI Bank"
    icici_github["card_name"] = "Unspecified / banking app"
    icici_github["source"] = "Published GitHub fintech app review dataset"
    icici_github["record_type"] = "banking_app_review"
    icici_github["review_text"] = icici_github["content"].fillna("").astype(str).str.strip()
    icici_github["source_url"] = ICICI_GITHUB_URL
    icici_github["source_sentiment_score"] = (
        pd.to_numeric(icici_github["score"], errors="coerce") - 3
    ) / 2
    icici_github["source_topic"] = ""
    icici_github["published_date"] = pd.to_datetime(icici_github["at"], errors="coerce")
    icici_github["engagement"] = pd.to_numeric(
        icici_github["thumbsUpCount"], errors="coerce"
    ).fillna(0)
    icici_github["source_period"] = icici_github["published_date"].dt.strftime("%Y-%m")
    icici_github = icici_github[[
        "bank_name", "card_name", "source", "record_type", "published_date",
        "review_text", "engagement", "source_url", "source_sentiment_score",
        "source_topic", "source_period"
    ]]

    hdfc = pd.read_excel(HDFC_PATH)
    hdfc["bank_name"] = "HDFC Bank"
    hdfc["card_name"] = "Unspecified bank product"
    hdfc["source"] = "Published GitHub HDFC sentiment dataset"
    hdfc["record_type"] = "bank_commentary"
    hdfc["review_text"] = hdfc["English"].fillna("").astype(str).str.strip()
    hdfc["source_url"] = HDFC_URL
    hdfc["source_sentiment_score"] = hdfc["sentiment"].map(
        {"Positive": 1.0, "Neutral": 0.0, "Negative": -1.0}
    )
    hdfc["source_topic"] = ""
    hdfc["published_date"] = pd.NaT
    hdfc["engagement"] = 0
    hdfc["source_period"] = ""
    hdfc = hdfc[["bank_name", "card_name", "source", "record_type", "published_date",
                 "review_text", "engagement", "source_url", "source_sentiment_score",
                 "source_topic", "source_period"]]

    source = pd.concat(
        [
            source[["bank_name", "card_name", "source", "record_type", "published_date",
                    "review_text", "engagement", "source_url", "source_sentiment_score",
                    "source_topic", "source_period"]],
            icici,
            icici_github,
            hdfc,
        ],
        ignore_index=True,
    )
    columns = [
        "record_id",
        "bank_name",
        "card_name",
        "source",
        "record_type",
        "published_date",
        "review_text",
        "engagement",
        "source_url",
        "source_sentiment_score",
        "source_topic",
        "source_period",
    ]
    source["record_id"] = [f"CC{i:04d}" for i in range(1, len(source) + 1)]
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    source[columns].to_csv(OUTPUT_PATH, index=False)
    deduped = source[
        source["review_text"].ne("")
        & source["record_type"].eq("credit_card_review")
    ].drop_duplicates(subset=["review_text"])
    deduped.to_csv(BALANCED_PATH, index=False)
    print(f"Imported {len(source)} published review records")
    print(f"Created full analysis sample with {len(deduped)} unique records")
    print(source["bank_name"].value_counts().to_string())


if __name__ == "__main__":
    main()
