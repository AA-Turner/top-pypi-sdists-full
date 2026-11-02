/**
 * Make sidebar toctree captions collapsible.
 * Collapse all sections by default except the active section.
 */

document.addEventListener('DOMContentLoaded', function() {
    const captions = document.querySelectorAll('.sidebar-tree .caption');

    captions.forEach(function(caption) {
        const nextElement = caption.nextElementSibling;
        let hasCurrentPage = false;

        if (nextElement && nextElement.tagName === 'UL') {
            const currentLinks = nextElement.querySelectorAll('a.current');
            hasCurrentPage = currentLinks.length > 0;
        }

        if (!hasCurrentPage) {
            caption.classList.add('collapsed');
        }

        caption.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            this.classList.toggle('collapsed');
        });
    });
});
