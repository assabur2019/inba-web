const electivesData = [
    // 3° Medio
    { grade: "3M", dept: "Lengua y Literatura", deptClass: "dept-lengua", title: "Participación y Argumentación en Democracia", icon: "fa-comments" },
    { grade: "3M", dept: "Filosofía", deptClass: "dept-filosofia", title: "Seminario de Filosofía", icon: "fa-brain" },
    { grade: "3M", dept: "Historia", deptClass: "dept-historia", title: "Comprensión Histórica del Presente", icon: "fa-landmark" },
    { grade: "3M", dept: "Matemática", deptClass: "dept-matematica", title: "Probabilidades y Estadística Descriptiva e Inferencial", icon: "fa-chart-pie" },
    { grade: "3M", dept: "Biología", deptClass: "dept-biologia", title: "Biología Celular y Molecular", icon: "fa-dna" },
    { grade: "3M", dept: "Química", deptClass: "dept-quimica", title: "Química", icon: "fa-flask" },
    { grade: "3M", dept: "Física", deptClass: "dept-fisica", title: "Física", icon: "fa-atom" },
    { grade: "3M", dept: "Educación Física", deptClass: "dept-edf", title: "Promoción de Estilos de Vida Activos y Saludables", icon: "fa-heart-pulse" },
    { grade: "3M", dept: "Artes Visuales", deptClass: "dept-artes", title: "Diseño y Arquitectura", icon: "fa-compass-drafting" },
    { grade: "3M", dept: "Música", deptClass: "dept-musica", title: "Interpretación Musical", icon: "fa-music" },

    // 4° Medio
    { grade: "4M", dept: "Lengua y Literatura", deptClass: "dept-lengua", title: "Taller de Literatura", icon: "fa-book-open-reader" },
    { grade: "4M", dept: "Filosofía", deptClass: "dept-filosofia", title: "Filosofía Política", icon: "fa-scale-balanced" },
    { grade: "4M", dept: "Historia", deptClass: "dept-historia", title: "Economía y Sociedad", icon: "fa-coins" },
    { grade: "4M", dept: "Matemática", deptClass: "dept-matematica", title: "Límites, Derivadas e Integrales", icon: "fa-square-root-variable" },
    { grade: "4M", dept: "Biología", deptClass: "dept-biologia", title: "Ciencias de la Salud", icon: "fa-user-doctor" },
    { grade: "4M", dept: "Química", deptClass: "dept-quimica", title: "Química", icon: "fa-vials" },
    { grade: "4M", dept: "Física", deptClass: "dept-fisica", title: "Física", icon: "fa-bolt" },
    { grade: "4M", dept: "Educación Física", deptClass: "dept-edf", title: "Ciencias del Ejercicio Físico y Deportivo", icon: "fa-person-running" },
    { grade: "4M", dept: "Artes Visuales", deptClass: "dept-artes", title: "Artes Visuales, Audiovisuales y Multimediales", icon: "fa-photo-film" },
    { grade: "4M", dept: "Música", deptClass: "dept-musica", title: "Creación y Composición Musical", icon: "fa-sliders" }
];

let activeLevel = "all";
let searchQuery = "";

document.addEventListener("DOMContentLoaded", () => {
    renderElectives();

    // Tab buttons listener
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            tabBtns.forEach(b => b.classList.remove("active"));
            const target = e.currentTarget;
            target.classList.add("active");
            activeLevel = target.getAttribute("data-level");
            renderElectives();
        });
    });

    // Search input listener
    const searchInput = document.getElementById("searchElectives");
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderElectives();
    });
});

function renderElectives() {
    const container = document.getElementById("electivesContainer");
    container.innerHTML = "";

    const filtered = electivesData.filter(item => {
        const matchesLevel = activeLevel === "all" || item.grade === activeLevel;
        const matchesSearch = item.title.toLowerCase().includes(searchQuery) ||
                              item.dept.toLowerCase().includes(searchQuery);
        return matchesLevel && matchesSearch;
    });

    if (filtered.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #64748b;">
                <i class="fa-solid fa-folder-open" style="font-size: 2.5rem; margin-bottom: 12px; display: block;"></i>
                <p>No se encontraron electivos que coincidan con la búsqueda.</p>
            </div>
        `;
        return;
    }

    filtered.forEach(item => {
        const card = document.createElement("div");
        card.className = "elective-card";
        
        const gradeLabel = item.grade === "3M" ? "3° Medio 2027" : "4° Medio 2027";

        card.innerHTML = `
            <div>
                <div class="card-top">
                    <span class="dept-badge ${item.deptClass}">${item.dept}</span>
                    <span class="grade-tag">${gradeLabel}</span>
                </div>
                <div class="card-icon">
                    <i class="fa-solid ${item.icon}"></i>
                </div>
                <h3 class="elective-title">${item.title}</h3>
            </div>
            <div class="card-footer">
                <i class="fa-solid fa-graduation-cap"></i> Electivo de Profundización 2027
            </div>
        `;
        container.appendChild(card);
    });
}
