import os
import click
import pandas as pd
import gseapy as gp
from gseapy import barplot
from statsmodels.stats.multitest import multipletests

def parse_filter_lfc(value):
    try:
        return float(value)
    except ValueError:
        raise click.BadParameter("filter-lfc must be a number or 'none'.")
    
def run_enrich(infile, outdir, protein_coding, multitest, gene_columns,
            padjust_columns, pval_columns, gene_type_columns, filter_sig_by,
            species, prefix,filter_lfc,lfc_columns, gene_sets):
    """Run kogo enrichment for target genes."""

    # 1. Load input
    click.echo(f"⏳ Starting analysis {infile} ...")
    try:
        df = pd.read_csv(infile, sep='\t')
    except Exception as e:
        raise click.ClickException(f"Failed to read input file: {e}")
    
    click.echo(f"⏳ Running pro-processing input data, {df.shape[0]} genes for further analysis")
    
    # 2. Filter for protein-coding genes
    if protein_coding:
        if gene_type_columns in df.columns:
            df = df[df[gene_type_columns].str.contains('protein_coding')]
        else:
            raise click.ClickException(f"'{gene_type_columns}' column not found in input file.")

    # 3. Apply multiple testing correction
    if multitest != 'none':
        try:
            df[padjust_columns] = multipletests(df[pval_columns], method=multitest)[1]
        except Exception as e:
            raise click.ClickException(f"Failed to adjust p-values: {e}")

    # 4. Select significant genes
    try:
        df_sig = df.copy()
        if filter_lfc != 'none':
            try:
                filter_lfc_val = float(filter_lfc)
                if lfc_columns in df.columns:
                    df_sig = df_sig[abs(df_sig[lfc_columns]) > filter_lfc_val]
                else:
                    click.secho(f"Warning: '{lfc_columns}' column not found in input file, skip this filter", fg='yellow')
            except ValueError:
                raise click.ClickException(f"Invalid value for --filter-lfc: {filter_lfc}. It must be a number or 'none'.")
        
        if filter_sig_by == 'pvalue':
            filter_sig_by = pval_columns
        elif filter_sig_by == 'padj':
            filter_sig_by = padjust_columns
        sig_genes = df_sig[df_sig[filter_sig_by] < 0.05][gene_columns].dropna().unique().tolist()
        if not sig_genes:
            raise click.ClickException("No significant genes found after filtering.")
    except Exception as e:
        raise click.ClickException(f"Error during filtering: {e}")
    
    click.echo(f"⏳ Pro-processing Completed, {len(sig_genes)} out of {df.shape[0]} genes for enrichment!")
    # Output
    
    if prefix == 'none':
        prefix = os.path.basename(infile).replace('.tsv','').replace('.txt','')
    if outdir == 'none':
        outdir = os.path.dirname(infile) + '/kogo'
        
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    
    table_file = os.path.join(outdir, f'{prefix}.for_kogo.table.tsv')
    gene_file = os.path.join(outdir, f'{prefix}.for_kogo.genelist.tsv')
    
    df.to_csv(table_file,sep='\t',index=False)
    pd.DataFrame(sig_genes).to_csv(gene_file,sep='\t',index=False,header=None)
    click.echo(f"📁 Pro-processed differential tables saved to: {table_file}")
    click.echo(f"📁 Gene list for enrichment saved to: {gene_file}")
    
    click.echo("⏳ Running enrichment ...")
    enr = gp.enrichr(gene_list=sig_genes,
                     gene_sets=list(gene_sets),
                     organism=species,
                     outdir=None)
    click.echo("✅ Enrichment completed")    

    res_file = os.path.join(outdir, f'{prefix}.kogo.results.tsv')
    fig_pdf = os.path.join(outdir, f'{prefix}.kogo.barplot.pdf')
    fig_png = os.path.join(outdir, f'{prefix}.kogo.barplot.png')

    enr.results.to_csv(res_file, sep='\t', index=False)
    
    click.echo(f"📁 Enrich Results saved to: {res_file}")

    ax = barplot(enr.results,
                 column="P-value",
                 group='Gene_set',
                 size=10,
                 top_term=10,
                 cutoff=1,
                 figsize=(3, 7),
                 color={'KEGG_2021_Human': 'salmon',
                        'GO_Biological_Process_2021': 'darkblue'})

    ax.figure.savefig(fig_pdf, bbox_inches='tight')
    ax.figure.savefig(fig_png, bbox_inches='tight', dpi=300)

    click.echo(f"📁 Enrich Plots saved to: {fig_pdf}, {fig_png}")


@click.command()
@click.option('-i', '--infile', type=click.Path(exists=True), required=True,
              help='Input summary table for filtering and KOGO.')
@click.option('--multitest',
    type=click.Choice(['none', 'b', 'hs', 'fdr_by', 'fdr_bh'], case_sensitive=False),
    default='none',
    show_default=True,
    help='Multiple testing correction method.')
@click.option('--protein-coding', is_flag=True,
              help='Filter results to protein-coding genes only.')
@click.option('--filter-sig-by',
    type=click.Choice(['pvalue', 'padj'], case_sensitive=False),
    default='padj',
    show_default=True,
    help='Metric to filter significant genes.')
@click.option('--filter-lfc', default=1, callback=lambda ctx, param, value: parse_filter_lfc(value),
              help="Numeric threshold for log2FoldChange, or 'none' to disable.")
@click.option('--gene-columns', default='gene_name',
              help='Column name for gene symbols in the input file.')
@click.option('--pval-columns', default='pvalue',
              help='Column name for raw p-values.')
@click.option('--padjust-columns', default='padj',
              help='Column name for adjusted p-values.')
@click.option('--gene-type-columns', default='gene_type',
              help='Column name for gene type info.')
@click.option('--lfc-columns', default='log2FoldChange',
              help='log2FoldChange name for gene type info.')

@click.option('-o', '--outdir', default='none',
              help='Output directory.')
@click.option(
    '--gene-sets',
    multiple=True,
    default=('KEGG_2021_Human', 'GO_Biological_Process_2021'),
    show_default=True,
    help="Gene sets to use in enrichment (can specify multiple, e.g., --gene-sets KEGG_2021_Human GO_Biological_Process_2021)"
)

@click.option('--species',
    type=click.Choice(['mouse', 'human'], case_sensitive=False),
    default='human',
    show_default=True,
    help='Species for enrichment.')
@click.option('--prefix', default='none',
              help='Prefix name for output files.')

def enrich(infile, outdir, protein_coding, multitest, gene_columns,
            padjust_columns, pval_columns, gene_type_columns, filter_sig_by,
            species, prefix,filter_lfc,lfc_columns, gene_sets):
    """Functional enrichment for genes"""
    run_enrich(infile, outdir, protein_coding, multitest, gene_columns,
            padjust_columns, pval_columns, gene_type_columns, filter_sig_by,
            species, prefix,filter_lfc,lfc_columns, gene_sets)

