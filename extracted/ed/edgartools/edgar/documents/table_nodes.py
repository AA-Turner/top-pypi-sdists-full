"""
Table-related nodes for the document tree.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
import pandas as pd
from edgar.documents.nodes import Node
from edgar.documents.types import NodeType, TableType


@dataclass
class Cell:
    """Table cell representation."""
    content: Union[str, Node]
    colspan: int = 1
    rowspan: int = 1
    is_header: bool = False
    align: Optional[str] = None
    
    def text(self) -> str:
        """Extract text from cell."""
        if isinstance(self.content, str):
            return self.content
        elif isinstance(self.content, Node):
            return self.content.text()
        return ''
    
    def html(self) -> str:
        """Generate cell HTML."""
        tag = 'th' if self.is_header else 'td'
        text = self.text()
        
        attrs = []
        if self.colspan > 1:
            attrs.append(f'colspan="{self.colspan}"')
        if self.rowspan > 1:
            attrs.append(f'rowspan="{self.rowspan}"')
        if self.align:
            attrs.append(f'align="{self.align}"')
        
        attr_str = ' ' + ' '.join(attrs) if attrs else ''
        return f'<{tag}{attr_str}>{text}</{tag}>'
    
    @property
    def is_numeric(self) -> bool:
        """Check if cell contains numeric data."""
        text = self.text().strip()
        if not text:
            return False
        
        # Remove common formatting
        clean_text = text.replace(',', '').replace('$', '').replace('%', '')
        clean_text = clean_text.replace('(', '-').replace(')', '')
        
        try:
            float(clean_text)
            return True
        except ValueError:
            return False
    
    @property
    def numeric_value(self) -> Optional[float]:
        """Get numeric value if cell is numeric."""
        if not self.is_numeric:
            return None
        
        text = self.text().strip()
        clean_text = text.replace(',', '').replace('$', '').replace('%', '')
        clean_text = clean_text.replace('(', '-').replace(')', '')
        
        try:
            return float(clean_text)
        except ValueError:
            return None


@dataclass
class Row:
    """Table row representation."""
    cells: List[Cell]
    is_header: bool = False
    
    def text(self) -> str:
        """Extract row text."""
        return ' | '.join(cell.text() for cell in self.cells)
    
    def html(self) -> str:
        """Generate row HTML."""
        cells_html = ''.join(cell.html() for cell in self.cells)
        return f'<tr>{cells_html}</tr>'
    
    @property
    def is_numeric_row(self) -> bool:
        """Check if row contains mostly numeric data."""
        numeric_count = sum(1 for cell in self.cells if cell.is_numeric)
        return numeric_count > len(self.cells) / 2
    
    @property
    def is_total_row(self) -> bool:
        """Check if this might be a total row."""
        text = self.text().lower()
        total_keywords = ['total', 'sum', 'subtotal', 'grand total']
        return any(keyword in text for keyword in total_keywords)


@dataclass
class TableNode(Node):
    """
    Table node with structured data.
    
    Supports complex table structures with multi-level headers,
    merged cells, and semantic understanding.
    """
    type: NodeType = field(default=NodeType.TABLE, init=False)
    headers: List[List[Cell]] = field(default_factory=list)
    rows: List[Row] = field(default_factory=list)
    footer: List[Row] = field(default_factory=list)
    table_type: TableType = TableType.GENERAL
    
    # Table metadata
    caption: Optional[str] = None
    summary: Optional[str] = None
    
    @property
    def semantic_type(self) -> TableType:
        """Get semantic type of table (alias for table_type)."""
        return self.table_type
    
    @semantic_type.setter
    def semantic_type(self, value: TableType):
        """Set semantic type of table."""
        self.table_type = value
    
    def text(self) -> str:
        """Convert table to text representation with same improvements as to_dataframe()."""
        from edgar.documents.utils.table_matrix import TableMatrix, ColumnAnalyzer
        from edgar.documents.utils.currency_merger import CurrencyColumnMerger
        
        lines = []
        
        # Add caption if present
        if self.caption:
            lines.append(f"Table: {self.caption}")
            lines.append("")
        
        # Build matrix to handle colspan/rowspan and apply improvements
        matrix = TableMatrix()
        matrix.build_from_rows(self.headers, self.rows)
        
        # Remove spacing columns
        analyzer = ColumnAnalyzer(matrix)
        clean_matrix = matrix.filter_spacing_columns()
        
        # Merge currency columns
        currency_merger = CurrencyColumnMerger(clean_matrix)
        currency_merger.detect_currency_pairs()
        if currency_merger.merge_pairs:
            clean_matrix = currency_merger.apply_merges()
        
        # Add headers from cleaned matrix
        if self.headers:
            for row_idx in range(len(self.headers)):
                expanded_row = clean_matrix.get_expanded_row(row_idx)
                header_texts = []
                for cell in expanded_row:
                    if cell is not None:
                        header_texts.append(cell.text())
                    else:
                        header_texts.append('')
                if header_texts:
                    header_text = ' | '.join(header_texts)
                    lines.append(header_text)
            
            # Add separator
            lines.append('-' * 50)
        
        # Add data rows from cleaned matrix
        start_row = len(self.headers) if self.headers else 0
        for row_idx in range(start_row, clean_matrix.row_count):
            expanded_row = clean_matrix.get_expanded_row(row_idx)
            row_texts = []
            for cell in expanded_row:
                if cell is not None:
                    row_texts.append(cell.text())
                else:
                    row_texts.append('')
            if row_texts and any(t.strip() for t in row_texts):
                row_text = ' | '.join(row_texts)
                lines.append(row_text)
        
        # Add footer (if present)
        if self.footer:
            lines.append('-' * 50)
            for row in self.footer:
                lines.append(row.text())
        
        return '\n'.join(lines)
    
    def html(self) -> str:
        """Generate table HTML."""
        parts = ['<table>']
        
        # Add caption
        if self.caption:
            parts.append(f'<caption>{self.caption}</caption>')
        
        # Add header
        if self.headers:
            parts.append('<thead>')
            for header_row in self.headers:
                cells = ''.join(cell.html() for cell in header_row)
                parts.append(f'<tr>{cells}</tr>')
            parts.append('</thead>')
        
        # Add body
        parts.append('<tbody>')
        for row in self.rows:
            parts.append(row.html())
        parts.append('</tbody>')
        
        # Add footer
        if self.footer:
            parts.append('<tfoot>')
            for row in self.footer:
                parts.append(row.html())
            parts.append('</tfoot>')
        
        parts.append('</table>')
        return '\n'.join(parts)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert table to pandas DataFrame with proper colspan/rowspan handling."""
        from edgar.documents.utils.table_matrix import TableMatrix, ColumnAnalyzer
        from edgar.documents.utils.currency_merger import CurrencyColumnMerger
        
        # Build matrix to handle colspan/rowspan
        matrix = TableMatrix()
        matrix.build_from_rows(self.headers, self.rows)
        
        # Remove spacing columns
        analyzer = ColumnAnalyzer(matrix)
        clean_matrix = matrix.filter_spacing_columns()
        
        # Merge currency columns ($ + value)
        currency_merger = CurrencyColumnMerger(clean_matrix)
        currency_merger.detect_currency_pairs()
        if currency_merger.merge_pairs:
            clean_matrix = currency_merger.apply_merges()
        
        # Extract headers with proper alignment
        if self.headers:
            # Get expanded headers from matrix
            header_arrays = []
            num_header_rows = len(self.headers)
            
            for row_idx in range(num_header_rows):
                expanded_row = clean_matrix.get_expanded_row(row_idx)
                header_texts = []
                
                prev_text = ''
                for i, cell in enumerate(expanded_row):
                    if cell is not None:
                        text = cell.text().strip()
                        header_texts.append(text)
                        prev_text = text
                    else:
                        # For spanned cells in first row, repeat the spanning header
                        # For subsequent rows, use empty string
                        if row_idx == 0 and prev_text:
                            header_texts.append(prev_text)
                        else:
                            header_texts.append('')
                
                # Fill in spanned cells with parent header text for MultiIndex
                if row_idx > 0 and header_arrays:
                    # For lower level headers, inherit from parent if empty
                    prev_header = header_arrays[-1]
                    for i, text in enumerate(header_texts):
                        if text == '' and i < len(prev_header):
                            # Check if this is under a spanned parent header
                            for j in range(i, -1, -1):
                                if prev_header[j] != '':
                                    # Keep empty to show it's under parent
                                    break
                
                header_arrays.append(header_texts)
            
            # Create column index
            if len(header_arrays) > 1:
                # Multi-level headers - create MultiIndex
                # Clean up arrays to same length
                max_len = max(len(arr) for arr in header_arrays)
                for arr in header_arrays:
                    while len(arr) < max_len:
                        arr.append('')
                
                df_columns = pd.MultiIndex.from_arrays(header_arrays)
            else:
                # Single level headers
                df_columns = header_arrays[0] if header_arrays else []
        else:
            # No headers, use numeric columns
            df_columns = list(range(clean_matrix.col_count))
        
        # Extract data rows with proper alignment
        data = []
        start_row = len(self.headers) if self.headers else 0
        
        for row_idx in range(start_row, clean_matrix.row_count):
            expanded_row = clean_matrix.get_expanded_row(row_idx)
            row_data = []
            
            for cell in expanded_row:
                if cell is not None:
                    text = cell.text()
                    # Check if this is a merged currency value (starts with $, €, £, etc.)
                    if text and text[0] in {'$', '€', '£', '¥'}:
                        # Keep the full text with currency symbol
                        row_data.append(text)
                    elif cell.is_numeric:
                        row_data.append(cell.numeric_value)
                    else:
                        row_data.append(text)
                else:
                    row_data.append(None)  # Empty cell
            
            # Only add non-empty rows
            if any(v is not None and str(v).strip() for v in row_data):
                data.append(row_data)
        
        # Create DataFrame
        if data and df_columns is not None:
            # Ensure data width matches column width
            col_count = len(df_columns) if hasattr(df_columns, '__len__') else df_columns.nlevels
            for row in data:
                while len(row) < col_count:
                    row.append(None)
                while len(row) > col_count:
                    row.pop()
            
            df = pd.DataFrame(data, columns=df_columns)
            
            # Set row index if first column is labels
            if self.has_row_headers and len(df.columns) > 0:
                df = df.set_index(df.columns[0])
            
            return df
        else:
            # Return empty DataFrame with columns
            return pd.DataFrame(columns=df_columns if df_columns is not None else [])
    
    def to_csv(self) -> str:
        """Export table as CSV."""
        df = self.to_dataframe()
        return df.to_csv(index=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert table to dictionary."""
        return {
            'type': self.table_type.name,
            'caption': self.caption,
            'headers': [[cell.text() for cell in row] for row in self.headers],
            'data': [[cell.text() for cell in row.cells] for row in self.rows],
            'footer': [[cell.text() for cell in row.cells] for row in self.footer]
        }
    
    def find_column(self, header_text: str) -> Optional[int]:
        """Find column index by header text."""
        if not self.headers:
            return None
        
        # Search in first header row
        for i, cell in enumerate(self.headers[0]):
            if header_text.lower() in cell.text().lower():
                return i
        
        return None
    
    def extract_column(self, column_index: int) -> List[str]:
        """Extract all values from a column."""
        values = []
        for row in self.rows:
            if column_index < len(row.cells):
                values.append(row.cells[column_index].text())
        return values
    
    def find_row_by_first_cell(self, text: str) -> Optional[Row]:
        """Find row by first cell content."""
        for row in self.rows:
            if row.cells and text.lower() in row.cells[0].text().lower():
                return row
        return None
    
    def get_numeric_columns(self) -> Dict[str, List[float]]:
        """Extract all numeric columns with their headers."""
        result = {}
        
        if not self.headers:
            return result
        
        # Check each column
        for col_idx, header_cell in enumerate(self.headers[0]):
            header = header_cell.text()
            values = []
            is_numeric_col = True
            
            # Extract values from column
            for row in self.rows:
                if col_idx < len(row.cells):
                    cell = row.cells[col_idx]
                    if cell.is_numeric:
                        values.append(cell.numeric_value)
                    else:
                        # Check if it's a total row or empty
                        if not row.is_total_row and cell.text().strip():
                            is_numeric_col = False
                            break
                        values.append(None)
            
            # Only include if mostly numeric
            if is_numeric_col and values:
                non_none_values = [v for v in values if v is not None]
                if len(non_none_values) > len(values) * 0.5:  # At least 50% numeric
                    result[header] = values
        
        return result
    
    def find_totals(self) -> Dict[str, float]:
        """Find total rows in table."""
        totals = {}
        
        for row in self.rows:
            if row.is_total_row:
                # Extract label from first cell
                label = row.cells[0].text() if row.cells else "Total"
                
                # Find numeric values in row
                for cell in row.cells[1:]:  # Skip label cell
                    if cell.is_numeric:
                        totals[label] = cell.numeric_value
                        break
        
        return totals
    
    @property
    def is_financial_table(self) -> bool:
        """Check if this appears to be a financial table."""
        if self.table_type == TableType.FINANCIAL:
            return True
        
        # Check headers for financial keywords
        financial_keywords = [
            'revenue', 'income', 'expense', 'asset', 'liability',
            'cash', 'equity', 'profit', 'loss', 'margin'
        ]
        
        header_text = ' '.join(
            cell.text().lower() 
            for row in self.headers 
            for cell in row
        )
        
        return any(keyword in header_text for keyword in financial_keywords)
    
    @property
    def row_count(self) -> int:
        """Get total number of rows in table (including headers)."""
        return len(self.headers) + len(self.rows)
    
    @property
    def col_count(self) -> int:
        """Get number of columns in table."""
        if self.headers and self.headers[0]:
            return len(self.headers[0])
        elif self.rows and self.rows[0].cells:
            return len(self.rows[0].cells)
        return 0
    
    @property
    def has_header(self) -> bool:
        """Check if table has header rows."""
        return bool(self.headers)
    
    @property
    def has_row_headers(self) -> bool:
        """Check if table has row headers (first column as labels)."""
        if not self.rows:
            return False
        
        # Check if first column is non-numeric
        first_col_numeric = 0
        for row in self.rows:
            if row.cells and row.cells[0].is_numeric:
                first_col_numeric += 1
        
        # If less than 20% of first column is numeric, likely row headers
        return first_col_numeric < len(self.rows) * 0.2
    
    @property
    def numeric_columns(self) -> List[int]:
        """Get indices of numeric columns."""
        numeric_cols = []
        
        for col_idx in range(self.col_count):
            numeric_count = 0
            total_count = 0
            
            for row in self.rows:
                if col_idx < len(row.cells):
                    total_count += 1
                    if row.cells[col_idx].is_numeric:
                        numeric_count += 1
            
            # If more than 50% numeric, consider it a numeric column
            if total_count > 0 and numeric_count / total_count > 0.5:
                numeric_cols.append(col_idx)
        
        return numeric_cols
    
    
    def summarize_for_llm(self, max_tokens: int = 500) -> str:
        """Create concise table summary for LLM processing."""
        parts = []
        
        # Add type and structure info
        parts.append(f"Table Type: {self.table_type.name}")
        parts.append(f"Size: {len(self.rows)} rows × {len(self.headers[0]) if self.headers else 'unknown'} columns")
        
        if self.caption:
            parts.append(f"Caption: {self.caption}")
        
        # Add column headers
        if self.headers:
            headers = [cell.text() for cell in self.headers[0]]
            parts.append(f"Columns: {', '.join(headers[:5])}")
            if len(headers) > 5:
                parts.append(f"  ... and {len(headers) - 5} more columns")
        
        # Add sample data or totals
        totals = self.find_totals()
        if totals:
            parts.append("Key totals:")
            for label, value in list(totals.items())[:3]:
                parts.append(f"  {label}: {value:,.0f}")
        
        # Add numeric column summary
        numeric_cols = self.get_numeric_columns()
        if numeric_cols:
            parts.append("Numeric columns found:")
            for col_name in list(numeric_cols.keys())[:3]:
                parts.append(f"  - {col_name}")
        
        return '\n'.join(parts)