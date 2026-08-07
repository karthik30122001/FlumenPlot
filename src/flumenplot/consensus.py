import pandas as pd
from skbio.stats import subsample_counts

# df = pd.read_csv("LR_combined.mpa.txt", delimiter="\t")
# print(df.head())
# print(df.iloc[:, 1:].sum().min())
# low = df.iloc[:, 1:].sum().min()


def kraken_consensus(dataframe):
    samples = []
    low = dataframe.iloc[:, 1:].sum().min()
    for col in dataframe.iloc[:, 1:].columns:
        sample = pd.Series(subsample_counts(dataframe[col], low, seed=6969))
        samples.append(sample)
    subsampled_df = pd.concat([dataframe.iloc[:, 0], *samples], axis=1)
    subsampled_df = dataframe.copy()
    subsampled_df.rename(columns={subsampled_df.columns[0]: 'taxon'}, inplace=True)
    # print(subsampled_df.sort_values(1, ascending=False).head())

    subsampled_df['reads_consensus'] = subsampled_df.iloc[:, 1:].mean(axis=1).round().astype(int)

    kingdom_only = subsampled_df[
            subsampled_df.iloc[:, 0].str.count(r"\|") == 0
    ]
    total_reads = kingdom_only['reads_consensus'].sum()

    subsampled_df['relative_abundance'] = (subsampled_df['reads_consensus'] / total_reads * 100).round(3)

    # print(subsampled_df.sort_values('relative_abundance', ascending=False).head())
 
    return (
            subsampled_df[['taxon', 'reads_consensus', 'relative_abundance']]
            )

    # subsampled_df[['taxon', 'reads_consensus', 'relative_abundance']].to_csv("LR_consensus.mpa.txt", sep="\t", header=True)

# mpa_consensus(df)



def mpa_consensus(dataframe):
    consensus_df = dataframe.copy()
    consensus_df.rename(columns={consensus_df.columns[0]: 'taxon'}, inplace=True)

    consensus_df['reads_consensus'] = consensus_df.iloc[:, 1:].mean(axis=1).round(8).astype(float)

    kingdom_only = consensus_df[
            consensus_df.iloc[:, 0].str.count(r"\|") == 0
    ]
    total_reads = kingdom_only['reads_consensus'].sum()

    consensus_df['relative_abundance'] = (consensus_df['reads_consensus'] / total_reads * 100).round(8)

    # print(consensus_df.sort_values('relative_abundance', ascending=False).head())
 
    return (
            consensus_df[['taxon', 'reads_consensus', 'relative_abundance']]
            )

    # subsampled_df[['taxon', 'reads_consensus', 'relative_abundance']].to_csv("LR_consensus.mpa.txt", sep="\t", header=True)

# mpa_consensus(df)
