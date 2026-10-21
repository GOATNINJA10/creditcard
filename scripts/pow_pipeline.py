from __future__ import annotations

from pathlib import Path
import re
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
RAW_PATH = DATA_DIR / "raw_data.csv"
ANALYSIS_PATH = DATA_DIR / "analysis_data.csv"
DATE = "2026-10-21"


TOPIC_KEYWORDS = {
    "Cashback": ["cashback", "cash back", "fuel surcharge", "discount"],
    "Rewards": ["reward", "points", "milestone", "redemption", "travel"],
    "Fees": ["fee", "annual", "surcharge", "charge", "forex"],
    "Benefits": ["lounge", "benefit", "offer", "movie", "insurance"],
    "Customer service": ["support", "customer care", "complaint", "chargeback", "resolve"],
}
POSITIVE = ["love", "great", "good", "easy", "useful", "excellent", "helpful", "smooth"]
NEGATIVE = ["bad", "poor", "hate", "delay", "denied", "hidden", "issue", "frustrating", "charged"]
SOURCE_TOPIC_MAP = {
    "reward": "Rewards",
    "benefit": "Benefits",
    "offer": "Benefits",
    "fuel": "Cashback",
    "credit": "Fees",
    "spending": "Benefits",
    "card": "Benefits",
}


def make_demo_data() -> pd.DataFrame:
    """Create a balanced, explicitly synthetic fixture for demonstrating the workflow."""
    banks = [
        ("HDFC Bank", "Millennia"),
        ("SBI Card", "SBI Cashback"),
        ("ICICI Bank", "Amazon Pay"),
        ("Axis Bank", "ACE"),
    ]
    texts = [
        ("Cashback", "The cashback offer is good and easy to understand."),
        ("Cashback", "Cashback was denied on one transaction and support was slow."),
        ("Rewards", "Reward points are useful for travel and redemption is smooth."),
        ("Rewards", "The milestone reward feels confusing and difficult to redeem."),
        ("Fees", "The annual fee is reasonable for the benefits."),
        ("Fees", "A hidden charge appeared and the fee feels frustrating."),
        ("Benefits", "The lounge benefit and movie offer are great."),
        ("Benefits", "The lounge access was denied despite meeting the spend."),
        ("Customer service", "Customer care was helpful and resolved my complaint."),
        ("Customer service", "Support delay is a poor experience and the issue remains."),
    ]
    rows: list[dict[str, object]] = []
    for i in range(240):
        bank, card = banks[i % len(banks)]
        topic, text = texts[i % len(texts)]
        rows.append(
            {
                "record_id": f"CC{i + 1:04d}",
                "bank_name": bank,
                "card_name": card,
                "source": "Synthetic demo",
                "published_date": f"2026-{(i % 9) + 1:02d}-{(i % 27) + 1:02d}",
                "review_text": f"{bank} {card}: {text} Context sample {i + 1}.",
                "engagement": (i * 7) % 101,
            }
        )
    return pd.DataFrame(rows)


def classify_topic(text: str) -> str:
    lowered = text.lower()
    scores = {topic: sum(word in lowered for word in words) for topic, words in TOPIC_KEYWORDS.items()}
    return max(scores, key=scores.get) if max(scores.values()) else "Other"


def classify_sentiment(text: str) -> str:
    lowered = text.lower()
    positive = sum(word in lowered for word in POSITIVE)
    negative = sum(word in lowered for word in NEGATIVE)
    if positive > negative:
        return "Positive"
    if negative > positive:
        return "Negative"
    return "Neutral"


