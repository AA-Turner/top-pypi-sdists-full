#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
PredictionGrid for the FeatrixSphere OO API.

Grid-based prediction batch with automatic matrix building and visualization.
Enables parameter sweep exploration across 1-3 dimensions with built-in plotting.
"""

import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .predictor import Predictor

logger = logging.getLogger(__name__)


class PredictionGrid:
    """
    Grid-based prediction batch with automatic matrix building and visualization.

    Collects prediction records at grid positions, then processes them all in one
    efficient batch call. Results are stored in numpy matrices for easy analysis
    and visualization.

    Usage:
        # Create grid from a predictor
        grid = predictor.predict_grid(degrees_of_freedom=2, grid_shape=(10, 8))

        # Set axis labels and values
        grid.set_axis_labels(['Spend ($)', 'Ad Set Campaign'])
        grid.set_axis_values(0, [f"${s}" for s in spend_levels])
        grid.set_axis_values(1, ad_sets)

        # Fill grid (records are collected, not predicted yet)
        for i, spend in enumerate(spend_levels):
            for j, ad_set in enumerate(ad_sets):
                record = {"spend": spend, "ad_set_name": ad_set}
                grid.predict(record, grid_position=(i, j))

        # Process all predictions in one batch
        grid.process_batch()

        # Visualize
        grid.plot_heatmap()   # 2D heatmap
        grid.plot_3d()        # 3D surface
    """

    def __init__(
        self,
        predictor: 'Predictor',
        degrees_of_freedom: int,
        grid_shape: tuple = None,
    ):
        self._predictor = predictor
        self.degrees_of_freedom = degrees_of_freedom

        # Grid shape
        if grid_shape:
            self.grid_shape = grid_shape
        else:
            default_sizes = {1: (20,), 2: (10, 10), 3: (8, 8, 8)}
            self.grid_shape = default_sizes.get(degrees_of_freedom, (10,) * degrees_of_freedom)

        # Prediction matrices
        self._prediction_matrix = {}  # class_name -> numpy array
        self._confidence_matrix = None
        self._filled_positions = set()

        # Batch collection
        self._pending_records = {}  # grid_position -> record
        self._batch_processed = False

        # Metadata for plotting
        self._axis_labels = [f"Param {i+1}" for i in range(degrees_of_freedom)]
        self._axis_values = [[] for _ in range(degrees_of_freedom)]
        self._colormap = 'viridis'

        # Statistics
        self._stats = {'predictions': 0, 'batched': 0, 'errors': 0}

    def predict(self, record: Dict[str, Any], grid_position: tuple) -> Dict[str, str]:
        """
        Queue a record for batch processing at a specific grid position.

        Args:
            record: Feature data to predict
            grid_position: Grid coordinates - (i,) for 1D, (i,j) for 2D, (i,j,k) for 3D

        Returns:
            Status dict with queuing info
        """
        if len(grid_position) != self.degrees_of_freedom:
            raise ValueError(f"Grid position must have {self.degrees_of_freedom} dimensions, got {len(grid_position)}")

        for i, pos in enumerate(grid_position):
            if pos >= self.grid_shape[i]:
                raise ValueError(f"Grid position {pos} exceeds dimension {i} size {self.grid_shape[i]}")

        self._pending_records[grid_position] = record

        return {
            "status": "queued_for_batch",
            "grid_position": grid_position,
            "total_queued": len(self._pending_records),
            "message": f"Record queued at position {grid_position}. Call process_batch() to run predictions."
        }

    def process_batch(self, show_progress: bool = True) -> Dict[str, Any]:
        """
        Process all queued records in a single batch prediction.

        Args:
            show_progress: Whether to show progress during batch processing

        Returns:
            Batch processing results with counts of processed/successful/failed
        """
        if not self._pending_records:
            return {"message": "No records to process", "processed": 0}

        if self._batch_processed:
            return {"message": "Batch already processed", "processed": len(self._filled_positions)}

        # Build ordered list and position mapping
        records_list = []
        position_mapping = {}  # list_index -> grid_position

        for grid_pos, record in self._pending_records.items():
            idx = len(records_list)
            records_list.append(record)
            position_mapping[idx] = grid_pos

        if show_progress:
            print(f"Processing {len(records_list)} grid positions in batch...")

        try:
            results = self._predictor.batch_predict(
                records=records_list,
                show_progress=show_progress,
            )

            successful = 0
            failed = 0

            for i, result in enumerate(results):
                grid_pos = position_mapping.get(i)
                if grid_pos is None:
                    failed += 1
                    continue

                probabilities = result.probabilities
                if not probabilities:
                    # Fall back: if probabilities is empty but we have a prediction dict
                    if isinstance(result.prediction, dict):
                        probabilities = result.prediction
                    else:
                        failed += 1
                        self._stats['errors'] += 1
                        continue

                # Initialize matrices on first successful prediction
                if not self._prediction_matrix:
                    self._initialize_matrices(probabilities.keys())

                # Fill matrices
                for class_name, probability in probabilities.items():
                    if class_name in self._prediction_matrix:
                        self._prediction_matrix[class_name][grid_pos] = probability

                # Confidence = highest probability
                max_prob = max(probabilities.values())
                self._confidence_matrix[grid_pos] = max_prob

                self._filled_positions.add(grid_pos)
                successful += 1

            self._stats['predictions'] = successful
            self._stats['batched'] = len(records_list)
            self._batch_processed = True
            self._pending_records.clear()

            if show_progress:
                print(f"Batch complete: {successful} successful, {failed} failed")
                print(f"Grid filled: {len(self._filled_positions)} positions")

            return {
                "processed": len(records_list),
                "successful": successful,
                "failed": failed,
            }

        except Exception as e:
            self._stats['errors'] += len(records_list)
            raise Exception(f"Error processing grid batch: {str(e)}")

    def _initialize_matrices(self, class_names):
        """Initialize prediction matrices for each class."""
        import numpy as np

        for class_name in class_names:
            self._prediction_matrix[class_name] = np.full(self.grid_shape, np.nan)

        self._confidence_matrix = np.full(self.grid_shape, np.nan)

    def set_axis_labels(self, labels: list):
        """Set custom labels for axes."""
        if len(labels) != self.degrees_of_freedom:
            raise ValueError(f"Must provide {self.degrees_of_freedom} labels")
        self._axis_labels = labels

    def set_axis_values(self, axis_index: int, values: list):
        """Set actual values for an axis (for proper tick labels)."""
        if axis_index >= self.degrees_of_freedom:
            raise ValueError(f"Axis index {axis_index} exceeds degrees of freedom {self.degrees_of_freedom}")
        self._axis_values[axis_index] = values

    def get_optimal_position(self, class_name: str = None) -> tuple:
        """
        Find grid position with highest probability for a class.

        Args:
            class_name: Class to optimize for (default: highest average probability)

        Returns:
            Grid position tuple with highest probability
        """
        import numpy as np

        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name]
        return np.unravel_index(np.nanargmax(matrix), matrix.shape)

    def get_stats(self) -> Dict[str, Any]:
        """Get grid statistics."""
        import numpy as np

        total_positions = int(np.prod(self.grid_shape))
        filled_ratio = len(self._filled_positions) / total_positions if total_positions > 0 else 0

        return {
            'grid_shape': self.grid_shape,
            'degrees_of_freedom': self.degrees_of_freedom,
            'total_positions': total_positions,
            'filled_positions': len(self._filled_positions),
            'fill_ratio': filled_ratio,
            'pending_records': len(self._pending_records),
            'batch_processed': self._batch_processed,
            'predictions_made': self._stats['predictions'],
            'errors': self._stats['errors'],
            'available_classes': list(self._prediction_matrix.keys()) if self._prediction_matrix else []
        }

    def export_data(self) -> Dict[str, Any]:
        """Export grid data for external analysis."""
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        return {
            'prediction_matrices': {cls: matrix.tolist() for cls, matrix in self._prediction_matrix.items()},
            'confidence_matrix': self._confidence_matrix.tolist() if self._confidence_matrix is not None else None,
            'grid_shape': self.grid_shape,
            'axis_labels': self._axis_labels,
            'axis_values': self._axis_values,
            'filled_positions': list(self._filled_positions),
            'stats': self.get_stats()
        }

    # -------------------------------------------------------------------------
    # Plotting methods
    # -------------------------------------------------------------------------

    def _best_class(self) -> str:
        """Return the class name with the highest average probability."""
        import numpy as np

        avg_probs = {}
        for cls, matrix in self._prediction_matrix.items():
            avg_probs[cls] = np.nanmean(matrix)
        return max(avg_probs, key=avg_probs.get)

    def plot_heatmap(self, class_name: str = None, figsize: tuple = (10, 8), title: str = None):
        """
        Plot 2D heatmap of prediction probabilities.

        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title

        Returns:
            (fig, ax) matplotlib objects
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("Heatmap plotting only supports 2D grids")
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        import matplotlib.pyplot as plt
        import numpy as np

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name]

        fig, ax = plt.subplots(figsize=figsize)

        # Transpose: axis 0 on X, axis 1 on Y
        display_matrix = matrix.T
        im = ax.imshow(display_matrix, cmap=self._colormap, aspect='auto', origin='lower')

        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(self._axis_labels[1])

        if self._axis_values[0]:
            ax.set_xticks(range(len(self._axis_values[0])))
            ax.set_xticklabels(self._axis_values[0])
        if self._axis_values[1]:
            ax.set_yticks(range(len(self._axis_values[1])))
            ax.set_yticklabels(self._axis_values[1])

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(f'Probability of {class_name}')

        if title is None:
            title = f'Prediction Heatmap: {class_name}'
        ax.set_title(title)

        plt.tight_layout()
        return fig, ax

    def plot_3d(self, class_name: str = None, figsize: tuple = (12, 9), title: str = None,
                value_filter: tuple = None, opacity: float = 0.8, show_wireframe: bool = False):
        """
        Plot 3D surface of prediction probabilities.

        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title
            value_filter: (min_value, max_value) to filter displayed predictions
            opacity: Surface opacity (0.0-1.0)
            show_wireframe: Overlay wireframe on surface

        Returns:
            (fig, ax) matplotlib objects
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("3D surface plotting only supports 2D grids")
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        import matplotlib.pyplot as plt
        import numpy as np
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name].copy()

        if value_filter is not None:
            min_val, max_val = value_filter
            mask = (matrix < min_val) | (matrix > max_val)
            matrix[mask] = np.nan

        x = np.arange(matrix.shape[0])
        y = np.arange(matrix.shape[1])
        X, Y = np.meshgrid(x, y, indexing='ij')

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_surface(X, Y, matrix, cmap=self._colormap, alpha=opacity)

        if show_wireframe:
            ax.plot_wireframe(X, Y, matrix, alpha=0.3, color='black', linewidth=0.5)

        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(self._axis_labels[1])
        ax.set_zlabel(f'Probability of {class_name}')

        if self._axis_values[0]:
            ax.set_xticks(range(len(self._axis_values[0])))
            ax.set_xticklabels(self._axis_values[0])
        if self._axis_values[1]:
            ax.set_yticks(range(len(self._axis_values[1])))
            ax.set_yticklabels(self._axis_values[1])

        cbar = fig.colorbar(surf, ax=ax, shrink=0.5)
        cbar.set_label(f'Probability of {class_name}')

        if title is None:
            title = f'3D Prediction Surface: {class_name}'
            if value_filter:
                title += f' (filtered: {value_filter[0]:.3f}-{value_filter[1]:.3f})'
        ax.set_title(title)

        return fig, ax

    def plot_3d_interactive(self, class_name: str = None, figsize: tuple = (12, 9)):
        """
        Create interactive 3D plot with sliders for Jupyter notebooks.

        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size

        Returns:
            Interactive widget (in Jupyter) or regular plot (elsewhere)
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("Interactive 3D plotting only supports 2D grids")
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        try:
            from IPython.display import display  # noqa: F401
            from ipywidgets import interact, FloatSlider, FloatRangeSlider, Checkbox
            import numpy as np
        except ImportError:
            print("Interactive widgets require Jupyter and ipywidgets")
            print("   Install with: pip install ipywidgets")
            print("   Falling back to static 3D plot...")
            return self.plot_3d(class_name=class_name, figsize=figsize)

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name]
        min_val = float(np.nanmin(matrix))
        max_val = float(np.nanmax(matrix))
        value_range = max_val - min_val

        print(f"Interactive 3D Surface Explorer: {class_name}")
        print(f"   Value range: {min_val:.4f} to {max_val:.4f}")

        def update_plot(value_range=(min_val, max_val), opacity=0.8, wireframe=False):
            import matplotlib.pyplot as plt
            plt.close('all')
            fig, ax = self.plot_3d(
                class_name=class_name, figsize=figsize,
                value_filter=value_range, opacity=opacity,
                show_wireframe=wireframe
            )
            filtered = matrix.copy()
            mask = (filtered < value_range[0]) | (filtered > value_range[1])
            filtered[mask] = np.nan
            visible = np.sum(~np.isnan(filtered))
            total = np.sum(~np.isnan(matrix))
            pct = (visible / total) * 100 if total > 0 else 0
            print(f"Showing {visible}/{total} points ({pct:.1f}%)")
            plt.show()

        value_slider = FloatRangeSlider(
            value=(min_val, max_val), min=min_val, max=max_val,
            step=value_range / 100 if value_range > 0 else 0.01,
            description='Value Filter:', continuous_update=False,
            style={'description_width': 'initial'}
        )
        opacity_slider = FloatSlider(
            value=0.8, min=0.1, max=1.0, step=0.1,
            description='Opacity:', continuous_update=False,
            style={'description_width': 'initial'}
        )
        wireframe_checkbox = Checkbox(
            value=False, description='Show Wireframe',
            style={'description_width': 'initial'}
        )

        return interact(
            update_plot,
            value_range=value_slider,
            opacity=opacity_slider,
            wireframe=wireframe_checkbox
        )

    def plot_1d(self, class_name: str = None, figsize: tuple = (10, 6), title: str = None):
        """
        Plot 1D line plot of prediction probabilities.

        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title

        Returns:
            (fig, ax) matplotlib objects
        """
        if self.degrees_of_freedom != 1:
            raise ValueError("1D plotting only supports 1D grids")
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        import matplotlib.pyplot as plt

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name]

        fig, ax = plt.subplots(figsize=figsize)
        x = self._axis_values[0] if self._axis_values[0] else range(len(matrix))
        ax.plot(x, matrix, marker='o', linewidth=2, markersize=6)

        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(f'Probability of {class_name}')

        if title is None:
            title = f'Prediction Curve: {class_name}'
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        return fig, ax

    def plot_3d_plotly(self, class_name: str = None, title: str = None,
                       value_filter: tuple = None, opacity: float = 0.8,
                       show_wireframe: bool = False, auto_display: bool = True):
        """
        Create interactive 3D surface plot using Plotly.

        Args:
            class_name: Specific class to plot (default: highest probability class)
            title: Custom title
            value_filter: (min_value, max_value) to filter displayed predictions
            opacity: Surface opacity (0.0-1.0)
            show_wireframe: Show wireframe overlay
            auto_display: Auto-display in Jupyter or return figure

        Returns:
            Plotly figure object
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("3D surface plotting only supports 2D grids")
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")

        try:
            import plotly.graph_objects as go
            import numpy as np
        except ImportError:
            print("Plotly not installed. Install with: pip install plotly")
            print("Falling back to matplotlib...")
            return self.plot_3d(class_name=class_name, title=title,
                               value_filter=value_filter, opacity=opacity,
                               show_wireframe=show_wireframe)

        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet.")

        if class_name is None:
            class_name = self._best_class()

        matrix = self._prediction_matrix[class_name].copy()

        if value_filter is not None:
            min_val, max_val = value_filter
            matrix[matrix < min_val] = np.nan
            matrix[matrix > max_val] = np.nan

        x_vals = self._axis_values[0] if self._axis_values[0] else list(range(matrix.shape[0]))
        y_vals = self._axis_values[1] if self._axis_values[1] else list(range(matrix.shape[1]))

        fig = go.Figure()

        surface = go.Surface(
            x=x_vals, y=y_vals, z=matrix,
            colorscale=self._colormap, opacity=opacity,
            name=f'{class_name} Surface',
            hovertemplate=(
                f"<b>{self._axis_labels[0]}</b>: %{{x}}<br>"
                f"<b>{self._axis_labels[1]}</b>: %{{y}}<br>"
                f"<b>{class_name}</b>: %{{z:.4f}}<br>"
                "<extra></extra>"
            )
        )
        fig.add_trace(surface)

        if show_wireframe:
            x_grid, y_grid = np.meshgrid(range(len(x_vals)), range(len(y_vals)), indexing='ij')
            x_flat = x_grid.flatten()
            y_flat = y_grid.flatten()
            z_flat = matrix.flatten()
            valid_mask = ~np.isnan(z_flat)
            x_valid = [x_vals[i] for i in x_flat[valid_mask]]
            y_valid = [y_vals[i] for i in y_flat[valid_mask]]
            z_valid = z_flat[valid_mask]

            wireframe = go.Scatter3d(
                x=x_valid, y=y_valid, z=z_valid,
                mode='markers',
                marker=dict(size=2, color='black', opacity=0.4),
                name='Wireframe Points', hoverinfo='skip'
            )
            fig.add_trace(wireframe)

        if title is None:
            title = f'Interactive 3D Prediction Surface: {class_name}'
            if value_filter:
                title += f' (filtered: {value_filter[0]:.3f}-{value_filter[1]:.3f})'

        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            scene=dict(
                xaxis_title=self._axis_labels[0],
                yaxis_title=self._axis_labels[1],
                zaxis_title=f'Probability of {class_name}',
                bgcolor='rgb(240, 240, 240)',
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2))
            ),
            width=800, height=600,
            margin=dict(l=0, r=0, t=40, b=0)
        )

        if auto_display:
            try:
                from IPython.display import display, HTML  # noqa: F401
                fig.show()
            except ImportError:
                pass

        return fig
