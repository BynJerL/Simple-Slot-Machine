const slots = document.querySelectorAll(".slot");
const gainEl = document.getElementById("gain");
const totalEl = document.getElementById("total");
const spinBtn = document.getElementById("spinBtn");
const endBtn = document.getElementById("endBtn");

let totalScore = 0;
let isSpinning = false;

const SYMBOL_DATA = {
    "🍓": { value: 1,  weight: 30 },
    "🍒": { value: 2,  weight: 25 },
    "🌽": { value: 4,  weight: 20 },
    "🍋": { value: 8,  weight: 15 },
    "💣": { value: -10, weight: 7 },
    "🍀": { value: 25, weight: 3 }
};

const JACKPOT_MULTIPLIER = 10;
const SPIN_COST = -1;
const BOMB_PENALTY = -3;

function setScore(element, value) {
    element.textContent = value > 0? `+${value}` : `${value}`;
    element.classList.remove("positive", "negative");
    element.classList.add(value >= 0 ? "positive" : "negative");
}

function randomSymbol() {
    const pool = [];

    for (const symbol in SYMBOL_DATA) {
        const { weight } = SYMBOL_DATA[symbol];
        for (let i = 0; i < weight; i++) {
            pool.push(symbol);
        }
    }

    return pool[Math.floor(Math.random() * pool.length)];
}

function spin() {
    if (isSpinning) return;

    isSpinning = true;
    spinBtn.disabled = true;
    endBtn.disabled = true;

    setScore(gainEl, 0);

    let results = [];
    let reelIndex = 0;

    function spinReel() {
        let ticks = 0;

        const interval = setInterval(() => {
            
            slots[reelIndex].textContent = randomSymbol();
            ticks++;

            if (ticks > 12 + reelIndex * 6) {
                const lastReelIndex = reelIndex;
                clearInterval(interval);
                slots[reelIndex].classList.add("stop");
                setTimeout(() => {
                    slots[lastReelIndex].classList.remove("stop")}, 150
                );
                results[reelIndex] = slots[reelIndex].textContent;
                reelIndex++;

                if (reelIndex < slots.length) {
                    spinReel();
                } else {
                    finishSpin(results);
                }
            }
        }, 70);
    }

    spinReel();
}

function finishSpin(results) {
    const counts = {};
    results.forEach(s => counts[s] = (counts[s] || 0) + 1);

    let gain = SPIN_COST;

    // --- JACKPOT ---
    if (Object.keys(counts).length === 1) {
        const icon = results[0];
        gain += SYMBOL_DATA[icon].value * JACKPOT_MULTIPLIER;

        if (icon === "💣") {
            alert("💣 DISASTER!!!");
        } else {
            alert(`${icon} JACKPOT!!!`);
        }
    }

    // --- TWO OF A KIND ---
    else if (Object.values(counts).includes(2)) {
        const icon = Object.keys(counts).find(k => counts[k] === 2);

        if (icon === "💣") {
            gain += BOMB_PENALTY;
        } else if ("💣" in counts) {
            gain += 1;
        } else {
            gain += SYMBOL_DATA[icon].value * 2;
        }
    }

    // --- BOMB (MIXED) ---
    else if ("💣" in counts) {
        gain += BOMB_PENALTY;
    }

    // --- NO MATCH ---
    else {
        gain += 0;
    }

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