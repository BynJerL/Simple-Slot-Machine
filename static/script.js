const slots = document.querySelectorAll(".slot");
const gainEl = document.getElementById("gain");
const totalEl = document.getElementById("total");
const spinBtn = document.getElementById("spinBtn");
const endBtn = document.getElementById("endBtn");

let totalScore = 0;
let isSpinning = false;

const SYMBOLS = ["🍓", "🍒", "🌽", "🍋", "💣", "🍀"];

function setScore(element, value) {
    element.textContent = value > 0? `+${value}` : `${value}`;
    element.classList.remove("positive", "negative");
    element.classList.add(value >= 0 ? "positive" : "negative");
}

function randomSymbol() {
    return SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
}

function spin() {
    if (isSpinning) return;

    isSpinning = true;
    spinBtn.disabled = true;
    endBtn.disabled = true;

    let spinCount = 0;

    const interval = setInterval(() => {
        slots.forEach(slot => {
            slot.textContent = randomSymbol();
        });

        spinCount++;

        if (spinCount > 15) {
            clearInterval(interval);
            finishSpin();
        }
    }, 80);
}

function finishSpin() {
    const gain = Math.floor(Math.random() * 21) - 5; // Fake gain for now :D

    totalScore += gain;

    setScore(gainEl, gain);
    setScore(totalEl, totalScore);

    isSpinning = false;
    spinBtn.disabled = false;
    endBtn.disabled = false;
}

spinBtn.addEventListener("click", spin);
endBtn.addEventListener("click", () => {
    alert(`Game Over!\nFinal Score: ${totalScore}`);
    spinBtn.disabled = true;
    endBtn.disabled = true;
});