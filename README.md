# FlumenPlot
FlumenPlot is a lightweight tool for visualizing **Kraken/MPA taxonomic classification outputs** as an interactive Sankey diagram.
It lets you explore how read abundance flows across taxonomic ranks and focus on specific taxa of interest.

---

## What It Does
* Parses Kraken / MPA taxonomy reports
* Generates an interactive Sankey diagram
* Preserves abundance proportions
* Supports dynamic filtering
* Allows lineage highlighting from a user-provided list
* Interactive lineage tracing directly from the diagram

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

### Click-to-Highlight
* Click any node in the Sankey diagram to instantly highlight its full lineage
* Traces the path from the selected taxon back to the root

### Copy Lineage
* Right-click any node to copy its full lineage path to your clipboard
* Copied output is formatted to be directly compatible with `list.txt`
* Paste it straight into a list file for persistent or batch highlighting

---

## Why Use It?
Kraken reports are dense and text-heavy.
FlumenPlot makes them easier to explore visually.
Use it to:
* Identify dominant taxa
* Explore taxonomic structure
* Focus on specific organisms
* Interactively trace and export lineages of interest
* Generate clean visual summaries

---

## Installation
FlumenPlot can be installed directly from GitHub using pip:
```
pip install git+https://github.com/karthik30122001/FlumenPlot.git
```
This will install the latest version of the tool from the main branch.

**Requirements**
* Python 3.12+
* pip

---

## Usage
FlumenPlot supports different input formats.
For MetaPhlAn-style `.mpa.txt` reports:

### Basic Usage
```bash
flumenplot metaphlan input.mpa.txt
```
This generates an interactive Sankey visualization `sankey.html` from the provided report.  
(Optional `-o` flag for custom output filename. Usage: `-o filename.html`)

---

### With Lineage Highlighting
To highlight specific taxa using a `list.txt` file:
```bash
flumenplot metaphlan input.mpa.txt -l list.txt
```
The `list.txt` file should contain one taxon per line.
Matching lineages will be highlighted in the Sankey plot.

---

## Input
* Kraken `.txt` or
* Metaphlan `.mpa.txt`
* Optional `list.txt` file for highlighting specific taxa

---

## Output
* Interactive Sankey visualization (HTML)
* Real-time filtering and lineage highlighting
* Click-to-highlight lineage tracing
* Right-click to copy lineage — ready for use as a `list.txt` input
