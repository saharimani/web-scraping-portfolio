# Web Scraping Portfolio

Three data-collection projects from my BSc Economics & Data Science at Royal Holloway (2023–24, Web Scraping module). Each one scrapes data that isn't available as a clean download, turns it into a dataset, and then analyses it.

| Project | What it collects | Techniques | Analysis |
|---|---|---|---|
| [**StackExchange Politics**](stackexchange-politics-scrapy) | Questions, tags, votes, answers, comments and user reputation from a full Stack Exchange forum | `Scrapy` spider with pagination, item loaders, request chaining (listing page → question page) | Tag frequencies, user engagement, OLS of reputation on activity |
| [**Economic data from Wikipedia**](wikipedia-country-economics) | Area, population, GDP, GDP per capita, Gini and HDI for ~200 sovereign states | `requests` + `lxml` with XPath on infoboxes | Cleaning, log transforms, correlations, OLS |
| [**Walk the World**](walk-the-world) | Which country a city is in, continents, land borders, country statistics | `BeautifulSoup`, `lxml`, XPath and CSS selectors | Builds a land-border graph and finds the route with the fewest border crossings using breadth-first search |

**Skills shown:** HTTP scraping, XPath and CSS selectors, Scrapy project structure, crawling many pages, turning messy HTML into tables, pandas cleaning, statsmodels regression, graph search.

## Scraping responsibly

- **The StackExchange spider ran against an offline copy of the forum** (a Kiwix archive served on `127.0.0.1`), not the live site. It also obeys `robots.txt`.
- **The Wikipedia projects send one request per page**, run sequentially.

## Looking back

Each project README ends with a short **"Known issues"** section. These are problems I found when reviewing the work later: a number-cleaning bug, an exclave that breaks a "shortest route", and fields saved as lists. I've left the original notebooks as they were run. I can't regenerate them, because the scraped datasets weren't kept and the source pages have changed since. Instead, each issue is explained next to the fix I'd make.
