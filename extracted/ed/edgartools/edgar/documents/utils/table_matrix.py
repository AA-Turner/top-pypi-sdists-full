"""
Table matrix builder for handling complex colspan/rowspan structures.
"""

from dataclasses import dataclass
from typing import List, Optional

from edgar.documents.table_nodes import Cell, Row


@dataclass
class MatrixCell:
    """Cell in the matrix with reference to original cell"""
    original_cell: Optional[Cell] = None
    is_spanned: bool = False  # True if this is part of a colspan/rowspan
    row_origin: int = -1  # Original row index
    col_origin: int = -1  # Original column index
    

class TableMatrix:
    """
    Build a 2D matrix representation of table with proper handling of merged cells.
    
    This class converts a table with colspan/rowspan into a regular 2D grid
    where each merged cell occupies multiple positions in the matrix.
    """
    
    def __init__(self):
        """Initialize empty matrix"""
        self.matrix: List[List[MatrixCell]] = []
        self.row_count = 0
        self.col_count = 0
        
    def build_from_rows(self, header_rows: List[List[Cell]], data_rows: List[Row]) -> 'TableMatrix':
        """
        Build matrix from header rows and data rows.
        
        Args:
            header_rows: List of header rows (each row is a list of Cells)
            data_rows: List of Row objects
            
        Returns:
            Self for chaining
        """
        # Combine all rows for processing
        all_rows = []
        
        # Add header rows
        for header_row in header_rows:
            all_rows.append(header_row)
        
        # Add data rows
        for row in data_rows:
            all_rows.append(row.cells)
        
        if not all_rows:
            return self
        
        # Calculate dimensions
        self.row_count = len(all_rows)
        
        # First pass: determine actual column count
        self._calculate_dimensions(all_rows)
        
        # Initialize matrix
        self.matrix = [[MatrixCell() for _ in range(self.col_count)] 
                       for _ in range(self.row_count)]
        
        # Second pass: place cells in matrix
        self._place_cells(all_rows)
        
        return self
    
    def _calculate_dimensions(self, rows: List[List[Cell]]):
        """Calculate the actual dimensions considering colspan"""
        max_cols = 0
        
        for row_idx, row in enumerate(rows):
            col_pos = 0
            for cell in row:
                # Skip positions that might be occupied by rowspan from above
                while col_pos < max_cols and self._is_occupied(row_idx, col_pos):
                    col_pos += 1
                
                # This cell will occupy from col_pos to col_pos + colspan
                col_end = col_pos + cell.colspan
                max_cols = max(max_cols, col_end)
                col_pos = col_end
        
        self.col_count = max_cols
    
    def _is_occupied(self, row: int, col: int) -> bool:
        """Check if a position is occupied by a cell from a previous row (rowspan)"""
        if row == 0:
            return False
        
        # Check if any cell above has rowspan that reaches this position
        for prev_row in range(row):
            if prev_row < len(self.matrix) and col < len(self.matrix[prev_row]):
                cell = self.matrix[prev_row][col]
                if cell.original_cell and cell.row_origin == prev_row:
                    # Check if this cell's rowspan reaches current row
                    if prev_row + cell.original_cell.rowspan > row:
                        return True
        return False
    
    def _place_cells(self, rows: List[List[Cell]]):
        """Place cells in the matrix handling colspan and rowspan"""
        for row_idx, row in enumerate(rows):
            col_pos = 0
            
            for cell_idx, cell in enumerate(row):
                # Find next available column position
                while col_pos < self.col_count and self.matrix[row_idx][col_pos].original_cell is not None:
                    col_pos += 1
                
                if col_pos >= self.col_count:
                    # Need to expand matrix
                    self._expand_columns(col_pos + cell.colspan)
                
                # Place cell in matrix
                for r in range(cell.rowspan):
                    for c in range(cell.colspan):
                        if row_idx + r < self.row_count and col_pos + c < self.col_count:
                            matrix_cell = MatrixCell(
                                original_cell=cell,
                                is_spanned=(r > 0 or c > 0),
                                row_origin=row_idx,
                                col_origin=col_pos
                            )
                            self.matrix[row_idx + r][col_pos + c] = matrix_cell
                
                col_pos += cell.colspan
    
    def _expand_columns(self, new_col_count: int):
        """Expand matrix to accommodate more columns"""
        if new_col_count <= self.col_count:
            return
        
        for row in self.matrix:
            row.extend([MatrixCell() for _ in range(new_col_count - self.col_count)])
        
        self.col_count = new_col_count
    
    def get_actual_columns(self) -> int:
        """Get the actual number of data columns (excluding empty/spacing columns)"""
        non_empty_cols = 0
        
        for col_idx in range(self.col_count):
            has_content = False
            for row_idx in range(self.row_count):
                cell = self.matrix[row_idx][col_idx]
                if cell.original_cell and not cell.is_spanned:
                    # Check if cell has actual content
                    text = cell.original_cell.text().strip()
                    if text and text not in ['', ' ', '\xa0']:
                        has_content = True
                        break
            
            if has_content:
                non_empty_cols += 1
        
        return non_empty_cols
    
    def get_column_widths(self) -> List[float]:
        """Estimate column widths based on content"""
        widths = []
        
        for col_idx in range(self.col_count):
            max_width = 0
            content_count = 0
            
            for row_idx in range(self.row_count):
                cell = self.matrix[row_idx][col_idx]
                if cell.original_cell and not cell.is_spanned:
                    text = cell.original_cell.text().strip()
                    if text:
                        max_width = max(max_width, len(text))
                        content_count += 1
            
            # If column has no content, it's likely a spacing column
            if content_count == 0:
                widths.append(0)
            else:
                widths.append(max_width)
        
        return widths
    
    def get_expanded_row(self, row_idx: int) -> List[Optional[Cell]]:
        """
        Get a row with cells expanded to match column count.
        
        For cells with colspan > 1, the cell appears in the first position
        and None in subsequent positions.
        """
        if row_idx >= self.row_count:
            return []
        
        expanded = []
        for col_idx in range(self.col_count):
            matrix_cell = self.matrix[row_idx][col_idx]
            if matrix_cell.original_cell:
                if not matrix_cell.is_spanned:
                    # This is the origin cell
                    expanded.append(matrix_cell.original_cell)
                else:
                    # This is a spanned position
                    expanded.append(None)
            else:
                # Empty cell
                expanded.append(None)
        
        return expanded
    
    def get_data_columns(self) -> List[int]:
        """
        Get indices of columns that contain actual data (not spacing).
        
        Returns:
            List of column indices that contain data
        """
        data_cols = []
        
        for col_idx in range(self.col_count):
            has_data = False
            
            for row_idx in range(self.row_count):
                cell = self.matrix[row_idx][col_idx]
                if cell.original_cell and not cell.is_spanned:
                    text = cell.original_cell.text().strip()
                    # Check for actual content (not just whitespace or nbsp)
                    if text and text not in ['', ' ', '\xa0', '-', '—', '–']:
                        has_data = True
                        break
            
            if has_data:
                data_cols.append(col_idx)
        
        return data_cols
    
    def filter_spacing_columns(self) -> 'TableMatrix':
        """
        Create a new matrix with spacing columns removed.
        
        Returns:
            New TableMatrix with only data columns
        """
        data_cols = self.get_data_columns()
        
        if len(data_cols) == self.col_count:
            # No spacing columns to remove
            return self
        
        # Create new matrix with only data columns
        new_matrix = TableMatrix()
        new_matrix.row_count = self.row_count
        new_matrix.col_count = len(data_cols)
        new_matrix.matrix = []
        
        for row_idx in range(self.row_count):
            new_row = []
            for new_col_idx, orig_col_idx in enumerate(data_cols):
                new_row.append(self.matrix[row_idx][orig_col_idx])
            new_matrix.matrix.append(new_row)
        
        return new_matrix
    
    def to_cell_grid(self) -> List[List[Optional[Cell]]]:
        """
        Convert matrix to a simple 2D grid of cells.
        
        Returns:
            2D list where each position contains either a Cell or None
        """
        grid = []
        
        for row_idx in range(self.row_count):
            row = []
            for col_idx in range(self.col_count):
                matrix_cell = self.matrix[row_idx][col_idx]
                if matrix_cell.original_cell and not matrix_cell.is_spanned:
                    row.append(matrix_cell.original_cell)
                else:
                    row.append(None)
            grid.append(row)
        
        return grid
    
    def debug_print(self):
        """Print matrix structure for debugging"""
        print(f"Matrix: {self.row_count}×{self.col_count}")
        
        for row_idx in range(self.row_count):
            row_str = []
            for col_idx in range(self.col_count):
                cell = self.matrix[row_idx][col_idx]
                if cell.original_cell:
                    text = cell.original_cell.text()[:10]
                    if cell.is_spanned:
                        row_str.append(f"[{text}...]")
                    else:
                        row_str.append(f"{text}...")
                else:
                    row_str.append("___")
            print(f"Row {row_idx}: {' | '.join(row_str)}")


