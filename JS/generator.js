async function generate() {
                const prompt = document.getElementById("prompt").value;

                const response = await 
                fetch("http://127.0.0.1:8000/generator",
                    {
                        method: "POST",
                        headers:{
                            "Content-Type" : "application/json"
                        },
                        body: JSON.stringify({prompt})
                    }
                );

                const data = await response.json();

                document.getElementById("code").innerText = data.answer;
            }