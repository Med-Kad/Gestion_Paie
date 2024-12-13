$(document).ready(function () {
    // Configuration pour le champ Employé
    $('#id_employe').select2({
        placeholder: "Sélectionnez un employé",
        width: '100%',
        allowClear: true,
        ajax: {
            url: "{% url 'search_employe' %}",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { q: params.term }; // Recherche
            },
            processResults: function (data) {
                return { results: data.results };
            },
        },
        
    });


    // Configuration pour le champ Fichier de Paie
    $('#id_fiche_paie').select2({
        placeholder: "Sélectionnez un fichier de paie",
        width: '100%',
        allowClear: true,
        ajax: {
            url: "{% url 'search_fichier_paie' %}",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { q: params.term }; // Recherche
            },
            processResults: function (data) {
                return { results: data.results };
            },
        },
    });
});