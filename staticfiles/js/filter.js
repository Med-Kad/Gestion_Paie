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
        const rib = document.getElementById('ribInput').value;
        const fullname = document.getElementById('nameInput').value;
        const address = document.getElementById('addressInput').value;

        const url = new URL(window.location.href);

        // Mettre à jour les paramètres de recherche
        if (rib) url.searchParams.set('rib', rib);
        else url.searchParams.delete('rib');

        if (fullname) url.searchParams.set('fullname', fullname);
        else url.searchParams.delete('fullname');

        if (address) url.searchParams.set('address', address);
        else url.searchParams.delete('address');

        window.history.pushState({}, '', url); // Met à jour l'URL sans recharger la page
        updateTable(url);
    };

    // Ajouter les écouteurs d'événements pour les champs de recherche
    document.getElementById('ribInput').addEventListener('input', handleInputChange);
    document.getElementById('nameInput').addEventListener('input', handleInputChange);
    document.getElementById('addressInput').addEventListener('input', handleInputChange);
});
/////////////////////////////////
