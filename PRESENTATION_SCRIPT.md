# Indian Credit Card Brand Intelligence — Presentation Script

## How to use this script

This script is written for the current 9-slide PowerPoint deck:

`outputs/brand_intelligence_deck.pptx`

Expected delivery time: **5–7 minutes**.

Speak naturally rather than reading every word exactly. The text below gives
simple dialogue, key points and transitions.

---

## Opening — before Slide 1

**Say:**

> Good morning/afternoon. Today I am presenting my proof of work on Indian
> credit-card brand intelligence.
>
> I analysed customer review data for HDFC Bank, SBI Card and ICICI Bank. The
> goal was to understand the topics customers discuss and the sentiment
> associated with those discussions.
>
> This is an issuer-level analysis using published pure credit-card reviews. It
> is a demonstration of the workflow rather than a complete market study.

---

## Slide 1 — Title and objective

**Time: 30 seconds**

**Say:**

> The project is called Indian Credit Card Brand Intelligence.
>
> I chose this topic because credit-card customers frequently discuss rewards,
> cashback, fees, benefits and service experiences. These are useful topics for
> a Marketing Strategy team because they can influence acquisition,
> communication and customer retention.
>
> The final analysis contains 1,771 unique pure credit-card reviews.

**Transition:**

> I will first explain the questions I wanted the analysis to answer.

---

## Slide 2 — Objective and research questions

**Time: 35 seconds**

**Say:**

> I focused on three questions.
>
> First, how much review volume is available for each issuer?
>
> Second, how does the sentiment mix differ between issuers?
>
> Third, which topics appear most often and where do negative experiences
> appear?
>
> These questions are intentionally practical. They connect the data work to
> the type of reporting a Marketing Strategy team would use.

**Transition:**

> Next, I will explain the data source and how I processed it.

---

## Slide 3 — Data and methodology

**Time: 55 seconds**

**Say:**

> I used a published GitHub dataset called “Sentiment Analysis on Credit Cards
> using Online Reviews.”
>
> The source contains credit-card review text, issuer names, topic labels and
> sentiment scores.
>
> I selected records for HDFC Bank, SBI Card and ICICI Bank. I excluded
> banking-app reviews and general bank commentary because the requirement was
> to use pure credit-card reviews.
>
> I standardised the issuer names, cleaned the review text, removed exact
> duplicate reviews and retained the original source score and topic.
>
> The source score was converted into three simple labels: positive, neutral
> and negative.

**Important disclaimer:**

> The source does not reliably provide specific card names, so this is an
> issuer-level analysis. It does not compare products such as Millennia,
> Regalia, SBI Cashback or ICICI Coral.

**Transition:**

> Before looking at the findings, I checked the quality and coverage of the
> dataset.

---

## Slide 4 — Dataset profile and quality

**Time: 45 seconds**

**Say:**

> After cleaning, the dataset contains 1,771 records.
>
> SBI Card has 1,368 records, HDFC Bank has 212 and ICICI Bank has 191.
>
> All records are pure credit-card reviews, but the issuer coverage is not
> balanced. I decided not to delete SBI records simply to make the counts
> equal. Keeping all valid observations is more transparent.
>
> Therefore, the SBI volume should be understood as source volume and not as
> market share.
>
> Publication dates and engagement values are not reliably available in this
> source, so I did not invent them.

**Transition:**

> With that limitation in mind, the next slide shows the review volume by
> issuer.

---

## Slide 5 — Share of voice proxy

**Time: 40 seconds**

**Say:**

> This chart shows the distribution of records in the source.
>
> SBI Card represents 77.2% of the records, HDFC Bank 12.0% and ICICI Bank
> 10.8%.
>
> I call this a “share of voice proxy” rather than share of voice because the
> sample is not balanced and does not represent the entire market.
>
> The practical takeaway is that raw review counts cannot be used to say that
> one issuer has more customers or stronger market presence.

**Transition:**

> I then compared sentiment percentages within each issuer.

---

## Slide 6 — Sentiment comparison

**Time: 55 seconds**

**Say:**

> HDFC Bank has 65.1% positive, 34.4% neutral and 0.5% negative reviews.
>
> SBI Card has 63.7% positive, 34.8% neutral and 1.5% negative reviews.
>
> ICICI Bank has 50.3% positive, 48.7% neutral and 1.0% negative reviews.
>
> In this sample, HDFC and SBI show higher positive shares than ICICI.
> However, this is a directional observation, not a national customer
> satisfaction ranking.
>
> There are only 24 negative reviews in total, so the negative percentages are
> too small to support strong complaint-prevalence conclusions.

**Transition:**

