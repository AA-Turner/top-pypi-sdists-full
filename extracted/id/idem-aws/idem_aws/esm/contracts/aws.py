def pre(hub, ctx):
    """
    Before using esm, verify that a region_name is part of the profile
    """
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]

    if func_ctx.acct.get("region_name"):
        # Region name already exists for the profile
        return

    # If there is no region_name, get it from hub.OPT
    opt = getattr(hub, "OPT") or {}
    acct = opt.get("acct") or {}
    extras = acct.get("extras") or {}
    aws_opts = extras.get("aws") or {}
    esm_opts = aws_opts.get("esm") or {}

    # Get the region name from the esm config
    if esm_opts.get("region_name"):
        hub.log.debug(
            "Getting region_name from hub.OPT.acct.extras.aws.esm.region_name"
        )
        func_ctx.acct["region_name"] = esm_opts.get("region_name")

    elif aws_opts.get("region_name"):
        # Fall back to the general config for region_name in acct.extras.aws.region_name
        hub.log.debug("Getting region_name from hub.OPT.acct.extras.aws.region_name")
        func_ctx.acct["region_name"] = aws_opts.get("region_name")
