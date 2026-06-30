import json
from importlib.resources import files


def load_templates():
    base = files("flumenplot.templates")
    with open(base.joinpath("index.html"), "r", encoding="utf-8") as f:
        index = f.read()
    with open(base.joinpath("sankey.js"), "r", encoding="utf-8") as f:
        sankey_js = f.read()
    with open(base.joinpath("sankey.css"), "r", encoding="utf-8") as f:
        sankey_css = f.read()
    return index, sankey_js, sankey_css


def render_html(data, output, color, list=[]):

    html, sankey_js, sankey_css = load_templates()
    html = html.replace("{{DATA}}", json.dumps(data, indent=2))
    html = html.replace("{{DATA1}}", "")
    html = html.replace("{{CSS}}", sankey_css)
    html = html.replace("{{SANKEYJS}}", sankey_js)
    html = html.replace("{{PATH}}", str(list))
    html = html.replace("{{HIGH_COLOR}}", color)
    html = html.replace("{{CHARTB}}", "")

    # charta = """<div id="chartA"></div>"""
    with open(output, "w") as f:
        f.write(html)

def render_html_multi(data, data1, output, color, list=[]):

    html, sankey_js, sankey_css = load_templates()
    html = html.replace("{{DATA}}", json.dumps(data, indent=2))
    html = html.replace("{{DATA1}}", json.dumps(data1, indent=2))
    html = html.replace("{{CSS}}", sankey_css)
    html = html.replace("{{SANKEYJS}}", sankey_js)
    html = html.replace("{{PATH}}", str(list))
    html = html.replace("{{HIGH_COLOR}}", color)
    html = html.replace("{{CHARTB}}", """"<div id="chartB"></div>""")

    # charta = """<div id="chartA"></div>"""
    with open(output, "w") as f:
        f.write(html)

def dump_dev_data(data_1, data_0_5, data_0_1, output, color, list=[]):
    """Write sample data to templates/dev_data.js for live-server dev workflow."""
    data = {
        "data_1": data_1,
        "data_0_5": data_0_5,
        "data_0_1": data_0_1
    }
    js = f"""\
    const DATA = {json.dumps(data, indent=2)};
    const HIGHLIGHT_PATH  = {json.dumps(list)};
    const HIGHLIGHT_COLOR = "{color}";
    """
    out_path = files("flumenplot.templates").joinpath("dev_data.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"Dev data written to {out_path}")
