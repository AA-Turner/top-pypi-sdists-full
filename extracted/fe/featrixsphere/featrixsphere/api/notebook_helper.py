#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
FeatrixNotebookHelper for Jupyter notebook visualization.

Provides visualization methods for training metrics, embedding spaces,
and model analysis in Jupyter notebooks.
"""

import logging
from typing import Dict, Any, Optional, List, Union, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .foundational_model import FoundationalModel
    from .predictor import Predictor
    from .http_client import ClientContext
    import matplotlib
    import plotly
    import numpy as np

logger = logging.getLogger(__name__)


def _training_curves(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a ``GET /session/<id>/training_metrics`` response into
    per-epoch series.

    The route returns one of two shapes:
      - ES timeline: ``{"source": "embedding_space_training", "data":
        {"epochs", "train_loss", "val_loss", "learning_rate", "gradient_norm", ...}}``
      - SP metrics: ``{"training_metrics": {"training_info": [{"epoch_idx",
        "loss", "validation_loss", "hyperparameters": {"learning_rate"},
        "metrics": {"accuracy", "auc", ...}}, ...], "final_metrics": {...}}}``

    Returns ``{"source", "epochs", "train_loss", "val_loss", "learning_rate",
    "gradient_norm", "accuracy", "auc", "final_metrics"}`` (lists hold None
    where an epoch did not record a value). Raises ValueError on any other
    shape rather than plotting an empty chart.
    """
    if 'data' in metrics and metrics.get('source') == 'embedding_space_training':
        data = metrics.get('data') or {}
        epochs = list(data.get('epochs') or [])
        return {
            'source': 'embedding_space',
            'epochs': epochs,
            'train_loss': list(data.get('train_loss') or []),
            'val_loss': list(data.get('val_loss') or []),
            'learning_rate': list(data.get('learning_rate') or []),
            'gradient_norm': list(data.get('gradient_norm') or []),
            'accuracy': [],
            'auc': [],
            'final_metrics': {},
        }
    if 'training_metrics' in metrics:
        tm = metrics.get('training_metrics') or {}
        # Per-epoch rows carry epoch_idx; the trailing best-checkpoint summary
        # row (best_epoch/best_value/...) does not.
        rows = [r for r in (tm.get('training_info') or [])
                if isinstance(r, dict) and 'epoch_idx' in r]
        epoch_metrics = [r.get('metrics') or {} for r in rows]
        return {
            'source': 'single_predictor',
            'epochs': [r['epoch_idx'] + 1 for r in rows],
            'train_loss': [r.get('loss') for r in rows],
            'val_loss': [r.get('validation_loss') for r in rows],
            'learning_rate': [(r.get('hyperparameters') or {}).get('learning_rate') for r in rows],
            'gradient_norm': [],
            'accuracy': [m.get('accuracy') for m in epoch_metrics],
            'auc': [m.get('roc_auc') or m.get('auc') for m in epoch_metrics],
            'final_metrics': tm.get('final_metrics') or {},
        }
    raise ValueError(
        "Unrecognized training_metrics response (expected 'source'/'data' for an "
        f"embedding space or 'training_metrics' for a predictor); got keys {sorted(metrics)}"
    )


def _present(epochs: List[Any], values: List[Any]) -> Tuple[List[Any], List[float]]:
    """(epochs, values) pairs with the None values dropped."""
    pairs = [(e, v) for e, v in zip(epochs, values) if v is not None]
    return [e for e, _ in pairs], [float(v) for _, v in pairs]


def _model_training_curves(model: Any) -> Dict[str, Any]:
    metrics = model.get_training_metrics() if hasattr(model, 'get_training_metrics') else model.get_metrics()
    return _training_curves(metrics)


