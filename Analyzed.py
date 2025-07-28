import pandas as pd
import re
import spacy
from textblob import TextBlob

# Load spaCy model
import en_core_web_sm
nlp = en_core_web_sm.load()

# Load data
df = pd.read_excel("New_Orleans_Main.xlsx")

# Define uncertainty indicators
uncertainty_keywords = [
    "i'm not sure", "it seems like", "hopefully", "might", "may", "maybe", "possibly", "perhaps",
    "could", "would", "should", "uncertain", "likely", "unlikely", "not certain", "i think", "i believe",
    "assume", "guess", "sort of", "kind of", "time will tell", "i feel like", "appears", "apparently"
]

# Compile regex
uncertainty_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in uncertainty_keywords) + r')\b', re.IGNORECASE)

# Sentiment scoring
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Count uncertainty keywords
def get_modality_score(text):
    return len(uncertainty_pattern.findall(text))

# Classify sentiment
def classify_sentiment(polarity):
    if polarity > 0.5:
        return "Positive"
    elif 0 < polarity <= 0.5:
        return "Weak Positive"
    elif polarity == 0:
        return "Neutral"
    elif -0.5 <= polarity < 0:
        return "Weak Negative"
    else:
        return "Negative"

# Classify certainty
def classify_interpretation(modality_score):
    if modality_score == 0:
        return "Highly Certain"
    elif modality_score <= 2:
        return "Moderately Certain"
    else:
        return "Uncertain"

# Apply analysis
df["Sentiment Score"] = df["Post Text"].astype(str).apply(get_sentiment)
df["Modality Score"] = df["Post Text"].astype(str).apply(get_modality_score)
df["Uncertain"] = df["Modality Score"].apply(lambda x: 1 if x > 0 else 0)
df["Meaning"] = df["Sentiment Score"].apply(classify_sentiment)
df["Interpretation"] = df["Modality Score"].apply(classify_interpretation)

# Summary
total = len(df)
uncertain = df["Uncertain"].sum()
percent_uncertain = round((uncertain / total) * 100, 2)

print(f"Total rows analyzed: {total}")
print(f"Uncertain rows: {uncertain} ({percent_uncertain}%)")

# Print most neutral
most_neutral_row = df.iloc[(df["Sentiment Score"] - 0).abs().argsort()[:1]]
print("\nMost Neutral Sentiment Text:")
print(most_neutral_row["Post Text"].values[0])

# Print highest modality
highest_modality_row = df.sort_values(by="Modality Score", ascending=False).head(1)
print("\nHighest Modality Score Text:")
print(highest_modality_row["Post Text"].values[0])

# Add summary row at bottom
summary_row = pd.DataFrame([{
    "Post Text": f"Summary: {uncertain} out of {total} posts ({percent_uncertain}%) are uncertain.",
    "Date": "", "City": "", "Conversation Name": "",
    "Sentiment Score": "", "Modality Score": "", "Uncertain": "",
    "Meaning": "", "Interpretation": ""
}])
df = pd.concat([df, summary_row], ignore_index=True)

# ----------------------------------------
#  Monthly Averages Per City
# ----------------------------------------

# Ensure date is datetime
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df_filtered = df.dropna(subset=["Date", "City"]).copy()
df_filtered.loc[:, "Year-Month"] = df_filtered["Date"].dt.to_period("M")

# Group by City and Month, calculate averages
grouped = df_filtered.groupby(["City", "Year-Month"]).agg({
    "Sentiment Score": "mean",
    "Modality Score": "mean",
    "Uncertain": "mean"
}).reset_index()

# Rename columns for clarity
grouped.columns = ["City", "Year-Month", "Avg Sentiment", "Avg Modality", "% Uncertain"]
grouped["Year-Month"] = grouped["Year-Month"].astype(str)
grouped = grouped.sort_values(by=["City", "Year-Month"])

# Pad grouped with spacer columns
spacer_cols = [f"Spacer_{i}" for i in range(3)]
for col in reversed(spacer_cols):
    grouped.insert(0, col, "")

# Pad grouped to match main df length
pad_rows = df.shape[0] - grouped.shape[0]
if pad_rows > 0:
    empty_rows = pd.DataFrame([[""] * grouped.shape[1]] * pad_rows, columns=grouped.columns)
    grouped = pd.concat([grouped, empty_rows], ignore_index=True)

# Combine into one DataFrame (original + summary on right)
combined = pd.concat([df.reset_index(drop=True), grouped.reset_index(drop=True)], axis=1)

# Save final output
output_path = "New_Orleans_Sentiment_FullOutput.xlsx"
combined.to_excel(output_path, index=False)
print(f"\n File saved as: {output_path}")
