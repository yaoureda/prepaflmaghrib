document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("filters-form");
    const content = document.getElementById("content");
    const statusText = document.getElementById("status-text");
    const noResults = document.getElementById("no-results");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const params = new URLSearchParams(new FormData(form));
        statusText.textContent = "Chargement...";
        content.innerHTML = "";
        noResults.classList.add("d-none");

        try {
            const response = await fetch(`/browse/annales?${params.toString()}`);
            const data = await response.json();

            statusText.textContent = `${data.length} résultat(s)`;

            if (data.length === 0) {
                noResults.classList.remove("d-none");
                return;
            }

            data.forEach(annale => {
                const col = document.createElement("div");
                col.className = "col-md-6 col-xl-4";

                col.innerHTML = `
                    <div class="card shadow-sm h-100">
                        <div class="card-body">
                            <h5 class="card-title" style="color:darkgreen; font-weight:bold;">${annale.filiere} ${annale.annee}</h5>
                            <p class="card-text">
                                <strong>Matière :</strong> ${annale.matiere}<br>
                                <strong>Thèmes :</strong> ${annale.themes}
                            </p>
                            <a href="${annale.url}" target="_blank" class="me-3">Sujet</a>
                            <a href="${annale.corrige}" target="_blank">Corrigé</a>
                        </div>
                    </div>
                `;

                content.appendChild(col);
            });

        } catch (error) {
            statusText.textContent = "Erreur lors du chargement.";
            console.error(error);
        }
    });
});
