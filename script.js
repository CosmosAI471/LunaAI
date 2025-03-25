async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    let response = await fetch(`https://your-hf-space-link/api?text=${encodeURIComponent(userInput)}`);
    let data = await response.json();

    chatBox.innerHTML += `<p><strong>Luna:</strong> ${data.response}</p>`;
    document.getElementById("user-input").value = "";
}
