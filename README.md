# Taxa-Viz

Taxa-Viz is a lightweight tool for visualizing **Kraken/MPA taxonomic classification outputs** as an interactive Sankey diagram.

It lets you explore how read abundance flows across taxonomic ranks — and focus on specific taxa of interest.

---

## What It Does

* Parses Kraken / MPA taxonomy reports
* Generates an interactive Sankey diagram
* Preserves abundance proportions
* Supports dynamic filtering
* Allows lineage highlighting from a user-provided list

---

## Interactive Features

### Abundance Filtering

* Set a minimum abundance percentage
* Instantly remove low-abundance taxa from the view

### Rank Filtering

* Filter by specific taxonomic ranks
* Combine rank and abundance filters in any way

### Lineage Highlighting

* Provide a `list.txt` file containing taxa of interest
* Highlight specific lineages in the Sankey plot
* Quickly inspect targeted organisms within the full classification

---

## Why Use It?

Kraken reports are dense and text-heavy.
Taxa-Viz makes them easier to explore visually.

Use it to:

* Identify dominant taxa
* Explore taxonomic structure
* Focus on specific organisms
* Generate clean visual summaries

---

## Installation

Taxa-Viz can be installed directly from GitHub using pip:

```pip install git+https://github.com/karthik30122001/taxa-viz.git```

This will install the latest version of the tool from the main branch.

Requirements
* Python 3.8+
* pip

---

## Usage

Taxa-Viz supports different input formats.
For MetaPhlAn-style `.mpa.txt` reports:

### Basic Usage

```bash
taxa-viz metaphlan input.mpa.txt
```

This generates an interactive Sankey visualization `sankey.html` from the provided report.  
(Optional `-o` flag for custom output filename. Usage `-o filename.html`)

---

### With Lineage Highlighting

To highlight specific taxa using a `list.txt` file:

```bash
taxa-viz metaphlan input.mpa.txt -l list.txt
```

The `list.txt` file should contain one taxon per line.
Matching lineages will be highlighted in the Sankey plot.

---

## Input

* Kraken `.mpa.txt` or compatible taxonomy report
* Optional `list.txt` file for highlighting specific taxa

---

## Output

* Interactive Sankey visualization (HTML)
* Real-time filtering and lineage highlighting

---


