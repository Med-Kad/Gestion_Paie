document.addEventListener("DOMContentLoaded", function () {
    const lockButtons = document.querySelectorAll(".lock-btn");

    const lockedSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
        <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 0 0-5.25 5.25v3a3 3 0 0 0-3 3v6.75a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3v-6.75a3 3 0 0 0-3-3v-3c0-2.9-2.35-5.25-5.25-5.25Zm3.75 8.25v-3a3.75 3.75 0 1 0-7.5 0v3h7.5Z" clip-rule="evenodd" />
    </svg>`;
    const unlockedSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
        <path d="M18 1.5c2.9 0 5.25 2.35 5.25 5.25v3.75a.75.75 0 0 1-1.5 0V6.75a3.75 3.75 0 1 0-7.5 0v3a3 3 0 0 1 3 3v6.75a3 3 0 0 1-3 3H3.75a3 3 0 0 1-3-3v-6.75a3 3 0 0 1 3-3h9v-3c0-2.9 2.35-5.25 5.25-5.25Z" />
    </svg>`;

    lockButtons.forEach((button) => {
        const fieldId = button.getAttribute("data-field-id");
        const field = document.getElementById(fieldId);
        const lockInput = document.getElementById(`lock_${fieldId}`);

        // Restaurer l'état du bouton (icône et classe) depuis localStorage
        const lockState = localStorage.getItem(`lock_${fieldId}`) || "unlocked";
        lockInput.value = lockState;

        if (lockState === "locked") {
            button.innerHTML = lockedSVG;
            button.classList.add("locked");
        } else {
            button.innerHTML = unlockedSVG;
            button.classList.remove("locked");
        }

        // Ajouter un gestionnaire de clics pour basculer l'état
        button.addEventListener("click", () => {
            if (lockInput.value === "locked") {
                // Déverrouiller
                lockInput.value = "unlocked";
                localStorage.setItem(`lock_${fieldId}`, "unlocked");
                button.innerHTML = unlockedSVG;
                button.classList.remove("locked");
            } else {
                // Verrouiller
                lockInput.value = "locked";
                localStorage.setItem(`lock_${fieldId}`, "locked");
                button.innerHTML = lockedSVG;
                button.classList.add("locked");
            }
        });

        // Synchroniser la valeur verrouillée lors des modifications du champ
        field.addEventListener("input", () => {
            if (lockInput.value === "locked") {
                localStorage.setItem(`locked_${fieldId}`, field.value);
            }
        });
    });
});