def clean_data() -> pd.DataFrame:
    input_path = ANALYSIS_PATH if ANALYSIS_PATH.exists() else RAW_PATH
    if not input_path.exists():
        DATA_DIR.mkdir(exist_ok=True)
        make_demo_data().to_csv(RAW_PATH, index=False)
        input_path = RAW_PATH
    df = pd.read_csv(input_path)
    required = ["record_id", "bank_name", "card_name", "source", "published_date", "review_text"]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    df = df.copy()
    df["review_text"] = df["review_text"].fillna("").astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    df["bank_name"] = df["bank_name"].astype(str).str.strip()
    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df["engagement"] = pd.to_numeric(df.get("engagement", 0), errors="coerce").fillna(0)
    input_records = len(df)
    df = df[df["review_text"].ne("")].drop_duplicates(subset=["review_text"]).reset_index(drop=True)
    df.attrs["input_records"] = input_records
    df.attrs["analysis_input"] = input_path.name
    if "source_topic" in df.columns:
        source_topics = df["source_topic"].str.lower().map(SOURCE_TOPIC_MAP)
        df["topic"] = source_topics.fillna(df["review_text"].map(classify_topic))
    else:
        df["topic"] = df["review_text"].map(classify_topic)
    if "source_sentiment_score" in df.columns:
        score = pd.to_numeric(df["source_sentiment_score"], errors="coerce")
        df["sentiment"] = score.map(
            lambda value: "Positive" if value > 0.1 else ("Negative" if value < -0.1 else "Neutral")
        )
    else:
        df["sentiment"] = df["review_text"].map(classify_sentiment)
    df.to_csv(DATA_DIR / "cleaned_data.csv", index=False, date_format="%Y-%m-%d")
    return df


def build_summaries(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    mentions = df.groupby("bank_name").size().reset_index(name="mentions").sort_values("mentions", ascending=False)
    sentiment = pd.crosstab(df["bank_name"], df["sentiment"], normalize="index").mul(100).round(1).reset_index()
    topics = pd.crosstab(df["bank_name"], df["topic"]).reset_index()
    bank_profile = (
        df.groupby("bank_name")
        .agg(
            reviews=("record_id", "size"),
            positive_share=("sentiment", lambda values: round((values == "Positive").mean() * 100, 1)),
            neutral_share=("sentiment", lambda values: round((values == "Neutral").mean() * 100, 1)),
            negative_share=("sentiment", lambda values: round((values == "Negative").mean() * 100, 1)),
            average_source_score=("source_sentiment_score", "mean"),
        )
        .reset_index()
        .sort_values("reviews", ascending=False)
    )
    topic_sentiment = (
        pd.crosstab([df["topic"], df["sentiment"]], columns="records")
        .reset_index()
        .pivot(index="topic", columns="sentiment", values="records")
        .fillna(0)
        .reset_index()
    )
    complaints = (
        df[df["sentiment"].eq("Negative")]
        .groupby(["bank_name", "topic"])
        .size()
        .reset_index(name="negative_mentions")
        .sort_values("negative_mentions", ascending=False)
    )
    negative_examples = df[df["sentiment"].eq("Negative")][
        ["record_id", "bank_name", "topic", "review_text", "source_sentiment_score"]
    ].sort_values("source_sentiment_score")
    quality = pd.DataFrame(
        {
            "check": [
                "Input records",
                "Cleaned records",
                "Exact duplicate reviews removed",
                "Issuers covered",
                "Missing publication dates (%)",
                "Missing/zero engagement (%)",
                "Negative reviews",
                "Largest issuer share (%)",
            ],
            "value": [
                int(df.attrs.get("input_records", len(df))),
                len(df),
                int(df.attrs.get("input_records", len(df)) - len(df)),
                df["bank_name"].nunique(),
                round(df["published_date"].isna().mean() * 100, 1),
                round((df["engagement"].eq(0)).mean() * 100, 1),
                int(df["sentiment"].eq("Negative").sum()),
                round(df["bank_name"].value_counts(normalize=True).max() * 100, 1),
            ],
        }
    )
    overall = pd.DataFrame(
        {
            "metric": ["Total records", "Issuers", "Topics", "Positive share (%)", "Negative share (%)"],
            "value": [
                len(df),
                df["bank_name"].nunique(),
                df["topic"].nunique(),
                round((df["sentiment"].eq("Positive").mean() * 100), 1),
                round((df["sentiment"].eq("Negative").mean() * 100), 1),
            ],
        }
    )
    return {
        "overall": overall,
        "mentions": mentions,
        "sentiment": sentiment,
        "topics": topics,
        "bank_profile": bank_profile,
        "topic_sentiment": topic_sentiment,
        "complaints": complaints,
        "negative_examples": negative_examples,
        "quality": quality,
    }


def save_charts(df: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    ax = summaries["mentions"].plot.bar(x="bank_name", y="mentions", legend=False, color="#1f4e79", figsize=(8, 4))
    ax.set_title("Share of voice proxy: mentions by issuer")
    ax.set_xlabel("")
    ax.set_ylabel("Mentions")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "mentions.png", dpi=160)
    plt.close()

    sentiment = summaries["sentiment"].set_index("bank_name")[["Positive", "Neutral", "Negative"]]
    ax = sentiment.plot.bar(stacked=True, color=["#70ad47", "#b7c9d6", "#c00000"], figsize=(8, 4))
    ax.set_title("Sentiment mix by issuer")
    ax.set_xlabel("")
    ax.set_ylabel("Share (%)")
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.15))
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sentiment.png", dpi=160)
    plt.close()

    topic = pd.crosstab(df["topic"], df["sentiment"])[["Positive", "Neutral", "Negative"]]
    ax = topic.plot.bar(stacked=True, color=["#70ad47", "#b7c9d6", "#c00000"], figsize=(8, 4))
    ax.set_title("Topic-level sentiment")
    ax.set_xlabel("")
    ax.set_ylabel("Records")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "topic_sentiment.png", dpi=160)
    plt.close()


