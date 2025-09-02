def pre_present(hub, ctx):
    hub.tool.aws.parameters.sync_sls_name_and_tag(ctx.ref, ctx.kwargs)
