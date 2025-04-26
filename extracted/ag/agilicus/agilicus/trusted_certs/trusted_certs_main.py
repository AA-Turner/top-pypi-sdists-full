import click
from ..output.table import output_entry
from . import trusted_certs


@click.command(name="add-trusted-certificate")
@click.argument("certificate", nargs=-1, type=click.Path(exists=True))
@click.option("--root", is_flag=True)
@click.option("--label", type=str, multiple=True)
@click.option("--org-id", default=None)
@click.option("--quiet", default=True)
@click.pass_context
def cli_command_add_trusted_certificate(ctx, certificate, label, quiet, **kwargs):
    for cert in certificate:
        results = trusted_certs.add_certificate(
            ctx, certificate=cert, labels=list(label), **kwargs
        )
        if quiet:
            continue
        for result in results:
            output_entry(ctx, result.to_dict())


@click.command(name="show-trusted-certificate")
@click.argument("certificate-id")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_show_trusted_certificate(ctx, **kwargs):
    result = trusted_certs.get_certificate(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-trusted-certificate")
@click.argument("certificate-id")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_trusted_certificate(ctx, **kwargs):
    trusted_certs.delete_certificate(ctx, **kwargs)


@click.command(name="add-trusted-certificate-label")
@click.argument("label", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_trusted_certificate_label(ctx, label, **kwargs):
    for _label in label:
        result = trusted_certs.add_label(ctx, label=_label, **kwargs)
        output_entry(ctx, result.to_dict())


@click.command(name="list-trusted-certificate-labels")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_trusted_certificate_labels(ctx, **kwargs):
    results = trusted_certs.list_labels(ctx, **kwargs)
    print(trusted_certs.format_labels(ctx, results))


@click.command(name="list-trusted-certificate-orgs")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_trusted_certificate_orgs(ctx, **kwargs):
    results = trusted_certs.list_orgs(ctx, **kwargs)
    print(trusted_certs.format_orgs(ctx, results))


@click.command(name="list-trusted-certificates")
@click.option("--org-id", default=None)
@click.option("--trusted-cert-label", default=None)
@click.option("--subject-search", default=None)
@click.option("--issuer-search", default=None)
@click.option("--subject", default=None)
@click.option("--issuer", default=None)
@click.option("--skid", default=None)
@click.option("--serial-number", default=None)
@click.option("--cert-root", is_flag=True, default=None)
@click.option("--key-usage-extension-search", default=None)
@click.option("--key-usage-crl-sign", is_flag=True, default=None)
@click.option("--key-usage-key-cert-sign", is_flag=True, default=None)
@click.pass_context
def cli_command_list_trusted_certificates(ctx, **kwargs):
    results = trusted_certs.list_certificates(ctx, **kwargs)
    print(trusted_certs.format_certificates_as_text(ctx, results))


@click.command(name="add-trusted-certificate-bundle")
@click.argument("bundle")
@click.option("--org-id", default=None)
@click.option("--label", default=None)
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_trusted_certificate_bundle(ctx, **kwargs):
    result = trusted_certs.add_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="add-trusted-certificate-bundle-label")
@click.argument("bundle-id")
@click.argument("label")
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_trusted_certificate_bundle_label(ctx, **kwargs):
    result = trusted_certs.add_bundle_label(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-trusted-certificate-bundle")
@click.argument("bundle-id", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_trusted_certificate_bundle(ctx, bundle_id, **kwargs):
    for _bundle_id in bundle_id:
        trusted_certs.delete_bundle(ctx, bundle_id=_bundle_id, **kwargs)


@click.command(name="list-trusted-certificate-bundles")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_trusted_certificate_bundle(ctx, **kwargs):
    results = trusted_certs.list_bundles(ctx, **kwargs)
    print(trusted_certs.format_bundles(ctx, results))


@click.command(name="get-trusted-certificate-bundle")
@click.argument("bundle-id")
@click.option("--org-id", default=None)
@click.option("--get-certs", is_flag=True, default=None)
@click.option("--trusted-cert-bundle-etag", default=None)
@click.pass_context
def cli_command_get_trusted_certificate_bundle(ctx, **kwargs):
    result = trusted_certs.get_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
