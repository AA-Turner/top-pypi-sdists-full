document.addEventListener('DOMContentLoaded', function() {
    const getCellValue = (tr, idx) => {
        const cell = tr.children[idx];
        return cell ? (cell.innerText || cell.textContent).trim() : '';
    };

    const comparer = (idx, asc) => (a, b) => {
        const vA = getCellValue(asc ? a : b, idx);
        const vB = getCellValue(asc ? b : a, idx);

        const vA_num = parseFloat(vA);
        const vB_num = parseFloat(vB);

        if (!isNaN(vA_num) && !isNaN(vB_num)) {
            return vA_num - vB_num;
        }
        return vA.localeCompare(vB, undefined, { numeric: true, sensitivity: 'base' });
    };

    document.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', () => {
            const table = th.closest('table');
            if (!table) return;

            const tbody = table.querySelector('tbody');
            if (!tbody) return;

            const thIndex = Array.from(th.parentNode.children).indexOf(th);
            const currentIsAsc = th.classList.contains('asc');
            const isAsc = !currentIsAsc;

            table.querySelectorAll('th.sortable').forEach(header => {
                header.classList.remove('asc', 'desc');
            });

            th.classList.add(isAsc ? 'asc' : 'desc');

            Array.from(tbody.querySelectorAll('tr'))
                .sort(comparer(thIndex, isAsc))
                .forEach(tr => tbody.appendChild(tr));
        });
    });

    // Initial sort for any table with a pre-sorted column
    document.querySelectorAll('table').forEach(table => {
        const initialSortHeader = table.querySelector('th.sortable.asc, th.sortable.desc');
        if (initialSortHeader) {
            const tbody = table.querySelector('tbody');
            if(tbody){
                const thIndex = Array.from(initialSortHeader.parentNode.children).indexOf(initialSortHeader);
                const isAsc = initialSortHeader.classList.contains('asc');
                Array.from(tbody.querySelectorAll('tr'))
                    .sort(comparer(thIndex, isAsc))
                    .forEach(tr => tbody.appendChild(tr));
            }
        }
    });
});
