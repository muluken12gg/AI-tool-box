const userIdKey = "mukai_user_id";
const userId = ensureUserId();
let chatHistory = null;

function ensureUserId() {
    let id = localStorage.getItem(userIdKey);
    if (!id) {
        id = crypto.randomUUID();
        localStorage.setItem(userIdKey, id);
    }
    return id;
}

function getChatHistoryElement() {
    if (!chatHistory) {
        chatHistory = document.getElementById("chat-history");
    }
    return chatHistory;
}

function renderMessage(role, content) {
    const chatEl = getChatHistoryElement();
    if (!chatEl) return;
    const messageEl = document.createElement("div");
    messageEl.className = `chat-bubble ${role}`;
    const roleLabel = role === "user" ? "You" : "AI";
    messageEl.innerHTML = `
        <span class="chat-role">${roleLabel}</span>
        <div>${escapeHtml(content)}</div>
    `;
    chatEl.appendChild(messageEl);
    chatEl.scrollTop = chatEl.scrollHeight;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

async function loadChatHistory() {
    const chatEl = getChatHistoryElement();
    if (!chatEl) return;
    chatEl.innerHTML = "Loading conversation...";

    try {
        const response = await fetch(`http://127.0.0.1:8000/chat/${userId}`);
        if (!response.ok) {
            throw new Error(`API error ${response.status}`);
        }

        const data = await response.json();
        chatEl.innerHTML = "";

        if (!data.messages || data.messages.length === 0) {
            chatEl.innerHTML = "Start the conversation by sending a message.";
            return;
        }

        data.messages.forEach((message) => {
            if (message.role === "system") return;
            renderMessage(message.role, message.content);
        });
    } catch (error) {
        chatEl.innerHTML = `Error loading history: ${error.message}`;
        console.error(error);
    }
}

async function sendMessage() {
    const input = document.getElementById("question");
    if (!input) return;
    const text = input.value.trim();
    if (!text) return;

    renderMessage("user", text);
    input.value = "";
    input.focus();

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: userId, message: text })
        });

        if (!response.ok) {
            throw new Error(`API error ${response.status}`);
        }

        const data = await response.json();
        renderMessage("assistant", data.reply);
    } catch (error) {
        renderMessage("assistant", `Error: ${error.message}`);
        console.error(error);
    }
}

function clearChat() {
    const chatEl = getChatHistoryElement();
    if (!chatEl) return;
    chatEl.innerHTML = "Start the conversation by sending a message.";
    localStorage.removeItem(userIdKey);
    location.reload();
}

window.addEventListener("DOMContentLoaded", () => {
    loadChatHistory();
    const input = document.getElementById("question");
    const sendBtn = document.getElementById("send-btn");
    const clearBtn = document.getElementById("clear-chat");

    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessage);
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", clearChat);
    }

    if (input) {
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    }
});