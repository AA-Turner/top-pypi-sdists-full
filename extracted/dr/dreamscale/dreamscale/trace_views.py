"""Repository-owned Rerun layout for asynchronous YAM diagnostics."""


def blueprint(contract=None):
    import rerun as rr
    import rerun.blueprint as bp
    from dreamscale_transport import catalog

    from dreamscale.policy.runtime.contract import runtime_contract_for_model

    # With none, YAM's default model's (the robot these views diagnose).
    contract = contract or runtime_contract_for_model(catalog.robot_models("yam")[0])
    groups = contract.joint_groups
    names = (
        ("left", "right") if len(groups) == 2 else tuple(f"arm_{i + 1}" for i in range(len(groups)))
    )
    normalized = set(contract.gripper_indices).issubset(contract.normalized_gripper_indices)
    gripper_unit = "[0,1]" if normalized else "raw checkpoint units"

    def joint_view(prefix, side, joint, name, count):
        return bp.TimeSeriesView(
            origin=f"{prefix}/{side}",
            name=name,
            plot_legend=bp.PlotLegend(visible=False),
            overrides={
                f"/{prefix}/{side}/{kind}": rr.SeriesLines(
                    visible_series=[index == joint for index in range(count)],
                )
                for kind in ("requested", "accepted", "measured")
            },
        )

    return bp.Blueprint(
        bp.Tabs(
            bp.Vertical(
                bp.TimeSeriesView(
                    origin="queue",
                    contents=["/queue/remaining", "/queue/capacity"],
                    name="Queue coverage (ticks)",
                ),
                bp.TimeSeriesView(
                    origin="queue",
                    contents=["/queue/hold", "/queue/in_flight"],
                    name="Hold / request active (0 or 1)",
                ),
                bp.TimeSeriesView(
                    origin="latency",
                    name="Request / network / inference / dispatch (ms)",
                    contents=[
                        f"/latency/{name}"
                        for name in (
                            "obs_to_action_ms",
                            "data_plane_rtt_ms",
                            "worker_inference_ms",
                            "dispatch_ms",
                        )
                    ],
                ),
                bp.TimeSeriesView(
                    origin="smoothing",
                    name="Adaptive response",
                    contents=[
                        f"/smoothing/{name}"
                        for name in (
                            "transition_steps",
                            "arm_speed_rad_s",
                            "correction_gain",
                            "new_action_weight",
                            "correction_rate_ratio",
                        )
                    ],
                ),
                name="Health",
            ),
            bp.TimeSeriesView(origin="latency", name="All latency components (ms)"),
            bp.Tabs(
                *(
                    bp.Vertical(
                        joint_view(
                            "joints", side, joint, f"Position ({contract.joint_unit})", len(group)
                        ),
                        joint_view(
                            "velocity",
                            side,
                            joint,
                            f"Velocity ({contract.joint_unit}/s)",
                            len(group),
                        ),
                        bp.Spatial2DView(
                            origin=f"horizon/{side}/{joint}",
                            name="Horizon: raw purple / old gray / merged amber",
                            visual_bounds=bp.VisualBounds2D(
                                x_range=(-170, 820), y_range=(-30, 260)
                            ),
                        ),
                        name=f"{side} joint {joint + 1}",
                    )
                    for side, group in zip(names, groups, strict=True)
                    for joint in range(len(group))
                ),
                name="Arms",
            ),
            bp.Vertical(
                *(
                    bp.TimeSeriesView(
                        origin=f"grippers/{side}", name=f"{side} gripper {gripper_unit}"
                    )
                    for side in names[: len(contract.gripper_indices)]
                ),
                name="Grippers",
            ),
            bp.Horizontal(
                bp.TensorView(
                    origin="disagreement/arms",
                    name=f"Raw prediction disagreement ({contract.joint_unit})",
                    scalar_mapping=bp.TensorScalarMapping(colormap="Viridis"),
                ),
                bp.TensorView(
                    origin="disagreement/grippers",
                    name=f"Raw gripper disagreement ({gripper_unit})",
                    scalar_mapping=bp.TensorScalarMapping(colormap="Viridis"),
                ),
                bp.TextDocumentView(origin="merge_details", name="Alignment / response"),
                name="Overlap",
            ),
            bp.Horizontal(
                *(
                    bp.Spatial2DView(origin=f"cameras/{role}", name=role)
                    for role in ("top", "left", "right")
                ),
                name="Inference inputs",
            ),
            bp.TextDocumentView(origin="summary", name="Partial / final summary"),
        ),
        bp.TimePanel(timeline="elapsed"),
        auto_layout=False,
        auto_views=False,
    )
