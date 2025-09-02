document.addEventListener('DOMContentLoaded', function() {
    const dateElement = document.getElementById('submission-date');
    if (dateElement) {
        const isoDate = dateElement.textContent.trim();
        if (isoDate) {
            const date = new Date(isoDate);

            // Helper function to pad numbers with a leading zero
            const pad = (num) => num.toString().padStart(2, '0');

            // Format the date part as dd/mm/yyyy
            const day = pad(date.getDate());
            const month = pad(date.getMonth() + 1); // getMonth() is zero-based
            const year = date.getFullYear();
            const formattedDate = `${day}/${month}/${year}`;

            // Format the time part as h:mm:ss am/pm
            let hours = date.getHours();
            const ampm = hours >= 12 ? 'pm' : 'am';
            hours = hours % 12;
            hours = hours ? hours : 12; // The hour '0' should be '12'
            const minutes = pad(date.getMinutes());
            const seconds = pad(date.getSeconds());
            const formattedTime = `${hours}:${minutes}:${seconds} ${ampm}`;

            const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            dateElement.textContent = `${formattedDate} at ${formattedTime} (${userTimezone})`;
        }
    }
});
