import json
import numpy as np
import os
import traceback
def read_benchmark_results(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def analyze_benchmark_results(file_path, base_result_dir, first_sentence_len=50):
    """
    Analyze benchmark results by creating a pandas DataFrame and generating both static PNG plots and interactive HTML dashboard.
    
    Args:
        file_path: Path to benchmark results file or directory
        base_result_dir: Directory to save analysis results
    """
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        print("Missing optional dependencies for analysis: pandas, matplotlib, numpy")
        print("Install them with: pip install pandas matplotlib numpy")
        return
    
    try:
        # Check if file_path is a directory or a single file
        all_results = []
        if os.path.isdir(file_path):
            # Process all JSON files in the directory
            print(f"Processing all JSON files in the directory: {file_path}")
            json_files = [f for f in os.listdir(file_path) if f.endswith('.json')]
            for json_file in json_files:
                full_path = os.path.join(file_path, json_file)
                file_results = read_benchmark_results(full_path)
                # Add filename as a column (without .json extension)
                file_name = os.path.basename(json_file).replace('.json', '')
                for result in file_results:
                    result['file_name'] = file_name
                all_results.extend(file_results)
        else:
            # Process a single file
            file_results = read_benchmark_results(file_path)
            file_name = os.path.basename(file_path).replace('.json', '')
            for result in file_results:
                result['file_name'] = file_name
            all_results.extend(file_results)
            
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(all_results)
        # extra_info_columns = [col for col in df.columns if not isinstance(df[col].iloc[0], list) and df[col].nunique() == 1]
        # extra_info_columns = []
        # df_extra_info = df[extra_info_columns]
        is_random_data_set = "random_input_len" in df.columns

        # Recalculate request_throughput and output_throughput based on tensor_parallel_size
        if 'tensor_parallel_size' in df.columns and 'request_throughput' in df.columns:
            # Convert tensor_parallel_size to numeric type to avoid TypeError
            df['tensor_parallel_size'] = pd.to_numeric(df['tensor_parallel_size'])
            df['request_throughput'] = df['request_throughput'] * 8 / df['tensor_parallel_size']
        
        if 'tensor_parallel_size' in df.columns and 'output_throughput' in df.columns:
            # Ensure tensor_parallel_size is numeric
            if not pd.api.types.is_numeric_dtype(df['tensor_parallel_size']):
                df['tensor_parallel_size'] = pd.to_numeric(df['tensor_parallel_size'])
            df['output_throughput'] = df['output_throughput'] * 8 / df['tensor_parallel_size']

        grid_search_columns = ["enable_chunked_prefill",
                               "enable_prefix_caching",
                               "use-v2-block-manager",
                               "multi-step-stream-outputs",
                               "tensor_parallel_size",
                               "speculative-draft-tensor-parallel-size",
                               "num-speculative-tokens"]
        if is_random_data_set:
            grid_search_columns.append("random_prefix_len")
        
        select_columns = ["request_throughput",
                          "output_throughput", 
                          "mean_output_token_len",
                          "p90_output_token_len",
                          "mean_input_token_len",
                          "p90_input_token_len",
                          "max_concurrency", 
                          "mean_ttfs_ms",
                          "std_ttfs_ms",
                          "p90_ttfs_ms",
                          "mean_tpot_ms",
                          "std_tpot_ms",
                          "p90_tpot_ms",
                          "mean_ttft_ms",
                          "std_ttft_ms",
                          "p90_ttft_ms",
                          "mean_e2el_ms",
                          "std_e2el_ms",
                          "p90_e2el_ms",
                          "mean_fs_token_len",
                          "std_fs_token_len",
                          "p90_fs_token_len",
         ]

        if 'file_name' in df.columns:
            select_columns = ["file_name"] + select_columns

        if is_random_data_set:
            recalculate_ttfs(df, first_sentence_len=first_sentence_len)
        
        # Filter out columns that have only a single unique value
        all_selected_columns = grid_search_columns + select_columns
        df = df[df['request_throughput'] != 0]  
        df = df[df['tensor_parallel_size'] == 4]
        # df.sort_values(by='request_throughput', ascending=False, inplace=True)


        filtered_columns = []
        for col in all_selected_columns:
            if col in df.columns:
                if df[col].nunique() > 1 or len(df) == 1:
                    filtered_columns.append(col)
        df = df[filtered_columns]
        
        # Keep actual mean_output_token_len values instead of hardcoding to 100
        if 'mean_output_token_len' in df.columns:
            df['mean_output_token_len'] = pd.to_numeric(df['mean_output_token_len'], errors='coerce')
            df['mean_output_token_len'] = df['mean_output_token_len'].round(0).astype(int)
        
        if 'mean_input_token_len' in df.columns:
            df['mean_input_token_len'] = pd.to_numeric(df['mean_input_token_len'], errors='coerce')
            df['mean_input_token_len'] = df['mean_input_token_len'].round(0).astype(int)
        
        df.to_csv(os.path.join(base_result_dir, "benchmark_results.csv"), index=False)
        print(f"Data frame of Benchmark results saved to {os.path.join(base_result_dir, 'benchmark_results.csv')}")
        
        # Rename columns
        renamed_grid_search_columns = {
            "enable_chunked_prefill": "chunkfill",
            "enable_prefix_caching": "precache",
            "tensor_parallel_size": "TP",
            "file_name": "file",
            "speculative-draft-tensor-parallel-size": "sp_tp",
            "num-speculative-tokens": "k",
        }
        
        if is_random_data_set:
            renamed_grid_search_columns["random_prefix_len"] = "prefix_len"
            renamed_grid_search_columns["mean_input_token_len"] = "input_len"
            renamed_grid_search_columns["mean_output_token_len"] = "output_len"
            
        df.rename(columns=renamed_grid_search_columns, inplace=True)
        
        # Create configuration ID for grouping
        config_columns = [col for col in renamed_grid_search_columns.values() if col in df.columns]
        df['config_id'] = df.apply(lambda row: '_'.join([f"{col}_{row[col]}" for col in config_columns]), axis=1)
        
        # Get unique configuration IDs
        config_ids = df['config_id'].unique()
        
        # Create groups based on configuration
        groups = []
        for config_id in config_ids:
            group_df = df[df['config_id'] == config_id]
            if not group_df.empty:
                groups.append((config_id, group_df))
        
        # Use different colors for different configurations
        colors = plt.cm.viridis(np.linspace(0, 1, len(groups)))
        
        # Define metrics to plot
        mean_metrics = [
            ('mean_ttft_ms', 'Mean TTFT (ms)'),
            ('mean_tpot_ms', 'Mean TPOT (ms)'),
            ('mean_ttfs_ms', 'Mean TTFS (ms)'),
            ('mean_e2el_ms', 'Mean E2EL (ms)')
        ]
        
        p90_metrics = [
            ('p90_ttft_ms', 'P90 TTFT (ms)'),
            ('p90_tpot_ms', 'P90 TPOT (ms)'),
            ('p90_ttfs_ms', 'P90 TTFS (ms)'),
            ('p90_e2el_ms', 'P90 E2EL (ms)')
        ]
        
        # Function to create matplotlib plots with given x-axis
        def create_performance_plots(y_axis, y_label, filename, swap_axes=False):
            # default x-axis is max_concurrency
            fig, axes = plt.subplots(2, 4, figsize=(20, 10))
            
            # Flatten axes for easier iteration
            axes = axes.flatten()
            
            # Helper function to create a plot for a metric
            def plot_metric(ax, metric, metric_label, y_axis_name, groups_data, swap_axes=swap_axes):
                # Define different marker styles for different configurations
                markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', '|']
                
                for j, (config_id, group) in enumerate(groups_data):
                    # Use different marker styles based on configuration
                    marker_idx = j % len(markers)
                    marker_style = markers[marker_idx]
                    
                    if swap_axes:
                        ax.scatter(group[y_axis], group[metric],
                                  label=config_id, 
                                  color=colors[j], marker=marker_style, s=70)
                        ax.plot(group[y_axis], group[metric],
                               color=colors[j], linestyle='-')
                        ax.set_xlabel(y_label)
                        ax.set_ylabel(metric_label)
                        ax.set_title(f'{y_label} vs {metric_label}')
                    else:
                        ax.scatter(group[metric], group[y_axis],
                                  label=config_id, 
                                  color=colors[j], marker=marker_style, s=70)
                        ax.plot(group[metric], group[y_axis],
                               color=colors[j], linestyle='-')
                        ax.set_ylabel(y_label)
                        ax.set_xlabel(metric_label)
                        ax.set_title(f'{metric_label} vs {y_label}')
                ax.grid(True)
                
                # Only add legend to the first graph (index 0)
                if ax == axes[0]:
                    ax.legend(fontsize='x-small', loc='upper right', frameon=True)
            
            # Plot mean metrics (first row)
            for i, (metric, ylabel) in enumerate(mean_metrics):
                plot_metric(axes[i], metric, ylabel, y_label, groups, swap_axes=swap_axes)
            
            # Plot p90 metrics (second row)
            for i, (metric, ylabel) in enumerate(p90_metrics):
                plot_metric(axes[i+4], metric, ylabel, y_label, groups, swap_axes=swap_axes)
            
            plt.tight_layout()
            plt.savefig(os.path.join(base_result_dir, filename))
            plt.close()
            
        # Create matplotlib plots
        create_performance_plots('max_concurrency', 'Concurrency', 'concurrency_analysis.png', swap_axes=True)
        create_performance_plots('request_throughput', 'Request Throughput', 'throughput_analysis.png')
        create_interactive_dashboard(df, base_result_dir)
        
    except ImportError as e:
        print(f"Could not analyze results: {e}")
        print("To enable analysis, install required packages: pip install pandas matplotlib plotly")
    except Exception as e:
        print(f"Error analyzing benchmark results: {e}")
        print(traceback.format_exc())
        print(traceback.format_exc())

def create_interactive_dashboard(df, base_result_dir):
    """
    Create an interactive HTML dashboard with Plotly and dropdown filters.
    """
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.offline as pyo
    except ImportError:
        print("Plotly not available, skipping interactive dashboard creation")
        return
        
    # Create plots directory
    plot_dir = os.path.join(base_result_dir)
    
    # Convert DataFrame to JSON for JavaScript
    data_json = df.to_json(orient='records')
    
    # Get configuration columns (exclude metric columns)
    metric_columns = ['request_throughput', 'output_throughput', 'mean_ttft_ms', 'mean_tpot_ms', 
                      'mean_e2el_ms', 'mean_ttfs_ms', 'std_ttft_ms', 'std_tpot_ms', 'std_e2el_ms', 
                      'std_ttfs_ms', 'p90_ttft_ms', 'p90_tpot_ms', 'p90_e2el_ms', 'p90_ttfs_ms', 
                      'mean_fs_token_len', 'std_fs_token_len', 'p90_fs_token_len', 'max_concurrency',
                      'p90_input_token_len', 'config_id']
    config_columns = [col for col in df.columns if col not in metric_columns]
    
    # Get unique values for filters
    filter_options = {}
    for col in config_columns:
        unique_vals = sorted(df[col].unique())
        filter_options[col] = unique_vals
    
    # Define metrics to plot - Updated to include TTFS and remove request_throughput vs request_throughput
    metrics = [
        ['mean_ttft_ms', 'Mean TTFT (ms)'],
        ['mean_tpot_ms', 'Mean TPOT (ms)'],
        ['mean_ttfs_ms', 'Mean TTFS (ms)'],
        ['mean_e2el_ms', 'Mean E2E Latency (ms)']
    ]
    
    p90_metrics = [
        ['p90_ttft_ms', 'P90 TTFT (ms)'],
        ['p90_tpot_ms', 'P90 TPOT (ms)'],
        ['p90_ttfs_ms', 'P90 TTFS (ms)'],
        ['p90_e2el_ms', 'P90 E2E Latency (ms)']
    ]

    # Generate filter controls HTML
    filter_controls_html = ""
    for col, values in filter_options.items():
        filter_controls_html += f"""
            <div class="filter-group">
                <label for="{col}_filter">{col.replace('_', ' ').title()}:</label>
                <select id="{col}_filter" onchange="updatePlots()">
                    <option value="all">All</option>
                    {''.join([f'<option value="{val}">{val}</option>' for val in values])}
                </select>
            </div>
"""

    # Generate unique values summary HTML
    unique_values_html = ""
    for col, values in filter_options.items():
        values_str = ", ".join([str(val) for val in values])
        unique_values_html += f"""
            <tr>
                <td class="column-name">{col.replace('_', ' ').title()}</td>
                <td class="unique-count">{len(values)}</td>
                <td class="values-list">{values_str}</td>
            </tr>
"""

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Benchmark Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .title {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .filter-group label {{
            font-weight: bold;
            color: #555;
        }}
        .filter-group select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }}
        .unique-values-section {{
            margin-bottom: 30px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }}
        .unique-values-section h3 {{
            margin-top: 0;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }}
        .unique-values-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        .unique-values-table th {{
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
            font-weight: bold;
            color: #495057;
        }}
        .unique-values-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }}
        .unique-values-table tr:hover {{
            background-color: #f8f9fa;
        }}
        .column-name {{
            font-weight: bold;
            color: #495057;
            min-width: 150px;
        }}
        .unique-count {{
            text-align: center;
            font-weight: bold;
            color: #007bff;
            min-width: 80px;
        }}
        .values-list {{
            word-wrap: break-word;
            max-width: 600px;
        }}
        .axis-controls {{
            margin-bottom: 20px;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 8px;
        }}
        .axis-controls label {{
            font-weight: bold;
            margin-right: 10px;
        }}
        .axis-controls select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }}
        .plots-container {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}
        .plot-section {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }}
        .plot-section h3 {{
            margin-top: 0;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }}
        .plot-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        .plot-item {{
            min-height: 400px;
            border: 1px solid #eee;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">Interactive Benchmark Results Dashboard</h1>
        
        <div class="unique-values-section">
            <h3>Dataset Configuration Summary</h3>
            <table class="unique-values-table">
                <thead>
                    <tr>
                        <th>Configuration Parameter</th>
                        <th>Unique Values Count</th>
                        <th>Available Values</th>
                    </tr>
                </thead>
                <tbody>
                    {unique_values_html}
                </tbody>
            </table>
        </div>
        
        <div class="controls">
            {filter_controls_html}
        </div>
        
        <div class="axis-controls">
            <label for="x_axis_select">Chart Type:</label>
            <select id="x_axis_select" onchange="updatePlots()">
                <option value="max_concurrency">Metrics vs Concurrency</option>
                <option value="request_throughput">Throughput vs Metrics</option>
            </select>
        </div>
        
        <div class="plots-container">
            <div class="plot-section">
                <h3>Mean Metrics vs X-Axis</h3>
                <div class="plot-grid">
                    <div id="mean_plot_0" class="plot-item"></div>
                    <div id="mean_plot_1" class="plot-item"></div>
                    <div id="mean_plot_2" class="plot-item"></div>
                    <div id="mean_plot_3" class="plot-item"></div>
                </div>
            </div>
            
            <div class="plot-section">
                <h3>P90 Metrics vs X-Axis</h3>
                <div class="plot-grid">
                    <div id="p90_plot_0" class="plot-item"></div>
                    <div id="p90_plot_1" class="plot-item"></div>
                    <div id="p90_plot_2" class="plot-item"></div>
                    <div id="p90_plot_3" class="plot-item"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Data from Python
        const rawData = {data_json};
        
        // Metrics definitions
        const metrics = {json.dumps(metrics)};
        const p90_metrics = {json.dumps(p90_metrics)};
        const configColumns = {json.dumps(config_columns)};
        
        // Global variable to track legend visibility state
        let legendVisibility = {{}};
        
        // Dynamically detect configuration columns (excluding metric columns)
        const metricColumns = ['request_throughput', 'output_throughput', 'mean_ttft_ms', 'mean_tpot_ms', 
                              'mean_e2el_ms', 'mean_ttfs_ms', 'std_ttft_ms', 'std_tpot_ms', 'std_e2el_ms', 
                              'std_ttfs_ms', 'p90_ttft_ms', 'p90_tpot_ms', 'p90_e2el_ms', 'p90_ttfs_ms', 
                              'mean_fs_token_len', 'std_fs_token_len', 'p90_fs_token_len', 'max_concurrency',
                              'p90_input_token_len', 'config_id'];
        
        function getConfigColumns() {{
            if (rawData.length === 0) return [];
            const allColumns = Object.keys(rawData[0]);
            return allColumns.filter(col => !metricColumns.includes(col));
        }}
        
        function filterData() {{
            let filteredData = rawData.slice();
            
            // Apply filters dynamically based on available config columns
            configColumns.forEach(col => {{
                const filterElement = document.getElementById(col + '_filter');
                if (filterElement) {{
                    const filterValue = filterElement.value;
                    if (filterValue !== 'all') {{
                        filteredData = filteredData.filter(row => row[col].toString() === filterValue);
                    }}
                }}
            }});
            
            return filteredData;
        }}
        
        function createTrace(data, xAxis, yMetric) {{
            const groups = {{}};
            const configColumns = getConfigColumns();
            
            data.forEach(row => {{
                // Create a flexible key based on available config columns
                const keyParts = configColumns.map(col => {{
                    if (row[col] !== undefined && row[col] !== null) {{
                        return `${{col}}:${{row[col]}}`;
                    }}
                    return null;
                }}).filter(part => part !== null);
                
                const key = keyParts.join(' | ');
                
                if (!groups[key]) {{
                    // Check if this trace should be visible based on global state
                    const visible = legendVisibility[key] !== false;
                    
                    groups[key] = {{
                        x: [],
                        y: [],
                        text: [],
                        name: key,
                        type: 'scatter',
                        mode: 'markers+lines',
                        visible: visible,
                        hovertemplate: '<b>%{{text}}</b><br>' +
                                     'X: %{{x}}<br>' +
                                     'Y: %{{y}}<br>' +
                                     '<extra></extra>',
                        hoverlabel: {{
                            bgcolor: 'white',
                            bordercolor: 'black',
                            font: {{size: 12}},
                            namelength: -1
                        }}
                    }};
                }}
                groups[key].x.push(row[xAxis]);
                groups[key].y.push(row[yMetric]);
                groups[key].text.push(key); // Add the full key as hover text for each point
            }});
            
            return Object.values(groups);
        }}
        
        function setupLegendClickHandler(plotId) {{
            document.getElementById(plotId).on('plotly_legendclick', function(data) {{
                const traceName = data.data[data.curveNumber].name;
                
                // Toggle visibility state
                legendVisibility[traceName] = !legendVisibility[traceName];
                
                // Update all plots with new visibility
                updateAllPlotsVisibility();
                
                // Prevent default legend behavior
                return false;
            }});
        }}
        
        function updateAllPlotsVisibility() {{
            const allPlotIds = [
                'mean_plot_0', 'mean_plot_1', 'mean_plot_2', 'mean_plot_3',
                'p90_plot_0', 'p90_plot_1', 'p90_plot_2', 'p90_plot_3'
            ];
            
            allPlotIds.forEach(plotId => {{
                const plotDiv = document.getElementById(plotId);
                if (plotDiv && plotDiv.data) {{
                    const updates = {{}};
                    plotDiv.data.forEach((trace, index) => {{
                        const visible = legendVisibility[trace.name] !== false;
                        updates[`visible[${{index}}]`] = visible;
                    }});
                    
                    Plotly.restyle(plotId, updates);
                }}
            }});
        }}
        
        function updatePlots() {{
            const filteredData = filterData();
            const xAxis = document.getElementById('x_axis_select').value;
            const swapAxes = xAxis === 'request_throughput';
            
            if (filteredData.length === 0) {{
                console.log('No data after filtering');
                return;
            }}
            
            // Initialize legend visibility for new traces
            const traces = createTrace(filteredData, 'max_concurrency', 'mean_ttft_ms');
            traces.forEach(trace => {{
                if (legendVisibility[trace.name] === undefined) {{
                    legendVisibility[trace.name] = true;
                }}
            }});
            
            // Create mean metric plots
            metrics.forEach((metric, i) => {{
                let traces, layout;
                
                if (swapAxes) {{
                    // When X-axis is "request_throughput", swap so metric is X and throughput is Y
                    traces = createTrace(filteredData, metric[0], 'request_throughput');
                    layout = {{
                        title: `Request Throughput vs ${{metric[1]}}`,
                        xaxis: {{ title: metric[1] }},
                        yaxis: {{ title: 'Request Throughput (req/s)' }},
                        showlegend: i === 0,
                        legend: {{
                            x: 0.5,
                            y: -0.2,
                            xanchor: 'center',
                            yanchor: 'top',
                            orientation: 'h',
                            bgcolor: 'rgba(255,255,255,0.8)',
                            bordercolor: 'rgba(0,0,0,0.2)',
                            borderwidth: 1
                        }},
                        margin: {{ t: 50, r: 50, b: 100, l: 80 }}
                    }};
                }} else {{
                    // Normal case: concurrency is X, metric is Y
                    traces = createTrace(filteredData, xAxis, metric[0]);
                    layout = {{
                        title: `${{metric[1]}} vs Concurrency`,
                        xaxis: {{ title: 'Concurrency' }},
                        yaxis: {{ title: metric[1] }},
                        showlegend: i === 0,
                        legend: {{
                            x: 0.5,
                            y: -0.2,
                            xanchor: 'center',
                            yanchor: 'top',
                            orientation: 'h',
                            bgcolor: 'rgba(255,255,255,0.8)',
                            bordercolor: 'rgba(0,0,0,0.2)',
                            borderwidth: 1
                        }},
                        margin: {{ t: 50, r: 50, b: 100, l: 80 }}
                    }};
                }}
                
                Plotly.newPlot(`mean_plot_${{i}}`, traces, layout, {{responsive: true}}).then(function() {{
                    // Setup legend click handler only for the plot with legend after plot is created
                    if (i === 0) {{
                        document.getElementById(`mean_plot_${{i}}`).on('plotly_legendclick', function(data) {{
                            const traceName = data.data[data.curveNumber].name;
                            
                            // Toggle visibility state
                            if (legendVisibility[traceName] === undefined) {{
                                legendVisibility[traceName] = true;
                            }}
                            legendVisibility[traceName] = !legendVisibility[traceName];
                            
                            // Update all plots with new visibility
                            updateAllPlotsVisibility();
                            
                            // Prevent default legend behavior
                            return false;
                        }});
                    }}
                }});
            }});
            
            // Create P90 metric plots  
            p90_metrics.forEach((metric, i) => {{
                let traces, layout;
                
                if (swapAxes) {{
                    // When X-axis is "request_throughput", swap so metric is X and throughput is Y
                    traces = createTrace(filteredData, metric[0], 'request_throughput');
                    layout = {{
                        title: `Request Throughput vs ${{metric[1]}}`,
                        xaxis: {{ title: metric[1] }},
                        yaxis: {{ title: 'Request Throughput (req/s)' }},
                        showlegend: false,
                        margin: {{ t: 50, r: 50, b: 50, l: 80 }}
                    }};
                }} else {{
                    // Normal case: concurrency is X, metric is Y
                    traces = createTrace(filteredData, xAxis, metric[0]);
                    layout = {{
                        title: `${{metric[1]}} vs Concurrency`,
                        xaxis: {{ title: 'Concurrency' }},
                        yaxis: {{ title: metric[1] }},
                        showlegend: false,
                        margin: {{ t: 50, r: 50, b: 50, l: 80 }}
                    }};
                }}
                
                Plotly.newPlot(`p90_plot_${{i}}`, traces, layout, {{responsive: true}});
            }});
        }}
        
        // Initialize plots when page loads
        document.addEventListener('DOMContentLoaded', function() {{
            updatePlots();
        }});
    </script>
</body>
</html>
"""
    
    # Write HTML file
    html_file = os.path.join(plot_dir, "interactive_benchmark_dashboard.html")
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"Interactive dashboard created: {html_file}")
    return html_file

def recalculate_ttfs(df, first_sentence_len):
    if 'mean_ttfs_ms' in df.columns and 'mean_ttft_ms' in df.columns and 'mean_tpot_ms' in df.columns :
        df['mean_ttfs_ms'] = df['mean_ttft_ms'] + df['mean_tpot_ms'] * first_sentence_len
            
    if 'p90_ttfs_ms' in df.columns and 'p90_ttft_ms' in df.columns and 'p90_tpot_ms' in df.columns :
        df['p90_ttfs_ms'] = df['p90_ttft_ms'] + df['p90_tpot_ms'] * first_sentence_len
            
    if 'std_ttfs_ms' in df.columns and 'std_ttft_ms' in df.columns and 'std_tpot_ms' in df.columns :
            # This is an approximation for std of sum of dependent variables
        df['std_ttfs_ms'] = np.sqrt(df['std_ttft_ms']**2 + (df['std_tpot_ms'] * first_sentence_len)**2)