class ColumnAnalyzer:
    """Analyze column structure to identify data vs spacing columns"""
    
    def __init__(self, matrix: TableMatrix):
        """Initialize with a table matrix"""
        self.matrix = matrix
    
    def identify_spacing_columns(self) -> List[int]:
        """
        Identify columns used only for spacing.
        
        Returns:
            List of column indices that are spacing columns
        """
        spacing_cols = []
        widths = self.matrix.get_column_widths()
        total_width = sum(widths)
        
        for col_idx in range(self.matrix.col_count):
            if self._is_spacing_column(col_idx, widths, total_width):
                spacing_cols.append(col_idx)
        
        return spacing_cols
    
    def _is_spacing_column(self, col_idx: int, widths: List[float], total_width: float) -> bool:
        """
        Check if a column is used for spacing.
        
        Criteria:
        - Column has no content (width = 0)
        - Column has very small width relative to total
        - Column contains only whitespace or formatting characters
        """
        # No content
        if widths[col_idx] == 0:
            return True
        
        # Very narrow column (less than 2% of total width)
        if total_width > 0 and widths[col_idx] / total_width < 0.02:
            # Check if it contains any meaningful data
            has_data = False
            for row_idx in range(self.matrix.row_count):
                cell = self.matrix.matrix[row_idx][col_idx]
                if cell.original_cell and not cell.is_spanned:
                    text = cell.original_cell.text().strip()
                    # Check for actual data (not just formatting)
                    if text and text not in ['', ' ', '\xa0', '-', '—', '–', '|']:
                        has_data = True
                        break
            
            if not has_data:
                return True
        
        return False
    
    def get_clean_column_indices(self) -> List[int]:
        """
        Get indices of non-spacing columns.
        
        Returns:
            List of column indices that contain actual data
        """
        spacing = set(self.identify_spacing_columns())
        return [i for i in range(self.matrix.col_count) if i not in spacing]