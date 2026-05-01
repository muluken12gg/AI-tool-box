async function summarize() {
    const outputEl = document.getElementById("summarized");
    const text = document.getElementById("text").value;
    outputEl.innerText = "Loading...";

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`API error ${response.status}`);
        }

        const data = await response.json();
        outputEl.innerText = data.answer;
    } catch (error) {
        outputEl.innerText = `Error: ${error.message}`;
        console.error(error);
    }
}

if (!localStorage.getItem("user_id")) {
    localStorage.setItem("user_id", crypto.randomUUID());
}