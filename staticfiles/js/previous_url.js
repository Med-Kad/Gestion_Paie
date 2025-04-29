
function SavePreviousUrl() {
    // Stocke l'URL actuelle dans le stockage local
    localStorage.setItem("previousUrl", window.location.href);
    console.log("URL précédente sauvegardée : " + window.location.href);
}


function handleDelete(rib, event) {
    console.log("handleDelete");

    // Récupérer l'URL précédente
    const previousUrl = window.location.href;

    // Trouver l'input correspondant à l'employé actuel
    const inputId = `previousUrl-${rib}`;
    const inputElement = document.getElementById(inputId);
    
    if (inputElement) {
        inputElement.value = previousUrl;
        console.log("Valeur de l'input : " + inputElement.value);
    } else {
        console.log("Input introuvable pour le RIB : " + rib);
    }

    // Demander confirmation
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet employé ?')) {
        return false;  // Annule la soumission si "Annuler"
    }

    return true;  // Soumet le formulaire après exécution du code
}



const previousUrl = localStorage.getItem("previousUrl");
if (previousUrl) {
    if (document.getElementById('previousUrl')){  // Vérifie si l'élément existe
    document.getElementById('previousUrl').value = previousUrl;
    }
}
