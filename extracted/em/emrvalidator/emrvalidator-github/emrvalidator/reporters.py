"""
Report generators for validation results
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.str_, str)):
            return str(obj)
        return super().default(obj)


class ValidationReport:
    """Base class for validation reports"""
    
    def __init__(self, results: Dict[str, Any]):
        """
        Initialize report
        
        Args:
            results: Validation results from DataValidator
        """
        self.results = results
        self.metadata = results.get('metadata', {})
        self.summary = results.get('summary', {})
        self.validations = results.get('results', [])
        
    def get_failed_count(self) -> int:
        """Get number of failed validations"""
        return sum(1 for v in self.validations if not v['passed'] and v.get('critical', True))
    
    def get_warning_count(self) -> int:
        """Get number of warnings"""
        return sum(1 for v in self.validations if not v['passed'] and not v.get('critical', True))
    
    def get_status(self) -> str:
        """Get overall status"""
        if self.get_failed_count() > 0:
            return "FAILED"
        elif self.get_warning_count() > 0:
            return "WARNING"
        return "PASSED"


class JSONReporter(ValidationReport):
    """Generate JSON reports"""
    
    def generate(self, filepath: Optional[str] = None, pretty: bool = True) -> str:
        """
        Generate JSON report
        
        Args:
            filepath: Optional path to save report
            pretty: Whether to format JSON nicely
            
        Returns:
            JSON string
        """
        report = {
            "report_type": "EMR Validation Report",
            "generated_at": datetime.now().isoformat(),
            "status": self.get_status(),
            "metadata": self.metadata,
            "summary": self.summary,
            "validations": self.validations,
            "failed_validations": [v for v in self.validations if not v['passed']],
            "statistics": {
                "total_validations": len(self.validations),
                "passed": sum(1 for v in self.validations if v['passed']),
                "failed": self.get_failed_count(),
                "warnings": self.get_warning_count(),
                "success_rate": self.summary.get('success_rate', 0)
            }
        }
        
        json_str = json.dumps(report, cls=NumpyEncoder, indent=2 if pretty else None)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str


class HTMLReporter(ValidationReport):
    """Generate beautiful HTML reports"""
    
    def generate(self, filepath: Optional[str] = None, title: Optional[str] = None) -> str:
        """
        Generate HTML report
        
        Args:
            filepath: Optional path to save report
            title: Custom title for report
            
        Returns:
            HTML string
        """
        title = title or self.metadata.get('name', 'EMR Validation Report')
        status = self.get_status()
        status_color = {
            'PASSED': '#10b981',
            'WARNING': '#f59e0b',
            'FAILED': '#ef4444'
        }.get(status, '#6b7280')
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f3f4f6;
            color: #1f2937;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
        }}
        
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}
        
        .status-badge {{
            display: inline-block;
            background: {status_color};
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.875rem;
            margin-top: 10px;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f9fafb;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .stat-card .label {{
            font-size: 0.875rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .stat-card .value {{
            font-size: 2rem;
            font-weight: 700;
            color: #1f2937;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1f2937;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }}
        
        .validation-item {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: box-shadow 0.2s;
        }}
        
        .validation-item:hover {{
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .validation-item.passed {{
            border-left: 4px solid #10b981;
        }}
        
        .validation-item.failed {{
            border-left: 4px solid #ef4444;
        }}
        
        .validation-item.warning {{
            border-left: 4px solid #f59e0b;
        }}
        
        .validation-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .validation-title {{
            font-weight: 600;
            font-size: 1.1rem;
            color: #1f2937;
        }}
        
        .validation-status {{
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .validation-status.passed {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .validation-status.failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .validation-status.warning {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .validation-details {{
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 10px;
        }}
        
        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }}
        
        .detail-item {{
            background: white;
            padding: 10px;
            border-radius: 4px;
        }}
        
        .detail-label {{
            font-size: 0.75rem;
            color: #9ca3af;
            text-transform: uppercase;
            margin-bottom: 2px;
        }}
        
        .detail-value {{
            font-weight: 600;
            color: #1f2937;
        }}
        
        .footer {{
            background: #f9fafb;
            padding: 20px 30px;
            text-align: center;
            color: #6b7280;
            font-size: 0.875rem;
            border-top: 1px solid #e5e7eb;
        }}
        
        .no-items {{
            text-align: center;
            padding: 40px;
            color: #6b7280;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .validation-item:hover {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
            <span class="status-badge">{status}</span>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="label">Total Rows</div>
                <div class="value">{self.metadata.get('total_rows', 'N/A'):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Columns</div>
                <div class="value">{self.metadata.get('total_columns', 'N/A')}</div>
            </div>
            <div class="stat-card">
                <div class="label">Validations</div>
                <div class="value">{len(self.validations)}</div>
            </div>
            <div class="stat-card">
                <div class="label">Success Rate</div>
                <div class="value">{self.summary.get('success_rate', 0)}%</div>
            </div>
            <div class="stat-card" style="border-left-color: #10b981;">
                <div class="label">Passed</div>
                <div class="value" style="color: #10b981;">{self.summary.get('passed', 0)}</div>
            </div>
            <div class="stat-card" style="border-left-color: #ef4444;">
                <div class="label">Failed</div>
                <div class="value" style="color: #ef4444;">{self.get_failed_count()}</div>
            </div>
            <div class="stat-card" style="border-left-color: #f59e0b;">
                <div class="label">Warnings</div>
                <div class="value" style="color: #f59e0b;">{self.get_warning_count()}</div>
            </div>
        </div>
        
        <div class="content">
"""
        
        # Failed validations section
        failed = [v for v in self.validations if not v['passed'] and v.get('critical', True)]
        if failed:
            html += """
            <div class="section">
                <div class="section-title">❌ Failed Validations</div>
"""
            for v in failed:
                html += self._render_validation(v, 'failed')
            html += """
            </div>
"""
        
        # Warnings section
        warnings = [v for v in self.validations if not v['passed'] and not v.get('critical', True)]
        if warnings:
            html += """
            <div class="section">
                <div class="section-title">⚠️ Warnings</div>
"""
            for v in warnings:
                html += self._render_validation(v, 'warning')
            html += """
            </div>
"""
        
        # Passed validations section
        passed = [v for v in self.validations if v['passed']]
        if passed:
            html += f"""
            <div class="section">
                <div class="section-title">✅ Passed Validations ({len(passed)})</div>
"""
            for v in passed[:10]:  # Show first 10 passed
                html += self._render_validation(v, 'passed')
            
            if len(passed) > 10:
                html += f"""
                <div class="no-items">
                    ... and {len(passed) - 10} more passed validations
                </div>
"""
            html += """
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            EMRValidator v1.0.0 | Healthcare Analytics Hub<br>
            Report generated for dataset with {self.metadata.get('total_rows', 'N/A')} rows
        </div>
    </div>
</body>
</html>
"""
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(html)
        
        return html
    
    def _render_validation(self, validation: Dict[str, Any], status: str) -> str:
        """Render a single validation item"""
        rule_name = validation.get('rule', 'Unknown')
        column = validation.get('column', 'N/A')
        message = validation.get('message', '')
        
        html = f"""
                <div class="validation-item {status}">
                    <div class="validation-header">
                        <div class="validation-title">{rule_name.replace('_', ' ').title()}: {column}</div>
                        <span class="validation-status {status}">{status.upper()}</span>
                    </div>
                    <div class="validation-details">
                        {message}
"""
        
        # Add detail grid for additional metrics
        details = {k: v for k, v in validation.items() 
                   if k not in ['rule', 'column', 'critical', 'passed', 'message']}
        
        if details:
            html += """
                        <div class="detail-grid">
"""
            for key, value in list(details.items())[:6]:  # Show max 6 details
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    html += f"""
                            <div class="detail-item">
                                <div class="detail-label">{key.replace('_', ' ').title()}</div>
                                <div class="detail-value">{value:,}</div>
                            </div>
"""
            html += """
                        </div>
"""
        
        html += """
                    </div>
                </div>
"""
        return html
