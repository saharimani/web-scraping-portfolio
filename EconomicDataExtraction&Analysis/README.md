# Economic data from Wikipedia: scraping and analysis

A scraper that builds a country-level dataset from Wikipedia: area, water share, population, GDP, GDP per capita, Gini and HDI for every sovereign state. The data is then cleaned and analysed with descriptive statistics, correlations and OLS.

## Data collection

- The scraper reads the links to all ~205 country pages from Wikipedia's *List of sovereign states*.
- From each country's infobox it extracts eight fields with **XPath**. For example, `//th[contains(.,'Gini')]/following-sibling::td/text()`.
- Missing fields are recorded as `"Not available"`, and the results are written to `countries_data.csv`.
- Requests are sent one at a time, using `requests` and `lxml`.

## Analysis (notebook)

1. **Cleaning:** "Not available" becomes NaN, "negligible" water area becomes 0, GDP strings are converted to trillions, and numbers are pulled out of text.
2. **Distributions:** summary statistics, plus log transforms of area, population and GDP, which are heavily skewed.
3. **Correlations:** scatter plots with trend lines (GDP vs HDI, GDP per capita vs Gini, population vs area).
4. **OLS:** log GDP per capita regressed on log population, HDI and Gini. n = 169, R² = 0.91. HDI is the only significant term.

## Known issues

These are problems I found when reviewing the work later. The notebook is left exactly as it was run.

**1. The number-cleaning step mixes in footnote and year digits.** `extract_numeric` keeps *every* digit in a cell, so footnote and year digits get appended to the real figure. For example, `"1.24 (2015)"` becomes `1.242015`, and a population with a citation marker gains extra digits. That is why the summary table shows impossible values:
- a maximum population of 1.04 × 10¹²;
- a GDP per capita of $1.16 bn;
- a water share of 24,069%.

The fix is to remove the citation brackets and keep only the first number:

```python
import re

def extract_numeric(value):
    if not isinstance(value, str):
        return value
    value = re.sub(r"\[[^\]]*\]", "", value)            # drop [12]-style citations
    match = re.search(r"\d[\d,]*\.?\d*", value)           # first number only
    return float(match.group().replace(",", "")) if match else float("nan")
```

A validity check would also have caught it, e.g. `assert df["Water Area(%)"].le(100).all()`.

**2. The regression is partly circular.** HDI is built partly from income per head (GNI per capita), so using it to "predict" GDP per capita produces a high R² largely by construction. A fairer specification would use HDI's non-income parts (education and life expectancy), or drop HDI and report the population and Gini effects on their own.

**3. Wikipedia changes over time.** The infobox layout and values differ between scrape dates, and the original CSV wasn't kept. That means the numbers above can't be reproduced exactly. Saving the raw HTML or the scraped CSV with a date would fix this.
