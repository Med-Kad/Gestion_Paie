document.addEventListener("DOMContentLoaded", () => {
    const updateTable = (url) => {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                document.querySelector('tbody').innerHTML = doc.querySelector('tbody').innerHTML;
                document.querySelector('.pagination').innerHTML = doc.querySelector('.pagination').innerHTML;
            });
    };

    const handleInputChange = () => {
        const date = document.getElementById('dateInput').value;
        const description = document.getElementById('descriptionInput').value;
        const type = document.getElementById('typeInput').value;

        const url = new URL(window.location.href);
        if (date || description || type) {
            url.searchParams.set('date', date);
            url.searchParams.set('description', description);
            url.searchParams.set('type', type);
        } else {
            // Réinitialiser l'URL si tous les champs sont vides
            url.searchParams.delete('date');
            url.searchParams.delete('description');
            url.searchParams.delete('type');
        }

        window.history.pushState({}, '', url); // Met à jour l'URL sans recharger la page
        updateTable(url);
    };

    document.getElementById('dateInput').addEventListener('input', handleInputChange);
    document.getElementById('descriptionInput').addEventListener('input', handleInputChange);
    document.getElementById('typeInput').addEventListener('input', handleInputChange);
});
