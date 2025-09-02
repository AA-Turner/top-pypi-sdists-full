def get(hub, ctx=None) -> str:
    """
    Get the region name from ctx and fall back to the region in config
    """
    if ctx and ctx.acct.get("region_name"):
        hub.log.trace("Using region name from acct profile")
        return ctx.acct["region_name"]

    opt = getattr(hub, "OPT") or {}
    acct = opt.get("acct") or {}
    extras = acct.get("extras") or {}
    aws_opts = extras.get("aws") or {}
    if aws_opts.get("region_name"):
        hub.log.trace("Using region name from idem config")
        return aws_opts["region_name"]

    hub.log.trace(
        "No acct profile specified, region and auth tokens may be used by boto from awscli config"
    )
