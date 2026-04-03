async function topic() {
                const topic = document.getElementById("topic").value;
                const question = document.getElementById("question").value;

                const response = await 
                fetch("http://127.0.0.1:8000/topic",
                    {
                        method: "POST",
                        headers:{
                            "Content-Type" : "application/json"
                        },
                        body: JSON.stringify({topic, question})
                    }
                );

                const data = await response.json();

                document.getElementById("answer").innerText = data.answer;
            }