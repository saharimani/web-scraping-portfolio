# StackExchange Politics: scraping and engagement analysis

A Scrapy spider that crawls every question in the Politics Stack Exchange forum. The scraped data is then analysed to see which topics dominate and how user activity relates to reputation.

## Data collection

The spider ran against an **offline Kiwix archive of politics.stackexchange.com (November 2023)**, served locally at `127.0.0.1:8080`. That gave a complete, stable copy of the forum without putting load on the live site.

For each question the spider:
1. reads the listing page and follows the **next page** link until the end;
2. takes the title, excerpt, tags, votes, answer count, time asked, and the asker's name, reputation and badges from the question's summary;
3. follows the link to the question page to **count its comments**, carrying the summary forward in `response.meta`.

Fields are defined in `items.py` and collected with an `ItemLoader`.

## Layout

```
stackexchange-politics-scrapy/
├── scrapy.cfg
├── StackExPolitics/
│   ├── items.py              fields scraped per question
│   ├── settings.py           robots.txt obeyed, UTF-8 feed export
│   ├── pipelines.py, middlewares.py   Scrapy defaults
│   └── spiders/StackExPoliticsSpider.py
└── politics_analysis.ipynb   cleaning, EDA and regression
```

Run it, with the archive served locally:

```bash
pip install scrapy
cd stackexchange-politics-scrapy
scrapy crawl StackExPoliticsSpider -O stackexpoliticdata.csv
```

## Analysis (notebook)

- **Cleaning:** parsing the "asked" timestamps, splitting the tag lists, converting reputation strings to numbers.
- **Tags:** the most frequent tags (US politics dominates), and tag trends over time.
- **Users:** the most active users and their questions, answers and comments.
- **Regression:** OLS of user reputation on the number of questions, answers and comments posted.
  - R² = 0.34 across 747 users.
  - Activity explains about a third of the variation in reputation.

## Known issues

- **Fields are saved as lists.** The `ItemLoader` has no output processors, so every field is written as a list (`[86]` rather than `86`). The notebook strips these during cleaning. The cleaner fix is `default_output_processor = TakeFirst()` on an item loader subclass, with `MapCompose(str.strip)` for text.
- **Reputation is a snapshot at crawl time.** It sums a user's activity across the whole forum, not just the questions scraped here. So the regression describes association, not what earns reputation.
- **The published files were originally flat.** They have now been arranged as a standard Scrapy project, so `scrapy crawl` works from this folder.