class FeatrixNotebookHelper:
    """
    Helper class for Jupyter notebook visualization.

    Access via featrix.get_notebook() - no separate import needed!

    Usage:
        notebook = featrix.get_notebook()

        # Visualize training
        fig = notebook.training_loss(fm, style='notebook')
        fig.show()

        # 3D embedding space
        fig = notebook.embedding_space_3d(fm, interactive=True)
        fig.show()

        # Training movie
        movie = notebook.training_movie(fm, notebook_mode=True)
    """

    def __init__(self, ctx: Optional['ClientContext'] = None):
        """Initialize notebook helper with client context."""
        self._ctx = ctx

    def training_loss(
        self,
        model: Union['FoundationalModel', 'Predictor'],
        style: str = 'notebook',
        show_learning_rate: bool = True,
        smooth: bool = True,
        figsize: Tuple[int, int] = (12, 6)
    ) -> Any:
        """
        Plot training loss curves.

        Args:
            model: FoundationalModel or Predictor to visualize
            style: Plot style ('notebook', 'paper', 'presentation')
            show_learning_rate: Show learning rate on secondary axis
            smooth: Apply smoothing to loss curves
            figsize: Figure size (width, height)

        Returns:
            matplotlib Figure

        Example:
            fig = notebook.training_loss(fm, style='notebook')
            fig.show()
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib is required for training_loss visualization")

        curves = _model_training_curves(model)

        # Apply style
        if style == 'notebook':
            plt.style.use('seaborn-v0_8-whitegrid')
        elif style == 'paper':
            plt.style.use('seaborn-v0_8-paper')
        elif style == 'presentation':
            plt.style.use('seaborn-v0_8-talk')

        fig, ax1 = plt.subplots(figsize=figsize)

        # Get loss history
        epochs, loss_history = _present(curves['epochs'], curves['train_loss'])

        # Apply smoothing if requested
        if smooth and len(loss_history) > 10:
            window = min(10, len(loss_history) // 5)
            loss_smoothed = np.convolve(loss_history, np.ones(window)/window, mode='valid')
            epochs_smoothed = epochs[window-1:]
            ax1.plot(epochs, loss_history, alpha=0.3, color='blue', label='Loss (raw)')
            ax1.plot(epochs_smoothed, loss_smoothed, color='blue', linewidth=2, label='Loss (smoothed)')
        else:
            ax1.plot(epochs, loss_history, color='blue', linewidth=2, label='Loss')

        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Show learning rate if available and requested
        if show_learning_rate:
            lr_epochs, lr_history = _present(curves['epochs'], curves['learning_rate'])
            if lr_history:
                ax2 = ax1.twinx()
                ax2.plot(lr_epochs, lr_history, color='red', linestyle='--', label='Learning Rate')
                ax2.set_ylabel('Learning Rate', color='red')
                ax2.tick_params(axis='y', labelcolor='red')
                ax2.set_yscale('log')

        # Title
        model_type = 'FM' if hasattr(model, 'dimensions') else 'Predictor'
        model_id = getattr(model, 'id', 'unknown')[:8]
        ax1.set_title(f'{model_type} Training Loss ({model_id}...)')

        fig.tight_layout()
        return fig

    def embedding_space_3d(
        self,
        fm: 'FoundationalModel',
        sample_size: int = 2000,
        interactive: bool = True,
        color_by: Optional[str] = None,
        figsize: Tuple[int, int] = (800, 600)
    ) -> Any:
        """
        Create 3D visualization of embedding space.

        Args:
            fm: FoundationalModel to visualize
            sample_size: Number of points to sample
            interactive: Use interactive plotly (True) or static matplotlib (False)
            color_by: Column name to color points by
            figsize: Figure size (width, height) for plotly

        Returns:
            plotly Figure (if interactive=True) or matplotlib Figure

        Example:
            fig = notebook.embedding_space_3d(fm, interactive=True)
            fig.show()
        """
        # Server shape: {"projections": {"coords": [{"x", "y", "z", "cluster_pre",
        # "set_columns", "scalar_columns", "string_columns", ...}, ...], ...}}
        response = fm.get_projections(limit=sample_size)
        coords = (response.get('projections') or {}).get('coords') or []
        coords = [c for c in coords if c.get('z') is not None]

        if not coords:
            raise ValueError("No 3D projection data available")

        points_3d = [(c['x'], c['y'], c['z']) for c in coords]
        if color_by is None:
            labels = [f"cluster {c.get('cluster_pre')}" for c in coords]
            colors = [c.get('cluster_pre') for c in coords]
        else:
            values = []
            for c in coords:
                value = None
                for group in ('scalar_columns', 'set_columns', 'string_columns'):
                    cols = c.get(group) or {}
                    if color_by in cols:
                        value = cols[color_by]
                        break
                values.append(value)
            if all(v is None for v in values):
                raise ValueError(f"Column {color_by!r} not found in projection coords")
            labels = [f"{color_by}={v}" for v in values]
            if all(isinstance(v, (int, float)) or v is None for v in values):
                colors = values
            else:
                categories = {v: i for i, v in enumerate(sorted({str(v) for v in values}))}
                colors = [categories[str(v)] for v in values]

        if interactive:
            try:
                import plotly.graph_objects as go
            except ImportError:
                raise ImportError("plotly is required for interactive 3D visualization")

            x = [p[0] for p in points_3d[:sample_size]]
            y = [p[1] for p in points_3d[:sample_size]]
            z = [p[2] for p in points_3d[:sample_size]]

            trace = go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers',
                marker=dict(
                    size=3,
                    color=colors[:sample_size] if colors else None,
                    colorscale='Viridis',
                    opacity=0.8
                ),
                text=labels[:sample_size] if labels else None,
                hovertemplate='%{text}<br>(%{x:.2f}, %{y:.2f}, %{z:.2f})<extra></extra>'
            )

            fig = go.Figure(data=[trace])
            fig.update_layout(
                title=f"Embedding Space 3D ({fm.id[:8]}...)",
                width=figsize[0],
                height=figsize[1],
                scene=dict(
                    xaxis_title='PC1',
                    yaxis_title='PC2',
                    zaxis_title='PC3',
                )
            )
            return fig

        else:
            try:
                import matplotlib.pyplot as plt
                from mpl_toolkits.mplot3d import Axes3D
            except ImportError:
                raise ImportError("matplotlib is required for static 3D visualization")

            fig = plt.figure(figsize=(figsize[0]/100, figsize[1]/100))
            ax = fig.add_subplot(111, projection='3d')

            x = [p[0] for p in points_3d[:sample_size]]
            y = [p[1] for p in points_3d[:sample_size]]
            z = [p[2] for p in points_3d[:sample_size]]

            scatter = ax.scatter(x, y, z, c=colors[:sample_size] if colors else None,
                               cmap='viridis', alpha=0.6, s=10)

            ax.set_xlabel('PC1')
            ax.set_ylabel('PC2')
            ax.set_zlabel('PC3')
            ax.set_title(f"Embedding Space 3D ({fm.id[:8]}...)")

            if colors:
                plt.colorbar(scatter)

            return fig

    def training_movie(
        self,
        model: Union['FoundationalModel', 'Predictor'],
        notebook_mode: bool = True,
        fps: int = 2,
        figsize: Tuple[int, int] = (10, 6)
    ) -> Any:
        """
        Create animated training movie.

        Shows how the model evolves during training, visualizing
        loss curves and optionally embedding space evolution.

        Args:
            model: FoundationalModel or Predictor to visualize
            notebook_mode: True for Jupyter widget, False for animation
            fps: Frames per second
            figsize: Figure size

        Returns:
            ipywidgets Widget (if notebook_mode) or matplotlib animation

        Example:
            movie = notebook.training_movie(fm, notebook_mode=True)
            # Widget displays automatically in Jupyter
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib is required for training_movie")

        curves = _model_training_curves(model)
        _, loss_history = _present(curves['epochs'], curves['train_loss'])

        if not loss_history:
            raise ValueError("No training history available")

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0, len(loss_history))
        ax.set_ylim(0, max(loss_history) * 1.1)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training Progress')

        line, = ax.plot([], [], 'b-', linewidth=2)
        epoch_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                            fontsize=12, verticalalignment='top')

        def init():
            line.set_data([], [])
            epoch_text.set_text('')
            return line, epoch_text

        def animate(frame):
            x = list(range(frame + 1))
            y = loss_history[:frame + 1]
            line.set_data(x, y)
            epoch_text.set_text(f'Epoch: {frame + 1}/{len(loss_history)}')
            return line, epoch_text

        anim = animation.FuncAnimation(
            fig, animate, init_func=init,
            frames=len(loss_history), interval=1000//fps,
            blit=True, repeat=False
        )

        if notebook_mode:
            try:
                from IPython.display import HTML
                plt.close(fig)  # Prevent static display
                return HTML(anim.to_jshtml())
            except ImportError:
                return anim
        else:
            return anim

    def embedding_evolution(
        self,
        fm: 'FoundationalModel',
        epoch_range: Optional[Tuple[int, int]] = None,
        interactive: bool = True,
        sample_size: int = 500
    ) -> Any:
        """
        Visualize embedding evolution over epochs.

        Shows how the embedding space changes during training.

        Args:
            fm: FoundationalModel to visualize
            epoch_range: Tuple of (start_epoch, end_epoch) or None for all
            interactive: Use interactive plotly
            sample_size: Number of points to sample

        Returns:
            plotly Figure (if interactive) or matplotlib Figure

        Example:
            fig = notebook.embedding_evolution(fm, epoch_range=(1, 50))
            fig.show()
        """
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("plotly is required for embedding_evolution")

        # Server shape: {"epoch_projections": {"epoch_<n>": {"epoch": n,
        # "coords": [{"x", "y", "z", ...}, ...]}, ...}}
        response = fm.get_epoch_projections(point_limit=sample_size)
        evolution = []
        for key, epoch_data in (response.get('epoch_projections') or {}).items():
            if not key.startswith('epoch_') or not isinstance(epoch_data, dict):
                continue
            epoch = epoch_data.get('epoch')
            if epoch is None:
                continue
            if epoch_range is not None and not (epoch_range[0] <= epoch <= epoch_range[1]):
                continue
            points = [(c['x'], c['y']) for c in (epoch_data.get('coords') or [])
                      if c.get('x') is not None and c.get('y') is not None]
            evolution.append({'epoch': epoch, 'points': points})
        evolution.sort(key=lambda e: e['epoch'])

        if not evolution:
            # Create placeholder figure
            fig = go.Figure()
            fig.add_annotation(
                text="Embedding evolution data not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="Embedding Evolution (data not available)",
                width=800, height=600
            )
            return fig

        # If data is available, create animation
        frames = []
        for epoch_data in evolution:
            epoch = epoch_data.get('epoch', 0)
            points = epoch_data.get('points', [])[:sample_size]

            frame = go.Frame(
                data=[go.Scatter(
                    x=[p[0] for p in points],
                    y=[p[1] for p in points],
                    mode='markers',
                    marker=dict(size=5, opacity=0.6)
                )],
                name=str(epoch)
            )
            frames.append(frame)

        fig = go.Figure(
            data=frames[0].data if frames else [],
            frames=frames,
            layout=go.Layout(
                title="Embedding Evolution",
                updatemenus=[{
                    "type": "buttons",
                    "buttons": [
                        {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 500}}]},
                        {"label": "Pause", "method": "animate", "args": [[None], {"mode": "immediate"}]}
                    ]
                }],
                sliders=[{
                    "steps": [{"args": [[str(e['epoch'])], {"frame": {"duration": 0}}], "label": str(e['epoch'])}
                             for e in evolution],
                    "currentvalue": {"prefix": "Epoch: "}
                }]
            )
        )

        return fig

    def training_comparison(
        self,
        models: List[Union['FoundationalModel', 'Predictor']],
        labels: Optional[List[str]] = None,
        figsize: Tuple[int, int] = (12, 6)
    ) -> Any:
        """
        Compare training across multiple models.

        Args:
            models: List of models to compare
            labels: Optional labels for each model
            figsize: Figure size

        Returns:
            matplotlib Figure

        Example:
            fig = notebook.training_comparison([fm1, fm2], labels=['v1', 'v2'])
            fig.show()
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib is required for training_comparison")

        fig, ax = plt.subplots(figsize=figsize)

        colors = plt.cm.tab10(np.linspace(0, 1, len(models)))

        for i, model in enumerate(models):
            curves = _model_training_curves(model)
            epochs, loss_history = _present(curves['epochs'], curves['train_loss'])

            label = labels[i] if labels and i < len(labels) else f"Model {i+1}"
            ax.plot(epochs, loss_history, color=colors[i], linewidth=2, label=label)

        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig

    def embedding_space_training(
        self,
        fm: 'FoundationalModel',
        style: str = 'notebook',
        figsize: Tuple[int, int] = (14, 6)
    ) -> Any:
        """
        Plot embedding space training metrics.

        Shows detailed metrics specific to foundational model training.

        Args:
            fm: FoundationalModel to visualize
            style: Plot style
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib is required")

        curves = _training_curves(fm.get_training_metrics())

        fig, axes = plt.subplots(1, 3, figsize=figsize)

        # Loss curve
        loss_epochs, loss = _present(curves['epochs'], curves['train_loss'])
        if loss:
            axes[0].plot(loss_epochs, loss, 'b-', linewidth=2)
            axes[0].set_title('Training Loss')
            axes[0].set_xlabel('Epoch')
            axes[0].set_ylabel('Loss')
            axes[0].grid(True, alpha=0.3)

        # Learning rate
        lr_epochs, lr = _present(curves['epochs'], curves['learning_rate'])
        if lr:
            axes[1].semilogy(lr_epochs, lr, 'r-', linewidth=2)
            axes[1].set_title('Learning Rate')
            axes[1].set_xlabel('Epoch')
            axes[1].set_ylabel('LR')
            axes[1].grid(True, alpha=0.3)

        # Gradient norm if available
        gn_epochs, grad_norm = _present(curves['epochs'], curves['gradient_norm'])
        if grad_norm:
            axes[2].plot(gn_epochs, grad_norm, 'g-', linewidth=2)
            axes[2].set_title('Gradient Norm')
            axes[2].set_xlabel('Epoch')
            axes[2].set_ylabel('Norm')
            axes[2].grid(True, alpha=0.3)
        else:
            axes[2].text(0.5, 0.5, 'No gradient data', ha='center', va='center')
            axes[2].set_title('Gradient Norm')

        fig.suptitle(f'Embedding Space Training ({fm.id[:8]}...)', fontsize=14)
        fig.tight_layout()
        return fig

    def single_predictor_training(
        self,
        predictor: 'Predictor',
        style: str = 'notebook',
        figsize: Tuple[int, int] = (14, 6)
    ) -> Any:
        """
        Plot single predictor training metrics.

        Shows detailed metrics specific to predictor training including
        accuracy, AUC, and confusion matrix evolution.

        Args:
            predictor: Predictor to visualize
            style: Plot style
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib is required")

        curves = _training_curves(predictor.get_metrics())
        final_metrics = curves['final_metrics']

        fig, axes = plt.subplots(1, 3, figsize=figsize)

        # Loss curve
        loss_epochs, loss = _present(curves['epochs'], curves['train_loss'])
        if loss:
            axes[0].plot(loss_epochs, loss, 'b-', linewidth=2)
            axes[0].set_title('Training Loss')
            axes[0].set_xlabel('Epoch')
            axes[0].set_ylabel('Loss')
            axes[0].grid(True, alpha=0.3)

        # Accuracy
        acc_epochs, accuracy = _present(curves['epochs'], curves['accuracy'])
        if accuracy:
            axes[1].plot(acc_epochs, accuracy, 'g-', linewidth=2)
            axes[1].set_title('Accuracy')
            axes[1].set_xlabel('Epoch')
            axes[1].set_ylabel('Accuracy')
            axes[1].set_ylim(0, 1)
            axes[1].grid(True, alpha=0.3)
        else:
            final_acc = final_metrics.get('accuracy', predictor.accuracy)
            if final_acc:
                axes[1].axhline(y=final_acc, color='g', linewidth=2)
                axes[1].set_title(f'Final Accuracy: {final_acc:.4f}')
            else:
                axes[1].text(0.5, 0.5, 'No accuracy data', ha='center', va='center')
                axes[1].set_title('Accuracy')

        # AUC
        auc_epochs, auc_history = _present(curves['epochs'], curves['auc'])
        if auc_history:
            axes[2].plot(auc_epochs, auc_history, 'r-', linewidth=2)
            axes[2].set_title('AUC')
            axes[2].set_xlabel('Epoch')
            axes[2].set_ylabel('AUC')
            axes[2].set_ylim(0, 1)
            axes[2].grid(True, alpha=0.3)
        else:
            final_auc = final_metrics.get('roc_auc') or final_metrics.get('auc') or predictor.auc
            if final_auc:
                axes[2].axhline(y=final_auc, color='r', linewidth=2)
                axes[2].set_title(f'Final AUC: {final_auc:.4f}')
            else:
                axes[2].text(0.5, 0.5, 'No AUC data', ha='center', va='center')
                axes[2].set_title('AUC')

        fig.suptitle(f'Predictor Training ({predictor.target_column})', fontsize=14)
        fig.tight_layout()
        return fig
