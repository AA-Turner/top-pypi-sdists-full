import plotly.graph_objects as go

from algowalk.utils.visualizer import StepVisualizer


class PlotlyStepVisualizer(StepVisualizer):

    def visualize(self, steps):
        if not steps or 'array' not in steps[0]:
            raise ValueError("Steps must be a list of dicts with at least an 'array' key.")

        total = len(steps[0]['array'])

        fig = go.Figure(
            layout=go.Layout(
                title="Sorting Algorithm - Dry run Visualization",
                xaxis=dict(title="Index", range=[-1, total]),
                yaxis=dict(title="Value", range=[0, max(max(step['array']) for step in steps) + 5]),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        buttons=[
                            dict(
                                label="▶ Play",
                                method="animate",
                                args=[None, {
                                    "frame": {"duration": 1000, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 500, "easing": "linear"}
                                }]
                            ),
                            dict(
                                label="⏸ Pause",
                                method="animate",
                                args=[[None], {
                                    "mode": "immediate",
                                    "frame": {"duration": 0, "redraw": False},
                                    "transition": {"duration": 0}
                                }]
                            )
                        ]
                    )
                ]
            )
        )

        # Initial frame
        initial_step = steps[0]
        fig.add_trace(go.Bar(
            x=list(range(total)),
            y=initial_step['array'],
            marker_color=["gray"] * total,
            hoverinfo="x+y"
        ))

        frames = []
        for i, step in enumerate(steps):
            arr = step['array']
            i_idx = step.get('i')
            j_idx = step.get('j')
            swap = step.get('swap', False)

            colors = ["gray"] * total
            if i_idx is not None and 0 <= i_idx < total:
                colors[i_idx] = "yellow"
            if j_idx is not None and 0 <= j_idx < total:
                colors[j_idx] = "red" if swap else "yellow"

            # Final step coloring
            if i == len(steps) - 1:
                colors = ["green"] * total

            frames.append(go.Frame(
                data=[go.Bar(
                    x=list(range(total)),
                    y=arr,
                    marker_color=colors
                )],
                name=f"frame{i}"
            ))

        fig.frames = frames
        fig.show()