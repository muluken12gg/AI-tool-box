async function topic() {
    const answerEl = document.getElementById("answer");
    const topic = document.getElementById("topic").value;
    const question = document.getElementById("question").value;
    answerEl.innerText = "Loading...";

    try {
        const response = await fetch("http://127.0.0.1:8000/topic", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic, question })
        });

        if (!response.ok) {
            throw new Error(`API error ${response.status}`);
        }

        const data = await response.json();
        answerEl.innerText = data.answer;
    } catch (error) {
        answerEl.innerText = `Error: ${error.message}`;
        console.error(error);
    }
}