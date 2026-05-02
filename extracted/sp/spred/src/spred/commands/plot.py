import click
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os


#plt.rcParams['font.family'] =  'Helvetica'
plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['axes.unicode_minus'] = False

def run_plot_volcano(infile, filter_lfc,pval_columns, padjust_columns,
                 lfc_columns, filter_sig_by, outdir,prefix):
    """Generate a volcano plot from differential expression results."""
    
    click.echo(f"⏳ Starting volcano plot generation for: {infile}")

    # Read input file
    try:
        df = pd.read_csv(infile, sep='\t')
    except Exception as e:
        raise click.ClickException(f"❌ Failed to read input file: {e}")
    
    # Use correct column for significance filtering
    sig_col = padjust_columns if filter_sig_by == 'padj' else pval_columns
    
    # Check required columns
    required_cols = [sig_col, lfc_columns]
    for col in required_cols:
        if col not in df.columns:
            raise click.ClickException(f"❌ Column '{col}' not found in input file.")
    
    # Prepare data
    df['-log10Q'] = -np.log10(df[sig_col].replace(0, np.nan))  # avoid log10(0)
    
    # Define DE genes vs. other
    sig_df = df[(df['-log10Q'] > 1.3) & (df[lfc_columns].abs() > filter_lfc)]
    other_df = df.drop(sig_df.index)
    
    # Plot
    fig, ax = plt.subplots(figsize=(7, 6))    
    sns.regplot(x=sig_df[lfc_columns],y=sig_df['-log10Q'], fit_reg=False, scatter_kws={'s':40})
    sns.regplot(x=other_df[lfc_columns], y=other_df['-log10Q'], fit_reg=False, scatter_kws={'s':40})

    ax.set_xlim(-max(2, df[lfc_columns].abs().max() + 1), max(2, df[lfc_columns].abs().max() + 1))
    ax.set_xlabel(r"$\log_2$ Fold Change", fontsize=14)
    ax.set_ylabel(f"$-log_{{10}}$ {filter_sig_by}", fontsize=14)
    ax.tick_params(labelsize=12)
    sns.despine()

    # Output settings
    if prefix == 'none':
        prefix = os.path.splitext(os.path.basename(infile))[0]
    if outdir == 'none':
        outdir = os.path.join(os.path.dirname(infile))
    os.makedirs(outdir, exist_ok=True)

    # Save plots
    pdf_path = os.path.join(outdir, f'{prefix}.volcano.pdf')
    png_path = os.path.join(outdir, f'{prefix}.volcano.png')
    fig.tight_layout()
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    
    click.echo(f"✅ Volcano plot saved to:\n  📄 {pdf_path}\n  🖼️ {png_path}")


def __pre_handle_data(df_in, pval_str='pvalue'):
    df = df_in.copy()
    df['chromsome'] = pd.Categorical(df['chromsome'], categories=categories, ordered=True)
    df.sort_values('chromsome', inplace=True)

    df['pos'] = df.apply(lambda x: int(np.mean([x['start'], x['end']])), axis=1)
    df['log10P'] = -np.log10(df[pval_str].replace(0, np.nan))  # 避免 log(0) 报错
    df['log10P'].fillna(0, inplace=True)
    df['i'] = np.arange(df.shape[0]) + 1
    return df

def __plot_manhan(df_in, pval_str='pvalue', pdjust_str='padj',
                  pad_size=100, figsize=(8, 4), y_cutoff=30, highlight_genes=None,gene_columns='gene_name'):
    plt.figure(figsize=figsize)

    sizes = df_in[pdjust_str].apply(lambda x: 15 if x < 0.05 else 10)

    sns.scatterplot(
        data=df_in, x='i', y='log10P', hue='chromsome',
        palette='dark', size=sizes, sizes=(10, 20),
        alpha=0.4, edgecolor='black', linewidth=0.2,
        legend=None
    )

    # 高亮指定基因
    if highlight_genes:
        highlight_genes = set(highlight_genes)
        df_highlight = df_in[df_in[gene_columns].isin(highlight_genes)]
        if not df_highlight.empty:
            plt.scatter(
                df_highlight['i'], df_highlight['log10P'],
                c='red', s=30, edgecolors='black', linewidths=0.5, zorder=5, label='Highlighted genes'
            )
            # 添加标签
            for _, row in df_highlight.iterrows():
                plt.text(row['i'], row['log10P'] + 0.5, row[gene_columns],
                         fontsize=7, color='black', ha='center', va='bottom', rotation=45)

    chrom_df = df_in.groupby('chromsome')['i'].median()
    plt.xticks(ticks=chrom_df, labels=xlabel_tgt)

    plt.xlabel('Chromosome', fontsize=14, labelpad=10)
    plt.ylabel('-log$_{10}$P', fontsize=14, labelpad=10)

    threshold_y = -np.log10(df_in[df_in[pdjust_str] >= 0.05][pval_str].min())
    plt.axhline(y=threshold_y, color='red', linestyle='--', linewidth=1)

    plt.ylim(0, y_cutoff)
    plt.xlim(df_in['i'].min() - pad_size, df_in['i'].max() + pad_size)
    sns.despine()


