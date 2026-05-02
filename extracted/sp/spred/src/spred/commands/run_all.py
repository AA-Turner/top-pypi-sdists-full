import click
from .analyze import run_analyze
from .enrich import run_enrich
from .plot import run_plot_volcano, run_plot_manhan
import os

@click.command(name="run-all")
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


def run_all(matrix, metadata, group, case, control, covariates, outdir, protein_coding,species,reference_source):
    """Run the entire analysis pipeline."""
    # Step 1: Run analyze command
    click.echo(f"⏳ Running analyze with {matrix}, {case}, {species}...")
    run_analyze(matrix=matrix, 
            metadata=metadata,
            group=group, 
            control=control, 
            case=case, 
            protein_coding = protein_coding,
            covariates=covariates,
            reference_source = reference_source,
            species=species, 
            outdir=outdir)
    
    enrich_outdir = f"{outdir}/results/kogo"
    table_outdfir = f"{outdir}/results/tables"
    
    # Step 2: Run enrich for gene results
    click.echo(f"Enrich outdir: {enrich_outdir}")
    gene_results = f"{table_outdfir}/{case}_vs_{control}.gene.deg.results.tsv"
    gene_enrich_prefix =  f"{case}_vs_{control}.gene.deg"
    
    click.echo(f"⏳ Running enrich for gene results: {gene_results}; outdir: {enrich_outdir}")
    run_enrich(infile=gene_results, outdir=enrich_outdir, prefix=gene_enrich_prefix, 
               protein_coding=protein_coding, species=species, multitest='hs',
               gene_columns='gene_name', padjust_columns='padj', pval_columns='pvalue',
               gene_type_columns='gene_type',lfc_columns='log2FoldChange',
               filter_sig_by='padj', filter_lfc=1, gene_sets=('KEGG_2021_Human', 'GO_Biological_Process_2021')
               )

    # Step 3: Run enrich for isoform results
    isoform_results = f"{table_outdfir}/{case}_vs_{control}.isoform.dtg.results.tsv"
    isoform_enrich_prefix =  f"{case}_vs_{control}.isoform.dtg"
    click.echo(f"⏳ Running enrich for isoform results: {isoform_results}")
    run_enrich(infile=isoform_results, outdir=enrich_outdir, prefix=isoform_enrich_prefix, 
            protein_coding=protein_coding, species=species, multitest='hs',
            gene_columns='gene_name', padjust_columns='padj', pval_columns='pvalue',
            gene_type_columns='gene_type',lfc_columns='log2FoldChange',
            filter_sig_by='padj', filter_lfc=1, gene_sets=('KEGG_2021_Human', 'GO_Biological_Process_2021')
            )


    # Step 4: Run enrich for sdGenes results
    sdgenes_results = f"{table_outdfir}/{case}_vs_{control}.sdGenes.results.tsv"
    sdgenes_enrich_prefix =  f"{case}_vs_{control}.sdGenes.deg"
    click.echo(f"⏳ Running enrich for sdGenes results: {sdgenes_results}")
    run_enrich(infile=sdgenes_results, outdir=enrich_outdir, prefix=sdgenes_enrich_prefix, 
        protein_coding=protein_coding, species=species, multitest='fdr_bh',
        gene_columns='gene_name', padjust_columns='padj', pval_columns='pvalue',
        gene_type_columns='gene_type',lfc_columns='log2FoldChange',
        filter_sig_by='padj', filter_lfc=1, gene_sets=('KEGG_2021_Human', 'GO_Biological_Process_2021')
        )
    
    # Step 5: Run plot-volcano for gene results
    volcano_gene_results = f"{enrich_outdir}/{gene_enrich_prefix}.for_kogo.table.tsv"
    new_volcano_gene_results = f'{table_outdfir}/{gene_enrich_prefix}.for_kogo.table.tsv'
    os.system(f'cp {volcano_gene_results} {new_volcano_gene_results}')
        
    click.echo(f"⏳ Running plot-volcano for gene results: {new_volcano_gene_results}")    
    run_plot_volcano(infile=new_volcano_gene_results, filter_lfc=1, pval_columns='pvalue', 
                     padjust_columns='padj', lfc_columns='log2FoldChange', 
                     filter_sig_by='padj', outdir = table_outdfir,prefix = f"{gene_enrich_prefix}.for_kogo")
    

    # Step 6: Run plot-volcano for isoform results
    volcano_isoform_results = f"{enrich_outdir}/{isoform_enrich_prefix}.for_kogo.table.tsv"
    new_volcano_isoform_results = f'{table_outdfir}/{isoform_enrich_prefix}.for_kogo.table.tsv'
    os.system(f'cp {volcano_isoform_results} {new_volcano_isoform_results}')
    
    click.echo(f"⏳ Running plot-volcano for isoform results: {new_volcano_isoform_results}")
    run_plot_volcano(infile=new_volcano_isoform_results, filter_lfc=1, pval_columns='pvalue', 
                     padjust_columns='padj', lfc_columns='log2FoldChange', 
                     filter_sig_by='padj', outdir = table_outdfir,prefix = f"{isoform_enrich_prefix}.for_kogo")

    # Step 7: Run plot-manhan for sdGenes results with highlighted genes
    manhan_sdgenes_results = f"{enrich_outdir}/{sdgenes_enrich_prefix}.for_kogo.table.tsv"
    new_volcano_sdgenes_results = f'{table_outdfir}/{sdgenes_enrich_prefix}.for_kogo.table.tsv'
    os.system(f'cp {manhan_sdgenes_results} {new_volcano_sdgenes_results}')
    
    click.echo(f"⏳ Running plot-manhan for sdGenes results: {new_volcano_sdgenes_results}")    
    run_plot_manhan(infile=manhan_sdgenes_results, pval_columns='pvalue', 
                     padjust_columns='padj',outdir= table_outdfir, prefix = f"{sdgenes_enrich_prefix}.for_kogo", 
                     log10_cutoff='auto', highlight_genes=None,gene_columns ='gene_name' )

