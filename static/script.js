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

const SFX = {
    spin: new Audio("assets/sfx/spin.mp3"),
    stop: new Audio("assets/sfx/reel_stop.mp3"),
    win: new Audio("assets/sfx/win.mp3"),
    jackpot: new Audio("assets/sfx/jackpot.mp3"),
    bomb: new Audio("assets/sfx/bomb.mp3"),
    end: new Audio("assets/sfx/game_over.mp3")
};

// Prevent overlap bugs
function playSFX(sound) {
    sound.currentTime = 0;
    sound.play();
}

const JACKPOT_MULTIPLIER = 10;
const SPIN_COST = -1;
const BOMB_PENALTY = -3;

function setScore(element, value) {
    element.textContent = value > 0? `+${value}` : `${value}`;
    element.classList.remove("positive", "negative");
    element.classList.add(value >= 0 ? "positive" : "negative");
}

function getDifficultyMultiplier() {
    if (totalScore < 20) return 1;
    if (totalScore < 50) return 1.3;
    if (totalScore < 100) return 1.7;
    return 2.2;
}

function randomSymbol() {
    const difficulty = getDifficultyMultiplier();

    const weightedPool = [];

    for (const icon in SYMBOL_DATA) {
        let weight = SYMBOL_DATA[icon].weight;

        // Bomb becomes more likely
        if (icon === "💣") {
            weight *= difficulty;
        }

        // Clover becomes rarer
        if (icon === "🍀") {
            weight /= difficulty;
        }

        weightedPool.push({ icon, weight });
    }

    const totalWeight = weightedPool.reduce((sum, i) => sum + i.weight, 0);
    let roll = Math.random() * totalWeight;

    for (const item of weightedPool) {
        roll -= item.weight;
        if (roll <= 0) return item.icon;
    }

    // Safety fallback
    return weightedPool[0].icon;
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
            playSFX(SFX.bomb);
            alert("💣 DISASTER!!!");
        } else {
            playSFX(SFX.jackpot);
            alert(`${icon} JACKPOT!!!`);
        }
    }

    // --- TWO OF A KIND ---
    else if (Object.values(counts).includes(2)) {
        const icon = Object.keys(counts).find(k => counts[k] === 2);

        if (icon === "💣") {
            playSFX(SFX.bomb);
            gain += BOMB_PENALTY;
        } else if ("💣" in counts) {
            playSFX(SFX.bomb);
            gain += 1;
        } else {
            playSFX(SFX.win);
            gain += SYMBOL_DATA[icon].value * 2;
        }
    }

    // --- BOMB (MIXED) ---
    else if ("💣" in counts) {
        playSFX(SFX.bomb);
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