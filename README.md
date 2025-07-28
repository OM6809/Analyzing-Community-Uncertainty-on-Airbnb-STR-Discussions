# Analyzing-Community-Uncertainty-on-Airbnb-STR-Discussions
This project investigates community uncertainty and sentiment surrounding Airbnb’s Short-Term Rental (STR) policies by scraping and analyzing posts from the Airbnb Community Center.

📌 Summary
The goal was to extract city-specific discussions, detect uncertainty using NLP techniques, and visualize patterns over time. The project was conducted during my Summer Research Assistantship and focuses on four major U.S. cities: Boston, New Orleans, Los Angeles, and Chicago.

🧩 Problem Statement
Airbnb’s rapid growth has triggered policy debates and confusion in many cities. Hosts and community members express concerns, ask questions, and discuss regulations on Airbnb forums. However, this feedback is unstructured and spread across hundreds of pages.

Research Questions:

How uncertain are hosts and users regarding STR policies in their cities?

What emotional tones accompany these discussions?

Do uncertainty and sentiment patterns vary by city and over time?

🌐 Data Source
Platform: Airbnb Community Center

Targeted Categories: Manage Listing, Welcome Guests, Community Café, etc.

Keywords: "STR", "regulations", "law" + city names

Time Range Filtered: October 2014 to February 2020

🧪 Tools & Technologies
Python for data extraction & analysis

undetected_chromedriver + BeautifulSoup for scraping dynamic JavaScript-rendered pages

pandas, re, and datetime for cleaning and preprocessing

spaCy and TextBlob for:

Sentiment Analysis

Uncertainty/Modality Detection

Gensim + LDA (Latent Dirichlet Allocation) for Topic Modeling

Matplotlib and Seaborn for visualizations

Excel / Jupyter Notebooks for structured output and reporting

📈 Challenges Encountered
Problem	Solution
Dynamic page loading	Used undetected_chromedriver with simulated scroll and delay
Missing or corrupted dates	Cleaned with .replace('\u200e', ''), try/except blocks, and fallback formats
Duplicate content	Used set() for uniqueness on post content
Mismatched user-reply-date relationships	Mapped messages with proper index handling
Ambiguity in language	Handled using regex-based modality detection + sentiment scoring

🔍 NLP Analysis Conducted
Uncertainty Detection

Used a dictionary of ~25 uncertainty phrases (e.g., "might", "I'm not sure", "hopefully")

Regex-based scoring to calculate Modality Score

Classified posts as:

Highly Certain

Moderately Certain

Uncertain

Sentiment Analysis

Used TextBlob to extract polarity (-1 to +1)

Categorized into:

Negative, Weak Negative, Neutral, Weak Positive, Positive

Topic Modeling

Applied LDA to detect major discussion topics per city

Revealed dominant concerns like zoning, licenses, neighbor complaints, etc.

📊 Key Insights
City	Posts Analyzed	% Uncertain
Los Angeles	168	50.6%
Chicago	234	50.85%
Boston	334	34.13%
New Orleans	103	34.95%

Community members often expressed neutral or weakly negative sentiment alongside uncertainty.

Spikes in uncertainty aligned with policy announcements or zoning changes.

"I’m not sure", "Hopefully", and "I think Airbnb might…" were among the most common hedging phrases.
