const slotDisplay = document.getElementById("slot-display");
const spinButton = document.getElementById("spin-btn");
const SYMBOLS_DATA = {
    "🍒": {value: 1, weight: 10},
    "🍊": {value: 2, weight: 10},
    "🍋": {value: 2, weight: 10},

    "🍇": {value: 3, weight: 8},
    "🍓": {value: 3, weight: 8},
    "🫐": {value: 3, weight: 8},

    "♠️": {value: 5, weight: 5},
    "♣️": {value: 5, weight: 5},
    "♥️": {value: 5, weight: 5},
    "♦️": {value: 5, weight: 5},

    "🍀": {value: 10, weight: 3},
    "🔔": {value: 10, weight: 3},

    "⭐": {value: 50, weight: 1},
    "💎": {value: 50, weight: 1},
};

function getRandomSymbol() {
    const symbolKeys = Object.keys(SYMBOLS_DATA);
    const randomKey = symbolKeys[Math.floor(Math.random() * symbolKeys.length)];
    return randomKey;
}

function rollMachine () {
    slotDisplay.querySelectorAll(".symbol").forEach(s => {
        s.textContent = getRandomSymbol();
    });
}

spinButton.addEventListener("click", rollMachine);