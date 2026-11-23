"""Scrape country-level economic indicators from Wikipedia infoboxes.

Collects area, water share, population, GDP, GDP per capita, Gini and HDI
for every sovereign state and writes them to countries_data.csv.
The analysis of the resulting CSV is in country_economics_analysis.ipynb.

Usage:
    python scraper.py
"""
import csv

import requests
from lxml import html


def get_country_urls():
    url ="https://en.wikipedia.org/wiki/List_of_sovereign_states"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    country_links = tree.xpath('//table[contains(@class,"wikitable")]/tbody/tr/td[1]//a/@href')

    base_url ="https://en.wikipedia.org"
    return [base_url + link for link in country_links if link.startswith("/wiki")]


def get_country_info(country_url):
    response =requests.get(country_url)
    tree =html.fromstring(response.content)

    def extract_first_or_none(xpath_query):
        results = tree.xpath(xpath_query)
        return ' '.join(results[0].strip().split()) if results else "Not available"

    #Xpaths
    country_name_xpath= "//div[@class='fn org country-name']/text()"
    country_name = extract_first_or_none(country_name_xpath)

    # XPath for area in square kilometers (without square miles)
    area_xpath = "//th[contains(.,'Total')]/following-sibling::td//text()"
    area = extract_first_or_none(area_xpath)
    area = area.split('(')[-1].split()[0]

    population_xpath = "//th[contains(.,'Population')]/../following-sibling::tr[1]//td/text()"
    population = extract_first_or_none(population_xpath)

    gdp_xpath ="//th[contains(.,'Total') and following-sibling::td[contains(text(),'$')]]/following-sibling::td/text()"
    gdp = extract_first_or_none(gdp_xpath)

    water_area_xpath = "//th[contains(.,'Water')]/following-sibling::td/text()"
    water_area = extract_first_or_none(water_area_xpath)

    gdp_per_capita_xpath = "//th[contains(.,'Per capita')]/following-sibling::td/text()"
    gdp_per_capita = extract_first_or_none(gdp_per_capita_xpath)

    gini_index_xpath = "//th[contains(.,'Gini')]/following-sibling::td/text()"
    gini_index = extract_first_or_none(gini_index_xpath)

    hdi_index_xpath = "//th[contains(.,'HDI')]/following-sibling::td/text()"
    hdi_index = extract_first_or_none(hdi_index_xpath)

    return {'Country':country_name,
            'Area (km)':area,
            'Water Area(%)':water_area,
            'Population':population,
            'GDP Total(trillion)':gdp,
            'GDP Per Capita($)':gdp_per_capita,
            'Gini Index':gini_index,
            'HDI Index':hdi_index}


def main():
    #Geting URLs of all countries
    country_urls = get_country_urls()

    #Scraping information for each country
    all_country_data = []
    for url in country_urls:
        country_data = get_country_info(url)
        all_country_data.append(country_data)

    #Writing data to CSV
    keys=['Country',
          'Area (km)',
          'Water Area(%)',
          'Population',
          'GDP Total(trillion)',
          'GDP Per Capita($)',
          'Gini Index',
          'HDI Index']
    with open('countries_data.csv','w',newline='',encoding='utf-8') as output_file:
        dict_writer =csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_country_data)


if __name__ == "__main__":
    main()
