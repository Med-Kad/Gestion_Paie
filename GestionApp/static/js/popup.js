function openPopup(fichierId) {
    // Sauvegarde l'URL actuelle dans le stockage local
    localStorage.setItem("previousUrl", window.location.href);

    document.getElementById("originalFichierId").value = fichierId;
    // if (fichierType == "BADR" || fichierType == "confraires_BADR") {
    //     document.getElementById("firstOption").value = "BADR";
    //     document.getElementById("firstOption").InnerHTML = "BADR";
    //     document.getElementById("secondOption").value = "confraires_BADR";
    //     document.getElementById("secondOption").InnerHTML = "Confraires BADR";
        
    // }else if (fichierType == "CPA" || fichierType == "confraires_CPA") {
    //     document.getElementById("firstOption").value = "CPA";
    //     document.getElementById("firstOption").InnerHTML = "CPA";
    //     document.getElementById("firstOption").value = "confraires_CPA";
    //     document.getElementById("secondOption").InnerHTML = "Confraires CPA";
    // }
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
