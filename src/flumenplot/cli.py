import argparse
import sys

from flumenplot.kraken2sankey import kraken2sankey
from flumenplot.mpa2sankey import mpa_to_sankey
from flumenplot.generate_report import dump_dev_data, render_html, render_html_multi
from flumenplot.order import  order_alpabetically
# from taxa_viz.kraken_to_sankey import kraken_to_sankey


def load_highlights(args):
    if args.highlight_list:
        with open(args.highlight_list) as fh:
            return [
                line.strip()
                for line in fh
                if line.strip()
            ]
    else:
        return []


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="FlumenPlot",
        description="Generate interactive Sankey plots from taxonomic classifier outputs",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Input format",
    )

    # ---- Kraken subcommand ----
    kraken = subparsers.add_parser(
        "kraken",
        help="Convert Kraken report to Sankey",
    )
    kraken.add_argument(
        "input",
        help="Kraken report file",
    )
    kraken.add_argument(
        "-o",
        "--output",
        default="sankey.html",
        help="Output HTML file (default: sankey.html)",
    )
    kraken.add_argument(
        "-l",
        "--highlight-list",
        metavar="FILE",
        help="File containing taxa to highlight (one per line)",
    )
    kraken.add_argument(
        "--highlight-color",
        help="Custom color to highlight taxa with",
    )
    #
    # ---- MetaPhlAn subcommand ----
    metaphlan = subparsers.add_parser(
        "metaphlan",
        help="Convert MPA style report to Sankey",
    )
    metaphlan.add_argument(
        "input",
        nargs="2",
        help="MetaPhlAn output file",
    )
    metaphlan.add_argument(
        "-o",
        "--output",
        default="sankey.html",
        help="Output HTML file (default: sankey.html)",
    )
    metaphlan.add_argument(
        "-l",
        "--highlight-list",
        metavar="FILE",
        help="File containing taxa to highlight (one per line)",
    )
    metaphlan.add_argument(
        "-c",
        "--consensus",
        action="store_true",
        default=False,
        help="Consensus plot for multi-sample files",
    )
    metaphlan.add_argument(
        "-b",
        "--comparative",
        action="store_true",
        default=False,
        help="Side by side comparision for two files",
    )
    metaphlan.add_argument(
        "--highlight-color",
        help="Custom color to highlight taxa with",
    )
    metaphlan.add_argument(
        "--debug",
        help="Debug",
    )
    args = parser.parse_args()

    try:
        if args.command == "kraken":
            data_1 = kraken2sankey(args.input, abundance=4.9,)
            data_0_5 = kraken2sankey(args.input, abundance=0.9,)
            data_0_1 = kraken2sankey(args.input, abundance=0.49,)
        #

        if args.command == "metaphlan" and args.comparative:
            datasets =[]
            for file in args.input:
                data_1 = mpa_to_sankey(file, min_percent=4.9, consensus=args.consensus)
                data_0_5 = mpa_to_sankey(file, min_percent=0.9, consensus=args.consensus)
                data_0_1 = mpa_to_sankey(file, min_percent=0.49, consensus=args.consensus)
                data_list = [data_1, data_0_5, data_0_1]
                for data in data_list:
                    data["nodes"] = order_alpabetically(data)

                data = {
                        "data_1": data_1,
                        "data_0_5": data_0_5,
                        "data_0_1": data_0_1
                        }

                datasets.append(data)
            
            list = load_highlights(args)
            if args.highlight_color:
                render_html_multi(datasets[0], datasets[1], args.output, color=args.highlight_color, list=list)
            else:
                render_html_multi(datasets[0], datasets[1], args.output, color="#f5e042", list=list)
            sys.exit()

        if args.command == "metaphlan":
            data_1 = mpa_to_sankey(args.input, min_percent=4.9, consensus=args.consensus)
            data_0_5 = mpa_to_sankey(args.input, min_percent=0.9, consensus=args.consensus)
            data_0_1 = mpa_to_sankey(args.input, min_percent=0.49, consensus=args.consensus)

        # else:
        #     parser.error("Unknown command")
        
        # print(get_children(data_1["nodes"][0], data_1["nodes"], data_1["links"]))

        # Render HTML (centralised here or in a helper)

        data_list = [data_1, data_0_5, data_0_1]
        for data in data_list:
            data["nodes"] = order_alpabetically(data)

        data = {
                "data_1": data_1,
                "data_0_5": data_0_5,
                "data_0_1": data_0_1
                }
        list = load_highlights(args)
        if args.highlight_color:
            render_html(data, args.output, color=args.highlight_color, list=list)
        else:
            render_html(data, args.output, color="#f5e042", list=list)
            # dump_dev_data(data_1, data_0_5, data_0_1, args.output, color="#f5e042", list=list)

    # except FileFormatError as e:
    #     print(f"File format error: {e}", file=sys.stderr)
    #     sys.exit(2)
    #
    # except ValidationError as e:
    #     print(f"Validation error: {e}", file=sys.stderr)
    #     sys.exit(3)

    except Exception as e:
        # Truly unexpected error
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(99)


if __name__ == "__main__":
    main()
