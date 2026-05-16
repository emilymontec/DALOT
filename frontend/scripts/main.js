const API_BASE_URL = "/api";
const SESSION_STORAGE_KEY = "nura_session_id";

const state = {
    analysis: null,
    sessionId: getSessionId(),
};

function getSessionId() {
    const stored = window.localStorage.getItem(SESSION_STORAGE_KEY);
    if (stored) {
        return stored;
    }

    const sessionId = `nura-${Date.now()}`;
    window.localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
    return sessionId;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatNumber(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
        return "0";
    }
    return new Intl.NumberFormat("es-ES").format(Number(value));
}

function formatDecimal(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
        return "0.00";
    }
    return Number(value).toFixed(2);
}

function getRiskLabel(riskLevel, score) {
    if (!riskLevel) {
        return "Sin evaluar";
    }
    return `${riskLevel.toUpperCase()} · ${formatDecimal(score)}`;
}

function setApiStatus(text, detail, status) {
    const statusEl = document.getElementById("api-status");
    const detailEl = document.getElementById("api-status-detail");
    if (!statusEl || !detailEl) {
        return;
    }

    statusEl.textContent = text;
    detailEl.textContent = detail;
    statusEl.dataset.state = status;
}

function updateSessionLabel() {
    const label = document.getElementById("session-id-label");
    if (label) {
        label.textContent = state.sessionId;
    }
}

async function testAPI() {
    setApiStatus("Comprobando...", "Validando conectividad del backend.", "loading");

    try {
        const response = await fetch(`${API_BASE_URL}/test/`);
        const data = await response.json();
        setApiStatus("Conectado", data.message || "Backend operativo.", "ok");
    } catch (error) {
        setApiStatus("Sin conexion", "No fue posible contactar al backend.", "error");
    }
}

function addMessage(text, sender, id = null) {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) {
        return;
    }

    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}-msg`;
    if (id) {
        msgDiv.id = id;
    }

    msgDiv.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function openFilePicker() {
    const input = document.getElementById("data-upload");
    if (input) {
        input.click();
    }
}

function clearAnalysis() {
    state.analysis = null;

    document.getElementById("selected-file-label").textContent = "Sin archivo";
    document.getElementById("stat-file").textContent = "Esperando carga";
    document.getElementById("stat-rows").textContent = "0";
    document.getElementById("stat-columns").textContent = "0";
    document.getElementById("stat-risk").textContent = "Sin evaluar";
    document.getElementById("stat-health-detail").textContent = "Salud de datos pendiente";
    document.getElementById("upload-hint").textContent = "Formatos soportados: `.csv`, `.xlsx`, `.xls`";
    document.getElementById("insights-list").innerHTML = "Carga un archivo para ver alertas, patrones y recomendaciones iniciales.";
    document.getElementById("trends-table").innerHTML = "Aun no hay metricas disponibles para mostrar.";
}

function renderInsights(insights) {
    const container = document.getElementById("insights-list");
    if (!container) {
        return;
    }

    if (!insights || !insights.length) {
        container.innerHTML = "No se detectaron insights relevantes con el archivo actual.";
        return;
    }

    container.innerHTML = insights
        .map((insight) => `<article class="insight-item">${escapeHtml(insight)}</article>`)
        .join("");
}

function renderTrends(trends) {
    const container = document.getElementById("trends-table");
    if (!container) {
        return;
    }

    const entries = Object.entries(trends || {});
    if (!entries.length) {
        container.innerHTML = "El archivo no contiene columnas numericas suficientes para estimar tendencias.";
        return;
    }

    const rows = entries
        .map(([name, data]) => `
            <tr>
                <td>${escapeHtml(name)}</td>
                <td>${formatDecimal(data.mean)}</td>
                <td>${formatDecimal(data.min)}</td>
                <td>${formatDecimal(data.max)}</td>
                <td>${formatDecimal(data.trend)}</td>
            </tr>
        `)
        .join("");

    container.innerHTML = `
        <table class="trend-table">
            <thead>
                <tr>
                    <th>Variable</th>
                    <th>Media</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Pendiente</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `;
}

function renderAnalysis(data) {
    state.analysis = data;

    document.getElementById("selected-file-label").textContent = data.file_name || "Archivo procesado";
    document.getElementById("stat-file").textContent = data.file_name || "Archivo listo";
    document.getElementById("stat-rows").textContent = formatNumber(data.summary?.rows);
    document.getElementById("stat-columns").textContent = formatNumber(data.summary?.columns);
    document.getElementById("stat-risk").textContent = getRiskLabel(data.health?.risk_level, data.health?.health_score);
    document.getElementById("stat-health-detail").textContent = `Faltantes: ${formatNumber(data.summary?.total_missing)} · Duplicados: ${formatNumber(data.summary?.duplicate_rows)}`;
    document.getElementById("upload-hint").textContent = "Analisis generado. Ya puedes preguntar al chat por riesgos, patrones o recomendaciones.";

    renderInsights(data.insights);
    renderTrends(data.trends);
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) {
        return;
    }

    addMessage(message, "user");
    input.value = "";

    const typingId = `typing-${Date.now()}`;
    addMessage("Analizando tu consulta...", "bot", typingId);

    try {
        const response = await fetch(`${API_BASE_URL}/chat/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: state.sessionId }),
        });
        const data = await response.json();

        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.remove();
        }

        if (response.ok && data.response) {
            addMessage(data.response, "bot");
            return;
        }

        addMessage(`Error: ${data.error || "No se pudo obtener respuesta del asistente."}`, "bot");
    } catch (error) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.remove();
        }
        addMessage("Error de conexion. Verifica que el backend este en ejecucion.", "bot");
    }
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    const allowedExtensions = [".csv", ".xlsx", ".xls"];
    const extension = `.${file.name.split(".").pop().toLowerCase()}`;
    if (!allowedExtensions.includes(extension)) {
        addMessage("Formato no soportado. Usa archivos CSV o Excel.", "bot");
        event.target.value = "";
        return;
    }

    document.getElementById("selected-file-label").textContent = file.name;
    addMessage(`Archivo cargado: ${file.name}`, "user");

    const typingId = `typing-${Date.now()}`;
    addMessage("Procesando archivo y calculando insights...", "bot", typingId);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("session_id", state.sessionId);

    try {
        const response = await fetch(`${API_BASE_URL}/analyze/`, {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.remove();
        }

        if (!response.ok) {
            addMessage(`Error al analizar el archivo: ${data.error || "Error desconocido."}`, "bot");
            return;
        }

        renderAnalysis(data);
        addMessage(
            `Analisis completado.\nArchivo: ${data.file_name}\nRegistros: ${data.summary.rows}\nColumnas: ${data.summary.columns}\nRiesgo: ${data.health.risk_level}\nSalud: ${formatDecimal(data.health.health_score)}`,
            "bot"
        );

        if (data.insights?.length) {
            addMessage(`Insights iniciales:\n- ${data.insights.join("\n- ")}`, "bot");
        }
    } catch (error) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.remove();
        }
        addMessage("No fue posible subir o analizar el archivo. Revisa el backend.", "bot");
    }

    event.target.value = "";
}

function initializeDashboard() {
    updateSessionLabel();
    clearAnalysis();
    testAPI();
}

window.testAPI = testAPI;
window.sendMessage = sendMessage;
window.handleKeyPress = handleKeyPress;
window.handleFileUpload = handleFileUpload;
window.openFilePicker = openFilePicker;
window.clearAnalysis = clearAnalysis;
window.initializeDashboard = initializeDashboard;
