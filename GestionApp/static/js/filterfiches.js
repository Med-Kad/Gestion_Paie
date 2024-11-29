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
        const employe_name = document.getElementById('employe_nameInput').value;
        const employe_rib = document.getElementById('employe_ribInput').value;
        const date = document.getElementById('dateInput').value;
        const type = document.getElementById('typeInput').value;
        const description = document.getElementById('descriptionInput').value;
        const montant = document.getElementById('montantInput').value;
        const libelle = document.getElementById('libelleInput').value;

        const url = new URL(window.location.href);
        if (employe_name || employe_rib || montant || libelle || date || type || description) {
        // if (employe || montant) {
            url.searchParams.set('employe_name', employe_name);
            url.searchParams.set('employe_rib', employe_rib);
            url.searchParams.set('montant', montant);
            url.searchParams.set('libelle', libelle);
            url.searchParams.set('date', date);
            url.searchParams.set('type', type);
            url.searchParams.set('description', description);
        } else {
            // Réinitialiser l'URL si tous les champs sont vides
            url.searchParams.delete('employe_name');
            url.searchParams.delete('employe_rib');
            url.searchParams.delete('montant');
            url.searchParams.delete('libelle');
            url.searchParams.delete('date');
            url.searchParams.delete('type');
            url.searchParams.delete('description');

        }

        window.history.pushState({}, '', url); // Met à jour l'URL sans recharger la page
        updateTable(url);
    };

    document.getElementById('montantInput').addEventListener('input', handleInputChange);
    document.getElementById('libelleInput').addEventListener('input', handleInputChange);
    document.getElementById('dateInput').addEventListener('input', handleInputChange);
    document.getElementById('typeInput').addEventListener('input', handleInputChange);
    document.getElementById('descriptionInput').addEventListener('input', handleInputChange);
    document.getElementById('employe_nameInput').addEventListener('input', handleInputChange);
    document.getElementById('employe_ribInput').addEventListener('input', handleInputChange);

});
