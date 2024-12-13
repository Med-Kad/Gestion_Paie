function closeNotification() { 
    const notification = document.querySelector('[role="alert"]');
    if (notification) {
        notification.style.display = "none"; // Ferme immédiatement la notification
    }
}

function confirmDownload(fichierId) {
    if (confirm("Voulez-vous vraiment télécharger ce fichier ?")) {
        window.location.href = `/telecharger/${fichierId}/`;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const notification = document.querySelector('[role="alert"]');

    if (notification) {
        const notificationType = notification.classList.contains('bg-green-200') ? 'success' : 'warning';

        if (notificationType === 'success') {
            // Ajoutez ici toute logique spécifique pour la notification de succès, si nécessaire.
            // Délai de 3 secondes avant de commencer la disparition
        setTimeout(() => {
            notification.style.opacity = "0"; // Définir l'opacité à 0
        }, 3000);

        // Supprimer complètement la notification après 1 seconde supplémentaire (durée de la transition)
        setTimeout(() => {
            notification.style.display = "none";
        }, 4000); // 3 secondes + 1 seconde
    }
        }

        
});