> I also grouped the reviews into business topics.

---

## Slide 7 — Topic-level competitor comparison

**Time: 45 seconds**

**Say:**

> The main topics are benefits, fees, rewards and cashback.
>
> Benefits is the largest topic in the current analysis. Fees and rewards are
> also recurring themes.
>
> These topics are useful for marketing because they can be connected to
> product positioning and customer communication.
>
> For example, rewards and cashback can inform acquisition messaging, while
> fees and service-related comments can identify areas where explanations or
> customer support may need improvement.
>
> Because SBI has more records, I use within-issuer percentages for comparison
> instead of comparing only raw topic counts.

**Transition:**

> Based on this analysis, I developed four practical recommendations.

---

## Slide 8 — Key findings and recommendations

**Time: 55 seconds**

**Say:**

> My first recommendation is not to interpret SBI’s larger source volume as
> market leadership.
>
> Second, the sentiment percentages suggest that HDFC and SBI are more
> positive than ICICI in this sample, but this should be validated with a
> larger and more balanced source.
>
> Third, the low number of negative records means complaint findings should be
> treated as hypotheses rather than final conclusions.
>
> Fourth, the next version should add an approved Axis Bank source and more
> comparable HDFC and ICICI credit-card reviews.
>
> From a recurring-study perspective, I would refresh the data monthly, track
> issuer, topic, sentiment, date and engagement, and maintain a manual
> validation sample.

**Transition:**

> I will close with the limitations and the next steps.

---

## Slide 9 — Limitations and next steps

**Time: 45 seconds**

**Say:**

> The main limitations are that Axis Bank is not included, the issuer sample
> sizes are uneven, publication dates and engagement are unavailable, and
> specific card names are not reliably provided.
>
> The source also needs a reuse-rights check before the raw review text is
> redistributed publicly.
>
> The next step would be to obtain an approved social-listening export or
> another permitted source with comparable card-level reviews, dates and
> engagement.
>
> After that, I would manually validate a sample of sentiment and topic
> labels, refresh the dashboard and compare changes over time.

---

## Closing statement

**Say:**

> To summarise, this proof of work demonstrates the full analyst workflow:
> sourcing permitted review data, cleaning it in Python, structuring sentiment
> and topics, creating summary tables, building an Excel dashboard and
> presenting the results in PowerPoint.
>
> The main learning from the project is that data quality and source coverage
> are as important as the charts. I have therefore kept the SBI records,
> disclosed the imbalance, excluded non-card reviews and avoided presenting
> source volume as market share.
>
> Thank you. I am happy to take questions.

---

## Likely questions and simple answers

### Why is Axis Bank missing?

> I could not find a verified, downloadable pure credit-card review dataset for
> Axis Bank. I chose not to fabricate or mix in unrelated bank reviews. The
> next step would be to obtain an approved Axis source.

### Why did you not reduce the SBI records?

> I did not want to discard valid observations just to create artificial
> balance. I retained all unique SBI reviews and clearly disclosed the
> imbalance. For comparison, I use percentages and sample sizes.

### Are these reviews for specific cards?

> No. The source identifies the issuer but does not reliably identify
> individual products. Therefore, the analysis is at issuer level only.

### How did you calculate sentiment?

> I retained the source sentiment score and mapped scores above 0.1 to
> positive, below -0.1 to negative, and the middle range to neutral.

### How did you classify topics?

> I used the published source topic labels and mapped them into business
> categories such as benefits, fees, rewards and cashback. I used a transparent
> keyword fallback where a source topic could not be mapped.

### Can these findings be called market share?

> No. The dataset is a published review sample with uneven issuer coverage.
> The volume chart is only a source-volume proxy.

### Why are dates and engagement missing?

> The selected source did not reliably provide those fields. I left them
> unavailable instead of creating artificial values.

### Can the raw CSV be published?

> Not until the source reuse and redistribution rights are confirmed. The
> dashboard and methodology can be demonstrated while the rights check is
> pending.

### What would you do with more time?

> I would obtain approved platform exports, add Axis Bank, collect product-level
> card names where explicitly available, validate labels manually and create a
> monthly trend tracker.

---

## Delivery reminders

- Start with the disclaimer, not the chart.
- Say “in this sample” instead of making national claims.
- Say “source-volume proxy” instead of “market share.”
- Do not say the dataset compares Millennia, Regalia, Coral or other specific
  cards.
- Do not describe app reviews or bank commentary as part of the final analysis.
- Mention that all unique SBI records were retained.
- Pause after Slide 6 so the audience can understand the sentiment comparison.
- Keep the detailed limitations for the end unless someone asks earlier.
