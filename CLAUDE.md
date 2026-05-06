# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Exploratory data analysis of the [Open Food Facts](https://world.openfoodfacts.org/) dataset (German-language academic project). The dataset (`en.openfoodfacts.org.products.csv`) is a large tab-separated file (~several GB, >180 columns) that is gitignored and must be obtained separately.

## Running the Notebook

```bash
jupyter notebook test.ipynb
# or
jupyter lab test.ipynb
```

Run all cells top-to-bottom. The notebook expects the CSV to be present in the project root as `en.openfoodfacts.org.products.csv`. It loads only a curated subset of ~22 columns for performance.

## Architecture

The entire analysis lives in `test.ipynb` as a single linear script (no imports from other modules). Each numbered section is self-contained:

1. **CSV loading** — reads only the columns listed in `COLS` using `usecols` for memory efficiency
2. **Basic info** — dtypes and describe
3. **Missing values** → `missing_values.png`
4. **Nutri-Score distribution** → `nutriscore_distribution.png`
5. **NOVA group** (processing level) → `nova_distribution.png`
6. **Top 20 countries** → `top_countries.png`
7. **Nutrient boxplots** (per 100g, clipped at 99th percentile) → `nutrients_boxplot.png`
8. **Yearly entries** (2012–2025) → `yearly_entries.png`
9. **Completeness histogram** → `completeness.png`
10. **Summary printout** for Milestone 1

All output PNGs are committed to the repository; the source CSV is not.

## Key Data Notes

- Separator is `\t` (tab), not comma
- `nova_group` and `nutriscore_grade` are the two primary quality/classification columns
- Nutrient columns follow the pattern `<nutrient>_100g` (values per 100g)
- `created_datetime` / `last_modified_datetime` are ISO strings; parse with `pd.to_datetime(..., errors="coerce")`
- `countries_en` is a comma-separated multi-value string; explode before aggregating
