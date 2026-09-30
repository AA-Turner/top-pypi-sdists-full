"""Auto-generated stub for module: identity."""
from typing import Any, Callable, Optional, Tuple

# Functions
def config_get(config: Any, keys: Any[str]) -> Optional[str]:
    """
    First non-empty string among ``keys``, from a dict or an attribute-bearing object.
    
        Both shapes are real and this is why the function exists: ``PostProcRunner`` passes the raw
        ``post_processing_config`` dict, while ``PostProcessor`` passes a *parsed* config object. A
        dict-only reader -- which is what ``backends._config_value`` is -- would make the two SDK entry
        points disagree about whether an app has a bundle, and keeping them in agreement is the entire
        reason ``select_engine_backend`` is a single function.
    
        Returns ``None`` rather than ``""`` for a miss, so a caller can chain with ``or`` and tell a
        source that answered blank from one that answered nothing.
    
        ``Mapping``, not ``dict``: a read-only view or a ``ChainMap`` is a mapping that is not a
        ``dict``, and testing for the concrete type sends it down the attribute branch, where it
        has no attribute to find and reads as empty. :func:`~.bootstrap.get_action_record` already
        pays a deep copy per call to avoid handing anyone a ``MappingProxyType`` for exactly this
        reason; the reader is the right place to fix it.
    """
    ...
def first_str(data: Any[str, Any], keys: Any[str]) -> Optional[str]:
    """
    The first non-blank string among ``keys``, unwrapping ``{"$oid": ...}`` encodings.
    
        Mapping-only, unlike :func:`config_get`: its sources are documents that came back from the
        platform, which are always dictionaries. What it adds instead is the ``$oid`` unwrap -- some
        encoders render an ObjectId as ``{"$oid": "..."}`` rather than as a string, and without the
        unwrap that field reads as a miss and the caller goes looking for an answer it already had.
    """
    ...
