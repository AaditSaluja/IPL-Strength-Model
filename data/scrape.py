# 

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
    "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2022-14452",
    "https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2022-14452",
    "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/indian-premier-league-2023-15129",
    "https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2023-15129"
]

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless=new")  # optional

# 1) Ensure UC downloads a v140-compatible Chrome/driver
driver = uc.Chrome(options=options, version_main=140)  # <-- key line

try:
    for url in urls:
        driver.get(url)

        # (Often there’s a cookie banner that blocks clicks/tables)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept Cookies'], button#onetrust-accept-btn-handler"))
            ).click()
        except Exception:
            pass  # banner not present

        # 2) Wait for the stats table Cricinfo renders (their tables use .ds-table classes)
        tbl = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.ds-table"))
        )

        # 3) Extract headers + rows
        headers = [th.text.strip() for th in tbl.find_elements(By.CSS_SELECTOR, "thead th") if th.text.strip()]
        rows = []
        for tr in tbl.find_elements(By.CSS_SELECTOR, "tbody tr"):
            tds = [td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")]
            if any(tds):
                rows.append(tds)

        # 4) Save CSV
        import csv
        k = url.split("/")
        sv = k[-2].split("-")[0] + "-" + k[-1].split("-")[-2] + ".csv"  
        print(sv)
        with open(sv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if headers:
                w.writerow(headers)
            w.writerows(rows)

        print(f"Wrote {len(rows)} rows to {sv}")

finally:
    driver.quit()
