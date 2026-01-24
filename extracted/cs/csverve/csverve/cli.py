"""Console script for csverve."""
import os

import click
import csverve.api as api
import yaml


@click.group()
def cli():
    pass


@cli.command()
@click.option('--in_f', multiple=True, required=True, help='CSV file path, allows multiple paths.')
@click.option('--out_f', required=True, help='Path of resulting merged CSV.')
@click.option('--how', required=True, help='How to join CSVs.')
@click.option('--on', multiple=True, required=False, help='Column to join CSVs on, allowes multiple.')
@click.option('--skip_header', is_flag=True, default=False, help='Writer header to resulting CSV.')
def merge(
        in_f,
        out_f,
        how,
        on,
        skip_header,
):
    on = list(on)
    api.merge_csv(
        list(in_f),
        out_f,
        how,
        on,
        skip_header,
    )


@cli.command()
@click.option('--in_f', required=True, help='CSV file path. Expects YAML w/ the same path as CSV with .yaml extension.')
@click.option('--out_f', required=True, help='Path of resulting merged CSV.')
@click.option('--dtypes', required=True, help='dtypes yaml file')
@click.option('--skip_header', is_flag=True, default=False, help='Writer header to resulting CSV.')
def rewrite(
        in_f,
        out_f,
        skip_header,
        dtypes
):
    assert os.path.exists(in_f)

    with open(dtypes, 'rt') as reader:
        dtypes_data = yaml.load(reader)

    api.rewrite_csv_file(
        in_f,
        out_f,
        skip_header,
        dtypes_data
    )


@cli.command()
@click.option('--in_f', required=True, help='CSV file path. Expects YAML w/ the same path as CSV with .yaml extension.')
@click.option('--out_f', required=True, help='Path of resulting merged CSV.')
@click.option('--skip_header', is_flag=True, default=False, help='Writer header to resulting CSV.')
def remove_duplicates(
        in_f,
        out_f,
        skip_header
):
    assert os.path.exists(in_f)

    api.remove_duplicates(
        in_f,
        out_f,
        skip_header
    )


@cli.command()
@click.option('--in_f', multiple=True, required=True, help='CSV file path, allows multiple paths.')
@click.option('--out_f', required=True, help='Path of resulting merged CSV.')
@click.option('--skip_header', is_flag=True, default=False, help='Writer header to resulting CSV.')
@click.option('--drop_duplicates', is_flag=True, default=False, help='remove duplicate rows')
def concat(
        in_f,
        out_f,
        skip_header,
        drop_duplicates
):
    api.concatenate_csv(
        list(in_f),
        out_f,
        skip_header,
        drop_duplicates
    )


@cli.command()
@click.option('--in_f', required=True, help='CSV file path, allows multiple paths.')
@click.option('--out_f', required=True, help='Path of resulting merged CSV.')
@click.option('--col_name', required=True, help='Column name to be added.')
@click.option('--col_val', required=True, help='Column value to be added (one value for all).')
@click.option('--col_dtype', required=True, help='Column pandas dtype.')
@click.option('--skip_header', is_flag=True, default=False, help='Writer header to resulting CSV.')
def annotate(
        in_f,
        out_f,
        col_name,
        col_val,
        col_dtype,
        skip_header,
):
    api.simple_annotate_csv(
        in_f,
        out_f,
        col_name,
        col_val,
        col_dtype,
        skip_header,
    )


if __name__ == "__main__":
    cli()
