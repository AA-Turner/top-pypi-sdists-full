"""
Early currency merger that works on raw table data before matrix expansion.
"""

from typing import List
from edgar.documents.table_nodes import Cell, Row


class EarlyCurrencyMerger:
    """Merge currency symbols with values at the row level before matrix building."""
    
    @staticmethod
    def merge_row_currencies(cells: List[Cell]) -> List[Cell]:
        """
        Merge adjacent $ and numeric cells, and numeric and % cells in a row.
        
        Args:
            cells: List of cells in a row
            
        Returns:
            New list of cells with currencies and percents merged
        """
        if len(cells) < 2:
            return cells
        
        merged = []
        i = 0
        
        while i < len(cells):
            cell = cells[i]
            cell_text = cell.text().strip()
            
            # Check if this is a currency symbol
            if i < len(cells) - 1 and cell_text == '$':
                next_cell = cells[i + 1]
                next_text = next_cell.text().strip()
                
                # Check if next cell is a numeric value
                if next_text and (next_text[0].isdigit() or next_text[0] == '(' or next_text == '—'):
                    # Merge them
                    merged_cell = Cell(
                        content=f"${next_text}",
                        colspan=cell.colspan,  # Keep first cell's colspan
                        rowspan=cell.rowspan,
                        is_header=cell.is_header,
                        align=next_cell.align  # Use number's alignment
                    )
                    merged.append(merged_cell)
                    
                    # Skip the value cell
                    i += 2
                    continue
            
            # Check if next cell is a percent symbol
            elif i < len(cells) - 1:
                next_cell = cells[i + 1]
                next_text = next_cell.text().strip()
                
                if next_text == '%':
                    # Check if current cell is numeric or parenthetical number or dash
                    if cell_text and (
                        cell_text[0].isdigit() or 
                        cell_text[0] == '(' or 
                        cell_text in ['—', '-', '–'] or
                        (cell_text.startswith('(') and cell_text.endswith(')'))
                    ):
                        # Merge them
                        merged_cell = Cell(
                            content=f"{cell_text}%",
                            colspan=cell.colspan,  # Keep first cell's colspan
                            rowspan=cell.rowspan,
                            is_header=cell.is_header,
                            align=cell.align
                        )
                        merged.append(merged_cell)
                        
                        # Skip the % cell
                        i += 2
                        continue
            
            # No merge, keep original cell
            merged.append(cell)
            i += 1
        
        return merged
    
    @staticmethod
    def merge_table_currencies(headers: List[List[Cell]], rows: List[Row]) -> tuple:
        """
        Merge currencies in entire table.
        
        Args:
            headers: List of header rows
            rows: List of data rows
            
        Returns:
            Tuple of (merged_headers, merged_rows)
        """
        # Merge headers
        merged_headers = []
        for header_row in headers:
            merged_cells = EarlyCurrencyMerger.merge_row_currencies(header_row)
            merged_headers.append(merged_cells)
        
        # Merge data rows
        merged_rows = []
        for row in rows:
            merged_cells = EarlyCurrencyMerger.merge_row_currencies(row.cells)
            merged_rows.append(Row(merged_cells, is_header=row.is_header))
        
        return merged_headers, merged_rows