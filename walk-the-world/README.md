# Walk the World: shortest land route between two cities

Given two city names, the program works out whether you could walk between them without crossing an ocean. If you can, it finds the route with the **fewest border crossings** and reports facts about each country on the way. All the data comes from Wikipedia at run time.

## How it works

1. **Validate the input:** check that both cities have a Wikipedia page (`requests` + `BeautifulSoup`).
2. **Find the countries:** read each city's country from its infobox using CSS selectors and XPath.
3. **Same country?** If both cities are in the same country, stop there.
4. **Ocean check:** map each country to its continent, then use a lookup of which continent pairs are separated by an ocean. For example, Tehran → Los Angeles reports the Pacific.
5. **Build the border graph:** scrape *List of countries and territories by number of land borders* into an adjacency list (country → neighbours).
6. **Shortest route:** run breadth-first search (`collections.deque`) on the graph. BFS gives the path with the fewest edges, which here means the fewest border crossings.
7. **Country facts:** scrape area, population and GDP for each country on the route, and report the largest, the most populous and the richest.

Example output for **Tehran → Paris**:

```
Iran -> Azerbaijan -> Russia -> Poland -> Germany -> France
```

## Layout

```
walk-the-world/
├── walk_the_world.ipynb  code, explanations and example runs
└── README.md
```

## Known issues

These are problems I found when reviewing the work later. The notebook is left exactly as it was run.

**1. Exclaves make the route impossible on foot.** The graph treats each country as a single node. Russia borders Poland only through **Kaliningrad**, which isn't connected to the rest of Russia. So Russia → Poland is not a walkable step, and the route above would really need to pass through Belarus or Lithuania. The fix is to model exclaves as separate nodes, with Kaliningrad linked only to Poland and Lithuania. Non-contiguous territories such as Alaska and French Guiana have the same problem.

**2. One population value is parsed incorrectly.** In the example output Russia's population is shown as `(`. The XPath picks up the first text node of the infobox row, and for Russia that node is a bracket. Joining all the text nodes and taking the first number fixes it.

**3. The ocean check is approximate.** It works at continent level with a hand-written lookup, so it doesn't handle land bridges or islands well. Cases like Panama, Egypt–Asia or Ireland can come out wrong. Checking whether a path exists in the border graph, instead of using continent rules, would answer "walkable?" directly.
