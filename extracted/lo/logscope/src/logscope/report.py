"""HTML report generation for Logscope."""

import sqlite3
import webbrowser
from typing import List, Dict, Any
import tempfile
import importlib.resources
import datetime

def get_run_ids(db_path: str = 'logscope.db', limit: int = 1) -> List[str]:
    """
    Get the most recent run IDs from the database.
    
    Args:
        db_path: Path to the SQLite database file
        limit: Number of most recent runs to retrieve
        
    Returns:
        List of run IDs ordered by most recent first
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT run FROM logs ORDER BY timestamp DESC")
        runs = cursor.fetchall()
        
    return [run['run'] for run in runs[:limit]]

def get_logs_by_run(db_path: str = 'logscope.db', run_id: str = None) -> List[Dict[str, Any]]:
    """
    Get logs for a specific run ID.
    
    Args:
        db_path: Path to the SQLite database file
        run_id: The run ID to retrieve logs for
        
    Returns:
        List of log entries for the specified run
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if run_id:
            cursor.execute("SELECT * FROM logs WHERE run = ? ORDER BY timestamp ASC", (run_id,))
        else:
            # Get the most recent run if no run_id specified
            cursor.execute("SELECT run FROM logs ORDER BY timestamp DESC LIMIT 1")
            last_run = cursor.fetchone()
            if not last_run:
                return []
            
            cursor.execute("SELECT * FROM logs WHERE run = ? ORDER BY timestamp ASC", (last_run['run'],))
            
        return [dict(row) for row in cursor.fetchall()]

def get_last_run_logs(db_path: str = 'logscope.db') -> List[Dict[str, Any]]:
    """Get logs from the most recent run in the database."""
    return get_logs_by_run(db_path)

def generate_html_report_for_run(logs: List[Dict[str, Any]]) -> str:
    """Generate an HTML report for a single run."""
    if not logs:
        return "<article><h2>No logs found</h2></article>"
    
    html = f"""
        <article>
            <p>Run ID: {logs[0]['run']}</p>
    """

    def trunc(s: str, max_len: int = 50) -> str:
        return s[:max_len] + '...' if len(s) > max_len else s

    last_timestamp = None
    time_diff = 0
    
    for i, log in enumerate(logs):
        timestamp = log['timestamp']
        if last_timestamp is None:
            last_timestamp = timestamp
        else:
            time_diff = (
                datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f') -
                datetime.datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S.%f')
            ).total_seconds()
            last_timestamp = timestamp
        message = log['message']
        short_message = trunc(message.split('\n')[0])
        source = log['source'] or 'N/A'
        function = log['function'] or 'N/A'
        filename = log['filename'] or 'N/A'
        lineno = log['lineno'] or 'N/A'
        event_type = log['event_type'] or 'log'
        
        html += f"""
            <div class="log-entry">
                <div class="entry-label" onclick="toggleDetails('run-{logs[0]['run']}-{i}')">
                    <strong>{short_message}</strong>
                    <span class="time-delta">(+{time_diff}s)</span>
                </div>
                <div class="log-details" id="run-{logs[0]['run']}-{i}">
                    <pre>{message}</pre>
                    <div class="props">
                        <p><strong>Source:</strong> {source}</p>
                        <p><strong>Function:</strong> {function}</p>
                        <p><strong>File:</strong> {filename}:{lineno}</p>
                        <p><strong>Event Type:</strong> {event_type}</p>
                    </div>
                </div>
            </div>
        """
    
    html += """
        </article>
    """
    return html

def generate_html_report(all_runs_logs: List[List[Dict[str, Any]]]) -> str:
    """
    Generate an HTML report from the provided logs for multiple runs.
    
    Args:
        all_runs_logs: List of log lists, where each inner list contains logs for one run
        
    Returns:
        HTML string containing the report
    """
    if not all_runs_logs or all(not logs for logs in all_runs_logs):
        return "<html><body><h1>No logs found</h1></body></html>"
    
    # Filter out empty runs
    all_runs_logs = [logs for logs in all_runs_logs if logs]
       
    with importlib.resources.files('logscope').joinpath('static/pico.min.css').open('r') as f:
        pico_css = f.read()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logs</title>
    <style>
        {pico_css}
        .log-entry {{
            margin: 1rem 0;
            padding: 0.25rem 0.5rem;
            border: 1px solid #555;
            border-radius: 4px;
            cursor: pointer;
            background-color: var(--pico-code-background-color);
        }}
        .log-details {{
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 4px;
            line-height: 0.5;
            font-size: 80%;
        }}
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        article {{
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border: 1px solid #555;
        }}
        .time-delta {{
            color: #666;
            font-size: 80%;
        }}
        .entry-label {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .props {{
            font-size: 70%;
            margin-top: 2rem;
        }}
    </style>
    <script>
        function toggleDetails(id) {{
            const details = document.getElementById(id);
            if (details.style.display === 'none' || !details.style.display) {{
                details.style.display = 'block';
            }} else {{
                details.style.display = 'none';
            }}
        }}
    </script>
</head>
<body>
    <main class="container">
        <h1>Logs</h1>
        <p>last {'run' if len(all_runs_logs) == 1 else str(len(all_runs_logs)) + ' runs'}</p>
"""
    
    for logs in all_runs_logs:
        html += generate_html_report_for_run(logs)
    
    html += """
    </main>
</body>
</html>
"""
    return html

def view_runs(db_path: str = 'logscope.db', num_runs: int = 1) -> None:
    """
    Generate an HTML report of the specified number of recent runs and open it in the browser.
    
    Args:
        db_path: Path to the SQLite database file (default: 'logscope.db')
        num_runs: Number of recent runs to include in the report (default: 1)
    """
    run_ids = get_run_ids(db_path, num_runs)
    
    if not run_ids:
        print("No logs found in the database.")
        return
    
    all_runs_logs = [get_logs_by_run(db_path, run_id) for run_id in run_ids]
    html_content = generate_html_report(all_runs_logs)
    
    # Create a temporary file with the HTML content
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    # Open the report in the default browser
    webbrowser.open('file://' + temp_path)
