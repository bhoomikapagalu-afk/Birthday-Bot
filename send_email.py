<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Little Mystery, Bhoomika 🎂</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #fdf6f0, #f3e7fb);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .card {
    background: white;
    border-radius: 20px;
    max-width: 460px;
    width: 100%;
    padding: 32px 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    text-align: center;
  }
  h1 {
    color: #d63384;
    font-size: 24px;
    margin-bottom: 4px;
  }
  .sub {
    color: #777;
    font-size: 14px;
    margin-bottom: 24px;
  }
  .timer {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 28px;
  }
  .timer div {
    background: #f3e7fb;
    border-radius: 12px;
    padding: 12px 10px;
    min-width: 64px;
  }
  .timer .num {
    font-size: 26px;
    font-weight: bold;
    color: #6f42c1;
  }
  .timer .label {
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
  }
  hr {
    border: none;
    border-top: 1px solid #eee;
    margin: 24px 0;
  }
  .guess-section h2 {
    font-size: 18px;
    color: #333;
    margin-bottom: 6px;
  }
  .hint {
    color: #d63384;
    font-size: 14px;
    font-style: italic;
    margin-bottom: 16px;
  }
  input[type=text] {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #ddd;
    font-size: 15px;
    margin-bottom: 12px;
  }
  button {
    background: #d63384;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
  }
  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  .msg {
    margin-top: 14px;
    font-size: 14px;
    min-height: 20px;
  }
  .attempts {
    margin-top: 8px;
    font-size: 13px;
    color: #999;
  }
  .success {
    color: #198754;
    font-weight: bold;
  }
  .fail {
    color: #dc3545;
  }
</style>
</head>
<body>

<div class="card">
  <h1>Hey Bhoomika 👋</h1>
  <div class="sub">Counting down to your big day...</div>

  <div class="timer">
    <div><div class="num" id="days">--</div><div class="label">Days</div></div>
    <div><div class="num" id="hours">--</div><div class="label">Hours</div></div>
    <div><div class="num" id="minutes">--</div><div class="label">Min</div></div>
    <div><div class="num" id="seconds">--</div><div class="label">Sec</div></div>
  </div>

  <hr>

  <div class="guess-section">
    <h2>Want to know who's behind this? 🕵️‍♀️</h2>
    <div class="hint">Hint: find my nickname</div>
    <input type="text" id="guessInput" placeholder="Type your guess..." autocomplete="off">
    <br>
    <button id="guessBtn" onclick="submitGuess()">Guess</button>
    <div class="msg" id="msg"></div>
    <div class="attempts" id="attemptsLeft"></div>
  </div>
</div>

<script>
  // ---- Countdown target: nearest upcoming Sept 23 ----
  function getTarget() {
    const now = new Date();
    let year = now.getFullYear();
    let target = new Date(year, 8, 23, 0, 0, 0); // month is 0-indexed, 8 = September
    if (target < now) {
      target = new Date(year + 1, 8, 23, 0, 0, 0);
    }
    return target;
  }

  function updateCountdown() {
    const now = new Date();
    const target = getTarget();
    let diff = Math.max(0, target - now);

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    document.getElementById('days').textContent = days;
    document.getElementById('hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
  }
  updateCountdown();
  setInterval(updateCountdown, 1000);

  // ---- Guess-who game: 3 attempts per day, reset daily ----
  // The answer is NOT stored as plain text — only its SHA-256 hash is kept here,
  // so opening dev tools / view-source won't reveal the actual word.
  const ANSWER_HASH = "8a47cccff5a0b4e11f87b5997986091cbd7acde690760373eac2e385c4ef754b";
  const MAX_ATTEMPTS = 3;

  async function sha256(text) {
    const enc = new TextEncoder().encode(text);
    const buf = await crypto.subtle.digest("SHA-256", enc);
    return Array.from(new Uint8Array(buf))
      .map(b => b.toString(16).padStart(2, "0"))
      .join("");
  }

  function todayKey() {
    const d = new Date();
    return `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
  }

  function getAttemptsLeft() {
    const storedDate = localStorage.getItem('guessDate');
    const today = todayKey();
    if (storedDate !== today) {
      // new day, reset
      localStorage.setItem('guessDate', today);
      localStorage.setItem('guessAttempts', '0');
      localStorage.removeItem('guessSolved');
    }
    const used = parseInt(localStorage.getItem('guessAttempts') || '0', 10);
    return MAX_ATTEMPTS - used;
  }

  function renderAttempts() {
    const left = getAttemptsLeft();
    const solved = localStorage.getItem('guessSolved') === 'true';
    const btn = document.getElementById('guessBtn');
    const input = document.getElementById('guessInput');
    const attemptsEl = document.getElementById('attemptsLeft');

    if (solved) {
      attemptsEl.textContent = "You already cracked it today 😉";
      btn.disabled = true;
      input.disabled = true;
    } else if (left <= 0) {
      attemptsEl.textContent = "No attempts left today. Come back tomorrow!";
      btn.disabled = true;
      input.disabled = true;
    } else {
      attemptsEl.textContent = `${left} attempt(s) left today`;
      btn.disabled = false;
      input.disabled = false;
    }
  }

  async function submitGuess() {
    const left = getAttemptsLeft();
    if (left <= 0) { renderAttempts(); return; }

    const input = document.getElementById('guessInput');
    const guess = input.value.trim().toLowerCase();
    const msgEl = document.getElementById('msg');

    if (!guess) {
      msgEl.textContent = "Type something first!";
      msgEl.className = "msg fail";
      return;
    }

    const used = parseInt(localStorage.getItem('guessAttempts') || '0', 10);
    localStorage.setItem('guessAttempts', String(used + 1));

    const guessHash = await sha256(guess);

    if (guessHash === ANSWER_HASH) {
      localStorage.setItem('guessSolved', 'true');
      msgEl.textContent = "🎉 You got it! But I'm staying mysterious a little longer... see you soon 😏";
      msgEl.className = "msg success";
    } else {
      msgEl.textContent = "Nope, not it. Try again!";
      msgEl.className = "msg fail";
    }

    input.value = "";
    renderAttempts();
  }

  document.getElementById('guessInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') submitGuess();
  });

  renderAttempts();
</script>

</body>
</html>
