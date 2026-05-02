import click
import pandas as pd
import os
from ..tools.iso_gene_differential import cal_diff,filter_by_express
from ..tools.splicing_genes import cal_sdgene
from ..tools.downloader import get_annotation_file


def run_analyze(matrix, metadata, group, case, control, covariates, outdir, protein_coding,species,reference_source):
    """Run differential analysis based on gene-level, isoform-level and sdGene indentification"""
    try:
        df_mtx = pd.read_csv(matrix, index_col=0, sep=None, engine='python')
        click.echo(f"✅ Reading matrix completed. There are {df_mtx.shape[0]} isoforms and  {df_mtx.shape[1]} samples ")
    except Exception as e:
        raise ValueError(f"Failed to read matrix file: {e}")

    try:
        df_meta = pd.read_csv(metadata, index_col=0, sep=None, engine='python')
        click.echo(f"✅ Reading metadata completed. There are {df_meta.shape[0]} samples and  {df_mtx.shape[1]} columns ")
    except Exception as e:
        raise ValueError(f"Failed to read metadata file: {e}")

    # Sample alignment check
    common_samples = df_mtx.columns.intersection(df_meta.index)
    if len(common_samples) == 0:
        raise ValueError("No matching sample names between matrix and metadata.")
    df_mtx = df_mtx[common_samples]
    df_meta = df_meta.loc[common_samples]
    
    click.echo(f"✅ Reading and checking samples completed. There are {len(common_samples)} common samples")    

    #Optional strict validation
    if group not in df_meta.columns:
        raise ValueError(f"Group column '{group}' not found.")
    if case not in df_meta[group].unique() or control not in df_meta[group].unique():
        raise ValueError(f"'{case}' or '{control}' not found in group column.")
    for cov in covariates:
        if cov not in df_meta.columns:
            raise ValueError(f"Covariate '{cov}' not found in metadata.")
    if not pd.api.types.is_numeric_dtype(df_mtx.values):
        raise ValueError("Matrix values must be numeric.")
    

    os.makedirs(f'{outdir}/results/tables', exist_ok=True)
    # Get annotation file from data folder (or download if missing)
    # Load annotation
    anno_path = get_annotation_file(species,reference_source)
    df_anno = pd.read_csv(anno_path, sep='\t', index_col=0)
    
    is_exits_rate = len(set(df_mtx.index) & set(df_anno.index))/len(set(df_mtx.index))
    click.echo(f"There are {len(set(df_mtx.index) & set(df_anno.index))} out of {len(set(df_mtx.index))} isoform in annotation file") 
    if is_exits_rate < 0.5:
        raise ValueError(f"Thre are only {is_exits_rate} isoform in annotation file; Please check {matrix} and {anno_path};")
    else:
        click.echo(f"There are {len(set(df_mtx.index) & set(df_anno.index))} out of {len(set(df_mtx.index))} isoform in annotation file") 
    

    # Step 1: isoform-level differential expression
    click.echo("⏳ Running isoform-level differential expression analysis...")    
    result_iso = cal_diff(filter_by_express(df_mtx,zero_ratio=0.5,how='isoform'), 
                          df_meta, group, case, control, list(covariates))
    result_iso_anno = df_anno[['gene_name', 'transcript_name', 'transcript_type', 'gene_type']].merge(
        result_iso, left_index=True, right_index=True)
    result_iso_anno.index.name = 'transcript_id'
    result_iso_anno = result_iso_anno.sort_values('pvalue')
    click.echo("✅ Isoform-level differential expression completed.")
    iso_dge_fi = f'{outdir}/results/tables/{case}_vs_{control}.isoform.dtg.results.tsv'
    result_iso_anno.to_csv(iso_dge_fi, sep='\t')
    click.echo(f"📁 Isoform DEG results saved to: {iso_dge_fi}")


    # Step 2: gene-level differential expression
    click.echo("⏳ Running gene-level differential expression analysis...")
    df_gene_mtx = df_mtx.merge(df_anno[['gene_name']], left_index=True, right_index=True)
    df_gene_mtx = df_gene_mtx.groupby('gene_name').sum()
    result_gene = cal_diff(filter_by_express(df_gene_mtx,zero_ratio=0.5,how='gene'), df_meta, group, case, control, list(covariates))
    result_gene_anno = df_anno.reset_index()[['gene_name', 'gene_type']].drop_duplicates().merge(
        result_gene, left_on='gene_name', right_index=True)
    click.echo("✅ Gene-level differential expression completed.")
    gene_dge_fi = f'{outdir}/results/tables/{case}_vs_{control}.gene.deg.results.tsv'
    result_gene_anno.to_csv(gene_dge_fi, sep='\t', index=False)
    click.echo(f"📁 Gene DEG results saved to: {gene_dge_fi}")
    
    # Step 3: sdGene analysis
    # Filter by protein-coding if needed
    if protein_coding:
        click.echo("⏳ Running sdGene identification (protein-coding only)...")
        if 'transcript_type' not in df_anno.columns:
            raise ValueError("'transcript_type' column not found in annotation.")
        tgt_isf_list = df_anno[df_anno['transcript_type'].str.contains('protein_coding')].index
        result_iso_anno_tgt = result_iso_anno.loc[result_iso_anno.index.intersection(tgt_isf_list)]
    else:
        click.echo("⏳ Running sdGene identification (all transcripts)...")
        result_iso_anno_tgt = result_iso_anno


    # Identify splicing driver genes
    df_sgenes = cal_sdgene(result_iso_anno_tgt.reset_index())
    df_sgenes_anno = df_anno.reset_index()[['gene_name', 'gene_type','chromsome','start','end']].drop_duplicates('gene_name').merge(df_sgenes, on='gene_name')
    click.echo("✅ sdGene identification completed.")
    sgene_fi = f'{outdir}/results/tables/{case}_vs_{control}.sdGenes.results.tsv'
    df_sgenes_anno.to_csv(sgene_fi, sep='\t',index=False)
    click.echo(f"📁 sdGene results saved to: {sgene_fi}")
        

@click.command()
@click.option('-m', '--matrix', type=click.Path(exists=True), required=True,
              help='Input gene expression matrix (rows: genes, columns: samples).')
@click.option('-e', '--metadata', type=click.Path(exists=True), required=True,
              help='Sample metadata file.')
@click.option('-g', '--group', required=True,
              help='Group column name in metadata.')
@click.option('-c1', '--case', required=True,
              help='Case group value (e.g., "tumor").')
@click.option('-c2', '--control', required=True,
              help='Control group value (e.g., "normal").')
@click.option('--covariates', multiple=True, default=[],
              help='Covariates to include in the model.')
@click.option('-o', '--outdir', default='./workdir',
              help='Output directory.')
@click.option('--protein-coding', default=True,
              help='Filter results to protein-coding transcripts only.')
@click.option(
    '--species',
    type=click.Choice(['mouse', 'human'], case_sensitive=False),
    default='human',
    show_default=True,
    help='Species: mouse or human'
)
@click.option(
    '--reference-source',
    type=click.Choice(['gencode', 'ncbi'], case_sensitive=False),
    default='gencode',
    show_default=True,
    help='Reference source: gencode or ncbi'
)


def analyze(matrix, metadata, group, case, control, covariates, outdir, protein_coding,species,reference_source):
    """Analyze DGE, DTE and SDG(sdGene) between groups"""
    ## differential gene expression (DGE), differential transcript expression (DTE), and splicing regulation driver genes (SDG/sdGenes)
    run_analyze(matrix, metadata, group, case, control, covariates, outdir, protein_coding,species,reference_source)
    