def build_excel(df: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> Path:
    path = OUTPUT_DIR / "Indian_Credit_Card_Brand_Intelligence_PoW.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Data", index=False)
        for name, table in summaries.items():
            table.to_excel(writer, sheet_name=name.title(), index=False)
        pd.DataFrame({"Dashboard note": [""]}).to_excel(writer, sheet_name="Dashboard", index=False)
        pivot_sections = {
            "Issuer volume": summaries["mentions"],
            "Issuer sentiment (%)": summaries["sentiment"],
            "Issuer topics": summaries["topics"],
            "Topic sentiment": summaries["topic_sentiment"],
        }
        row = 1
        for title, table in pivot_sections.items():
            pd.DataFrame([[title]]).to_excel(
                writer, sheet_name="Pivot_Tables", startrow=row - 1, index=False, header=False
            )
            table.to_excel(writer, sheet_name="Pivot_Tables", startrow=row, index=False)
            row += len(table) + 4
    wb = load_workbook(path)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E79")
            cell.alignment = Alignment(horizontal="center")
        for column in ws.columns:
            letter = column[0].column_letter
            ws.column_dimensions[letter].width = min(max(max(len(str(c.value or "")) for c in column) + 2, 12), 36)
    dash = wb["Dashboard"]
    dash.delete_rows(1, dash.max_row)
    dash.sheet_view.showGridLines = False
    dash.merge_cells("A1:Z1")
    dash["A1"] = "INDIAN CREDIT CARD BRAND INTELLIGENCE"
    dash["A1"].font = Font(bold=True, size=20, color="FFFFFF")
    dash["A1"].fill = PatternFill("solid", fgColor="1F4E79")
    dash["A1"].alignment = Alignment(horizontal="center", vertical="center")
    dash.row_dimensions[1].height = 34
    dash.merge_cells("A2:Z2")
    dash["A2"] = "Pure credit-card review sample | HDFC Bank | SBI Card | ICICI Bank"
    dash["A2"].font = Font(bold=True, size=11, color="1F4E79")
    dash["A2"].alignment = Alignment(horizontal="center")
    dash.merge_cells("A3:Z3")
    dash["A3"] = (
        "Directional source analysis — issuer volume is not market share; "
        "Axis Bank is not included in the current dataset."
    )
    dash["A3"].font = Font(italic=True, size=10, color="C00000")
    dash["A3"].alignment = Alignment(horizontal="center")

    kpi_fill = PatternFill("solid", fgColor="D9EAF7")
    kpi_border = Border(
        left=Side(style="thin", color="9FBAD0"),
        right=Side(style="thin", color="9FBAD0"),
        top=Side(style="thin", color="9FBAD0"),
        bottom=Side(style="thin", color="9FBAD0"),
    )
    kpis = [
        ("A5:D5", "A6:D7", "TOTAL REVIEWS", int(summaries["overall"].loc[0, "value"])),
        ("F5:I5", "F6:I7", "ISSUERS", int(summaries["overall"].loc[1, "value"])),
        ("K5:N5", "K6:N7", "POSITIVE SHARE", f"{summaries['overall'].loc[3, 'value']}%"),
        ("P5:S5", "P6:S7", "NEGATIVE SHARE", f"{summaries['overall'].loc[4, 'value']}%"),
    ]
    for label_range, value_range, label, value in kpis:
        dash.merge_cells(label_range)
        dash.merge_cells(value_range)
        label_cell = dash[label_range.split(":")[0]]
        value_cell = dash[value_range.split(":")[0]]
        label_cell.value = label
        value_cell.value = value
        for cell_range in (label_range, value_range):
            for row in dash[cell_range]:
                for cell in row:
                    cell.fill = kpi_fill
                    cell.border = kpi_border
                    cell.alignment = Alignment(horizontal="center", vertical="center")
        label_cell.font = Font(bold=True, size=9, color="1F4E79")
        value_cell.font = Font(bold=True, size=18, color="1F4E79")
    dash.row_dimensions[6].height = 24
    dash.row_dimensions[7].height = 24

    dash.merge_cells("A9:Z9")
    dash["A9"] = "Issuer volume and sentiment"
    dash["A9"].font = Font(bold=True, size=13, color="1F4E79")
    dash["A9"].fill = PatternFill("solid", fgColor="EAF2F8")
    dash["A9"].alignment = Alignment(horizontal="left")
    mentions = wb["Mentions"]
    chart = BarChart()
    chart.title = "Review volume by issuer (source-volume proxy)"
    chart.x_axis.title = "Issuer"
    chart.y_axis.title = "Number of reviews"
    chart.style = 10
    chart.add_data(Reference(mentions, min_col=2, min_row=1, max_row=mentions.max_row), titles_from_data=True)
    chart.set_categories(Reference(mentions, min_col=1, min_row=2, max_row=mentions.max_row))
    chart.height = 7.2
    chart.width = 13.5
    dash.add_chart(chart, "A10")

    sentiment = wb["Sentiment"]
    sentiment_chart = BarChart()
    sentiment_chart.type = "col"
    sentiment_chart.grouping = "stacked"
    sentiment_chart.overlap = 100
    sentiment_chart.title = "Sentiment mix by issuer (%)"
    sentiment_chart.x_axis.title = "Issuer"
    sentiment_chart.y_axis.title = "Share of reviews (%)"
    sentiment_chart.style = 11
    sentiment_chart.add_data(
        Reference(sentiment, min_col=2, max_col=4, min_row=1, max_row=sentiment.max_row),
        titles_from_data=True,
    )
    sentiment_chart.set_categories(Reference(sentiment, min_col=1, min_row=2, max_row=sentiment.max_row))
    sentiment_chart.height = 7.2
    sentiment_chart.width = 13.5
    dash.add_chart(sentiment_chart, "N10")

    topic_sentiment = wb["Topic_Sentiment"]
    topic_chart = BarChart()
    topic_chart.type = "col"
    topic_chart.grouping = "stacked"
    topic_chart.overlap = 100
    topic_chart.title = "Topic-level sentiment"
    topic_chart.x_axis.title = "Topic"
    topic_chart.y_axis.title = "Number of reviews"
    topic_chart.style = 12
    topic_chart.add_data(
        Reference(topic_sentiment, min_col=2, max_col=4, min_row=1, max_row=topic_sentiment.max_row),
        titles_from_data=True,
    )
    topic_chart.set_categories(
        Reference(topic_sentiment, min_col=1, min_row=2, max_row=topic_sentiment.max_row)
    )
    topic_chart.height = 7.2
    topic_chart.width = 27
    dash.add_chart(topic_chart, "A26")
    dash.merge_cells("A42:Z42")
    dash["A42"] = (
        "Method note: sentiment labels use the published source score; topics use source labels "
        "where available. See Pivot_Tables for the supporting summaries."
    )
    dash["A42"].font = Font(italic=True, size=9, color="666666")
    dash["A42"].alignment = Alignment(wrap_text=True)
    for column in range(1, 27):
        dash.column_dimensions[chr(64 + column) if column <= 26 else "Z"].width = 12
    dash.column_dimensions["A"].width = 16
    dash.column_dimensions["B"].width = 14
    wb.save(path)
    with pd.ExcelWriter(OUTPUT_DIR / "summary_tables.xlsx", engine="openpyxl") as writer:
        for name, table in summaries.items():
            table.to_excel(writer, sheet_name=name.title(), index=False)
    return path


