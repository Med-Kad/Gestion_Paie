function openPopup(fichierId) {
    // Sauvegarde l'URL actuelle dans le stockage local
    localStorage.setItem("previousUrl", window.location.href);

    document.getElementById("originalFichierId").value = fichierId;
    document.getElementById("clonePopup").classList.remove("hidden");
}

function closePopup() {
    document.getElementById("clonePopup").classList.add("hidden");
    document.getElementById("originalFichierId").value = "";
    document.getElementById("mois").value = "1";
    document.getElementById("annee").value = "";
    document.getElementById("type").value = "BADR";
    document.getElementById("description").innerHTML = "";

    // Récupère l'URL précédente depuis le stockage local
    const previousUrl = localStorage.getItem("previousUrl");
    if (previousUrl) {
        // Supprime l'URL du stockage local (optionnel)
        localStorage.removeItem("previousUrl");

        // Redirige vers l'URL précédente
        window.location.href = previousUrl;
    }
}
