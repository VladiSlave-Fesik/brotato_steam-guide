import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# URLs
URLS = {
    "characters": "https://brotato.wiki.spellsandguns.com/Characters",
    "weapons": "https://brotato.wiki.spellsandguns.com/Weapons",
    "items": "https://brotato.wiki.spellsandguns.com/Items",
}


# Create Selenium driver
def create_driver():
    """ Creates and configures Selenium WebDriver. """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


# Function to parse names from a section
def parse_titles(driver, url):
    """ Extracts names from a section and returns them as a list. """
    print(f"Parsing: {url}")
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    elements = driver.find_elements(By.XPATH, "//table[contains(@class, 'wikitable')]/tbody/tr/td[1]//a")

    names = [f"[h1] {el.text} [/h1]" for el in elements if el.text.strip()]
    return names


# Main function
def main():
    parser = argparse.ArgumentParser(description="Parse Brotato wiki pages and extract names.")
    parser.add_argument("--section", choices=["characters", "weapons", "items", "all"], default="characters",
                        help="Choose section to parse or 'all' for everything (default: all)")

    args = parser.parse_args()

    driver = create_driver()

    results = []

    if args.section == "all":
        for section, url in URLS.items():
            results.extend(parse_titles(driver, url))
    else:
        results.extend(parse_titles(driver, URLS[args.section]))

    driver.quit()

    # Print results
    for line in results:
        print(line)


if __name__ == "__main__":
    main()
