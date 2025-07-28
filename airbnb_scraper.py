import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
from datetime import datetime

# Setup Chrome
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = uc.Chrome(options=options)

# Define allowed date range
start_date = datetime(2014, 10, 1)
end_date = datetime(2020, 2, 29)

# URLs
base_url = "https://community.withairbnb.com"
search_base = "https://community.withairbnb.com/t5/forums/searchpage/tab/message?filter=location&q=boston%20str&location=category:homes_en&collapse_discussion=true&page={}" #Change the link before "&"
all_links = set()

# Step 1: Collect post URLs
for page_num in range(1, 200 ):  # Increase page range (feel free to modify)
    driver.get(search_base.format(page_num))
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "lxml")
    links = soup.find_all("a", href=lambda href: href and ("/m-p/" in href or "/t5/" in href))

    for link in links:
        full_url = urljoin(base_url, link['href'].split("?")[0])
        all_links.add(full_url)

print(f" Collected {len(all_links)} unique discussion links")

# Step 2: Extract data
results = []
seen = set()

for i, url in enumerate(all_links, 1):
    print(f"[{i}/{len(all_links)}] Scraping: {url}")
    try:
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "lxml")

        # Get the conversation title
        title_tag = soup.select_one("h2.PageTitle span.lia-link-disabled")
        conversation_name = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Extract post messages and dates
        messages = soup.find_all("div", class_="lia-message-body-content")
        dates = soup.find_all("span", class_="local-date") + soup.find_all("span", attrs={"data-li-local-date": True})
        usernames = soup.find_all("a", class_="lia-user-name-link")

        if not messages or not dates or len(dates) < len(messages):
            print("⚠ Skipping due to missing content or dates")
            continue

        # Clean and parse the main post date
        raw_main_date = dates[0].get_text(strip=True).replace('\u200e', '')
        try:
            main_date_obj = datetime.strptime(raw_main_date, "%d-%m-%Y")
        except ValueError:
            print(f"️ Skipping: couldn't parse main date {raw_main_date}")
            continue

        # Filter by date range
        if not (start_date <= main_date_obj <= end_date):
            continue

        main_post = messages[0].get_text(" ", strip=True)
        if main_post in seen:
            continue
        seen.add(main_post)

        # Add main post row
        results.append({
            "Post Text": main_post.strip(),
            "Date": raw_main_date,
            "City": "Boston",
            "Conversation Name": conversation_name
        })

        # Add replies as individual rows
        for idx in range(1, len(messages)):
            try:
                reply_text = messages[idx].get_text(" ", strip=True)
                raw_reply_date = dates[idx].get_text(strip=True).replace('\u200e', '')
                username = usernames[idx].get_text(strip=True) if idx < len(usernames) else "Unknown"

                reply_entry = f"↳ {username} on {raw_reply_date}:\n{reply_text.strip()}"

                results.append({
                    "Post Text": reply_entry,
                    "Date": raw_reply_date,
                    "City": "",
                    "Conversation Name": ""
                })

            except Exception as e:
                print(f"️ Error processing reply: {str(e)}")
                continue

    except Exception as e:
        print(f" Error scraping {url[:60]}: {str(e)}")

driver.quit()

# Step 3: Save to Excel
df = pd.DataFrame(results)
df.drop_duplicates(subset=["Post Text", "Date"], inplace=True)
print("Available columns:", df.columns.tolist())
print("Sample rows:", df.head())

df = df[["Post Text", "Date", "City", "Conversation Name"]]

df.to_excel("Boston_Homes_STR_Datewise.xlsx", index=False) # For every subsection it needs to be changed Keyword too
print(f"\n Saved {len(df)} rows to 'Boston_Homes_STR_Datewise.xlsx'") # For every subsection it needs to be changed Keyword too


#Analysis







