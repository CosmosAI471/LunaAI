const API_URL = "https://luna-backend-7ryq.onrender.com/lunaapi";

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}

function addMessage(msg, sender) {
  const chatlog = document.getElementById("chatlog");
  const message = document.createElement("div");
  message.className = sender;
  message.innerText = `${sender === 'user' ? 'You' : 'Luna'}: ${msg}`;
  chatlog.appendChild(message);
  chatlog.scrollTop = chatlog.scrollHeight;
}

async function sendToLuna(message, lat = null, lon = null) {
  addMessage(message, 'user');

  const payload = {
    user_message: message,
    location: lat && lon ? { lat, lon } : null
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  const reply = data.reply || "Sorry, no response.";
  addMessage(reply, 'luna');
  speak(reply);
}

function startVoiceInput() {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();
  recognition.onresult = async (event) => {
    const msg = event.results[0][0].transcript;
    navigator.geolocation.getCurrentPosition(pos => {
      const { latitude, longitude } = pos.coords;
      sendToLuna(msg, latitude, longitude);
    }, () => sendToLuna(msg));
  };
}

function sendText() {
  const input = document.getElementById("textInput");
  const msg = input.value;
  input.value = '';
  navigator.geolocation.getCurrentPosition(pos => {
    const { latitude, longitude } = pos.coords;
    sendToLuna(msg, latitude, longitude);
  }, () => sendToLuna(msg));
}
