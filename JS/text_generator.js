async function chat() {
    const outputEl = document.getElementById("text");
    const prompt = document.getElementById("prompt").value;
    outputEl.innerText = "Loading...";

    try {
        const response = await fetch("http://127.0.0.1:8000/text_generator", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
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