def resolve_app_deployment_id(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which deployment this is, or ``""`` when no source knows.
    
        Same shape as :func:`resolve_application_id` with **the two record slices reversed**:
        ``actionDetails`` is searched before ``jobParams``. That is not a style choice -- the two
        slices carry different values for this field, and reading them in the other order answers
        with the wrong deployment rather than with nothing.
    
        Args:
            stream_info: The frame's own description, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record; called only on a miss.
    
        Returns:
            The id, or ``""`` when no source knew.
    """
    ...
def resolve_application_id(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which application this is, or ``""`` when no source knows.
    
        Order, cheapest first:
    
        1. ``stream_info`` -- already in hand on the frame path,
        2. the **raw** post-processing config -- also in hand,
        3. the action record's ``jobParams``, then its ``actionDetails`` -- one round trip, and
           only if the first two missed.
    
        ``jobParams`` is searched **before** ``actionDetails``, and that order is specific to this
        field: :func:`resolve_app_deployment_id` searches the two the other way round. The record
        carries both slices and they disagree, so the order is per field rather than per record.
    
        The key is plain ``application_id`` at every step here. A post-processing config read back
        from the backend as a **document** spells it ``_idApplication`` instead; that is a
        different source with a different shape, and a caller holding one of those documents
        should read that field itself rather than pass it here as though it were a config.
    
        Args:
            stream_info: The frame's own description of what it belongs to, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record. Called only if the
                two free sources miss, so the round trip is paid only when it buys something.
    
        Returns:
            The id, or ``""`` -- which means *no source knew*, and is a refusal rather than a
            value. Callers decide what to do about it; this function never invents one.
    """
    ...
def resolve_application_version(stream_info: Optional[Any[str, Any]] = None, pp_config: Any = None, action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which version of the application is deployed, or ``""`` when no source knows.
    
        The version travels with the application id on a ``deploy_add`` record, so the same order
        applies and the same round trip answers both. A ``deploy_postproc_add`` record carries no
        version at all, which is a miss rather than a fault -- the deployment record knows it, and
        that is a call the caller makes, not this function.
    
        **This is the version a deployment RUNS.** The application catalogue also publishes a
        version, and the two are routinely different; a caller that wants the published one is
        asking a different question.
    
        Args:
            stream_info: The frame's own description, if there is one.
            pp_config: The raw post-processing config, if the caller holds one.
            action_record: A function returning this worker's action record; called only on a miss.
    
        Returns:
            The version, or ``""`` when no source knew.
    """
    ...
def resolve_location(*sources: Any) -> Tuple[str, str]:
    """
    Which site a camera belongs to, as ``(location_id, location_name)``; ``""`` for a miss.
    
        ``sources`` are the camera descriptions the caller already holds, most specific first --
        the matched camera entry, then ``camera_info`` and the stream's own fields. Each half is
        the first source that answers it, so the id and the name may come from different sources.
    
        **``location`` is read by shape, because it holds either.** Before the post-processor
        enriches a stream, ``location`` is the site's id; after, it is the site's display NAME
        (resolved from the id). Read as an id unconditionally, a name reaches
        ``get_location/{id}`` and is a 400 on every cool-off -- measured live on LPR and FR in
        2026-09. So:
    
        * the id is ``location_id`` / ``locationId``, else ``location`` only when it is a 24-hex
          ObjectId; the all-zero placeholder the platform writes for "no site" is no id,
        * the name is ``location`` / ``locationName`` only when it is **not** id-shaped: showing
          a user ``68f28be1f74ae116727448c4`` as a site name is worse than showing nothing.
    
        Deciding is all this does. Looking the name up for an id is the caller's round trip
        (``InferenceAPI.fetch_location``), taken only when the id came without a name.
    
        Args:
            *sources: Mappings or attribute-bearing objects, most specific first. ``None`` is
                skipped.
    
        Returns:
            ``(location_id, location_name)``, either of which may be ``""``.
    """
    ...
def resolve_project_id(action_record: Optional[Callable[[], Any[str, Any]]] = None) -> str:
    """
    Which project this worker belongs to, or ``""`` -- **read the warnings first**.
    
        This resolver is narrower than the other three and deliberately so.
    
        **It has one source: the action record's ``_idProject``.** Not ``jobParams``, not
        ``actionDetails`` -- the field sits at the top level of the record.
    
        **The session's own ``project_id`` is not a source, although it is the first one today.**
        The live resolution starts at ``getattr(session, "project_id", "")`` and only then falls
        through to the rest. That source cannot come here, because reaching it means holding a
        session and this module holds none -- which is the property that lets every function in it
        be tested with a literal. A caller that has a session already has the answer without
        asking, so it reads its own first and calls this only on a miss::
    
            project_id = getattr(session, "project_id", "") or resolve_project_id(get_record)
    
        Two sentences of the caller's, rather than a session parameter that would put I/O one
        argument away from every function in this file.
    
        **It is empty on a decoupled deployment, by design rather than by accident.** The
        ``deploy_postproc_add`` record a decoupled analytics container is launched with carries no
        ``_idProject`` at all, so this answers ``""`` there and always will. That is why an
        analytics client needs no project, and why a caller that treats ``""`` as a fault will
        report one on every decoupled node.
    
        **``$MATRICE_PROJECT_ID`` is deliberately not a source here.** It is written by the
        facial-recognition path and read by it, inside one container. A container runs one usecase,
        so every read of that variable from outside facial recognition has no writer in its own
        process and returns ``""`` on every call. Adding it here would document a fallback that
        cannot fire and would hide the real answer -- that those callers have no project.
    
        **The licence-plate path's ``projectID`` is a different source, not a fallback.** It comes
        off the LPR server record, spells the key differently, and is scoped to that server rather
        than to this worker. Merging the two would answer one question with the other's value.
    
        Args:
            action_record: A function returning this worker's action record.
    
        Returns:
            The project id, or ``""`` -- which on a decoupled node is the correct answer.
    """
    ...
def resolve_sidecar_base_url(host: str, port: Any) -> str:
    """
    Where to reach a sidecar whose server record says it is at ``host:port``.
    
        A sidecar's record names the address it is reachable at from outside. When that address is
        **this machine's own**, the sidecar is running on this box and the loopback address reaches
        it without leaving the host -- so the record's host is replaced with ``localhost`` while
        the port is kept.
    
        ``public_ip`` is passed in rather than looked up, because looking it up is an outbound
        request and this module makes none. ``resolve_public_ip_once`` does that half, caches it
        for the process, and answers ``"localhost"`` when the lookup fails -- a cheap wrong answer
        beating a correct one that costs the first frame two minutes. A caller that does not have
        the value, or does not care, omits it and gets the record's own address, which is
        reachable either way; the loopback form only avoids a round trip out of the machine and
        back.
    
        **This refuses where the two existing copies guess, and that is the one behavioural
        difference to know about.** Both of them read the record as ``get("host", "localhost")``
        and ``get("port", 8081)``, so a record that carries neither produces
        ``http://localhost:8081`` -- an address that looks resolved and points at whatever happens
        to answer on this box. A caller that wants those defaults states them at the call site,
        where the reader can see which value is the record's and which is the fallback::
    
            resolve_sidecar_base_url(rec.host or "localhost", rec.port or 8081, public_ip=ip)
    
        Args:
            host: The host from the server record.
            port: The port from the server record. Accepts the integer the record carries or the
                string some producers send.
            public_ip: This machine's public address, if the caller knows it.
    
        Returns:
            A base URL, or ``""`` when the record carried no host -- a refusal rather than a
            guess. A port of its own is omitted when the record had none, rather than defaulted:
            the two sidecars listen on different ports, so there is no value this function could
            supply that would be right for both.
    """
    ...