def add_textbox(slide, text: str, left: float, top: float, width: float, height: float, size: int = 20, bold: bool = False) -> None:
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor(31, 78, 121)


def build_deck(df: pd.DataFrame, summaries: dict[str, pd.DataFrame]) -> Path:
    path = OUTPUT_DIR / "brand_intelligence_deck.pptx"
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    profile = summaries["bank_profile"].set_index("bank_name")
    voice = ", ".join(
        f"{name}: {int(row.reviews)} ({row.reviews / len(df) * 100:.1f}%)"
        for name, row in profile.iterrows()
    )
    sentiment_text = "\n".join(
        f"{name}: {row.positive_share:.1f}% positive | {row.neutral_share:.1f}% neutral | {row.negative_share:.1f}% negative"
        for name, row in profile.iterrows()
    )
    slides = [
        ("Indian Credit Card Brand Intelligence", "Proof of Work | Published credit-card review dataset | 21 October 2026"),
        ("Objective and research questions", "How does issuer visibility compare?\nWhich topics drive positive and negative conversation?\nWhere can Marketing prioritize deeper investigation?"),
        ("Data and methodology", f"{len(df)} deduplicated pure credit-card review records from the published GitHub source.\nOnly records labelled credit_card_review are included; app reviews and bank commentary are excluded.\nSource sentiment scores are mapped to positive, neutral and negative labels; topics use source labels where available."),
        ("Dataset profile and quality", f"{len(df)} deduplicated records | {df['bank_name'].nunique()} issuers | {df['topic'].nunique()} topics\nAll unique SBI credit-card records are retained. Issuer volume is unbalanced, so percentages and sample sizes accompany raw counts. Axis is excluded."),
        ("Share of voice proxy", voice + "\n\nThis is source-volume share, not market share or brand preference. SBI has more source records and therefore higher raw volume."),
        ("Sentiment comparison", sentiment_text + "\n\nOnly 24 reviews are negative, so differences are directional rather than statistically conclusive."),
        ("Topic-level competitor comparison", "Benefits is the dominant topic, followed by fees and rewards. SBI contributes most pure credit-card records; use within-issuer percentages rather than raw counts, while retaining all SBI records."),
        ("Key findings and recommendations", "1. SBI Card dominates source volume; do not interpret raw counts as performance.\n2. HDFC and SBI show higher positive shares than ICICI in this sample.\n3. Negative reviews are too sparse for strong complaint rankings.\n4. Add Axis data and a permitted current source before making market claims."),
        ("Limitations and next steps", "The analysis is pure credit-card review data but remains issuer-imbalanced, lacks Axis coverage, and has no reliable dates or engagement values. Reuse rights need confirmation.\nNext: obtain additional comparable card-level HDFC, ICICI and Axis reviews, QA labels, and refresh the dashboard."),
    ]
    for idx, (title, body) in enumerate(slides):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = RGBColor(245, 248, 250)
        add_textbox(slide, title, 0.7, 0.6, 12, 0.8, 28, True)
        add_textbox(slide, body, 0.9, 1.8, 11.4, 4.5, 20)
        if idx == 4:
            slide.shapes.add_picture(str(CHART_DIR / "mentions.png"), Inches(7.2), Inches(3.8), width=Inches(5.3))
        if idx == 5:
            slide.shapes.add_picture(str(CHART_DIR / "sentiment.png"), Inches(7.2), Inches(3.8), width=Inches(5.3))
        add_textbox(slide, "Illustrative PoW — not for external publication without approved data", 0.7, 7.05, 11, 0.25, 9)
    prs.save(path)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = clean_data()
    summaries = build_summaries(df)
    save_charts(df, summaries)
    build_excel(df, summaries)
    build_deck(df, summaries)
    print(f"Created {len(df)} cleaned records")
    print(f"Outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