import os
import click
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define constants (保持不变)
categories = ['chr1','chr2', 'chr3','chr4','chr5','chr6','chr7','chr8','chr9',
              'chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17',
              'chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM']

xlabel_tgt = ['1','2','3','4','5','6','7','8','9','10',
              '11','12','13','14','15','16','17','18','19','29','21','22','X','Y','M']


def run_plot_manhan(infile, pval_columns, padjust_columns, outdir, prefix, log10_cutoff, highlight_genes,gene_columns):
    """Generate a manhan plot from differential results."""
    click.echo(f"⏳ Starting manhan plot generation for: {infile}")
    
    if highlight_genes:
        # If highlight_genes is a single string with spaces, split it into a list
        if len(highlight_genes) == 1 and ' ' in highlight_genes[0]:
            highlight_genes = highlight_genes[0].split()
        print(f"Highlight genes: {highlight_genes}")

    try:
        df = pd.read_csv(infile, sep='\t')
    except Exception as e:
        raise click.ClickException(f"❌ Failed to read input file: {e}")

    df_plot = __pre_handle_data(df, pval_str=pval_columns)

    # Determine Y-axis cutoff
    if log10_cutoff == "auto":
        log10_cutoff_val = np.ceil(df_plot['log10P'].max()) + 2
        click.echo(f"📐 Auto-set Y-axis max to: {log10_cutoff_val}")
    else:
        try:
            log10_cutoff_val = float(log10_cutoff)
        except ValueError:
            raise click.ClickException("❌ --log10-cutoff must be a number or 'auto'.")

    __plot_manhan(
        df_plot,
        pval_str=pval_columns,
        pdjust_str=padjust_columns,
        figsize=(10, 4),
        y_cutoff=log10_cutoff_val,
        highlight_genes=highlight_genes,
        gene_columns = gene_columns
    )

    prefix = prefix if prefix != 'none' else os.path.splitext(os.path.basename(infile))[0]
    outdir = outdir if outdir != 'none' else os.path.dirname(infile)
    os.makedirs(outdir, exist_ok=True)

    pdf_path = os.path.join(outdir, f'{prefix}.manha.pdf')
    png_path = os.path.join(outdir, f'{prefix}.manha.png')

    plt.savefig(pdf_path, bbox_inches='tight')
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close()

    click.echo(f"✅ manhan plot saved to:\n  📄 {pdf_path}\n🖼️ {png_path}")


@click.command(name = "plot-volcano")
@click.option('-i', '--infile', type=click.Path(exists=True), required=True,
              help='Input differential expression results (TSV format) for volcano plot.')
@click.option('--prefix', default='none',
              help='Prefix for output files. If "none", use input filename.')
@click.option('--outdir', default='none',
              help='Output directory. If "none", use input file directory')
@click.option('--filter-lfc', default=1.0, show_default=True,
              help="Numeric threshold for absolute log2FoldChange to define DE genes.")
@click.option('--pval-columns', default='pvalue',
              help='Column name for raw p-values.')
@click.option('--padjust-columns', default='padj',
              help='Column name for adjusted p-values.')
@click.option('--lfc-columns', default='log2FoldChange',
              help='Column name for log2 fold change values.')
@click.option('--filter-sig-by',
    type=click.Choice(['pvalue', 'padj'], case_sensitive=False),
    default='padj', show_default=True,
    help='Metric used to filter significant genes.')

def plot_volcano(infile, filter_lfc,pval_columns, padjust_columns,
                 lfc_columns, filter_sig_by, outdir,prefix):
    """Volcano plot"""
    run_plot_volcano(infile, filter_lfc,pval_columns, padjust_columns,
                 lfc_columns, filter_sig_by, outdir,prefix)


@click.command(name="plot-manhan")
@click.option('-i', '--infile', type=click.Path(exists=True), required=True,
              help='Input sdGenes or other differential results (TSV format) for manhan plot.')
@click.option('--prefix', default='none',
              help='Prefix for output files. If "none", use input filename.')
@click.option('--outdir', default='none',
              help='Output directory. If "none", use input file directory')
@click.option('--pval-columns', default='pvalue',
              help='Column name for raw p-values.')
@click.option('--padjust-columns', default='padj',
              help='Column name for adjusted p-values.')
@click.option('--log10-cutoff', default='auto', show_default=True,
              help='Maximum value for Y-axis (-log10P) in the plot. Use "auto" to set automatically.')
@click.option('--highlight-genes', '-g', multiple=True, default=None,
              help='List of gene names to highlight in the plot. Can be used multiple times.')
@click.option('--gene-columns', default='gene_name',
              help='Column name for gene symbols in the input file.')
def plot_manhan(infile, pval_columns, padjust_columns, outdir, prefix, log10_cutoff, highlight_genes,gene_columns):
    """Manhattan plot"""
    run_plot_manhan(infile, pval_columns, padjust_columns, outdir, prefix, log10_cutoff, highlight_genes,gene_columns)



