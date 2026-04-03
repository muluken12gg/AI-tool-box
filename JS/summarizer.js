async function summarize() {
                const text = document.getElementById("text").value;

                const response = await 
                fetch("http://127.0.0.1:8000/summarize",
                    {
                        method: "POST",
                        headers:{
                            "Content-Type" : "application/json"
                        },
                        body: JSON.stringify({text})
                    }
                );

                const data = await response.json();

                document.getElementById("summarized").innerText = data.answer;
            }