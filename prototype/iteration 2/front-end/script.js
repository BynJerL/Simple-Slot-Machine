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
    const weights = symbolKeys.map(key => SYMBOLS_DATA[key].weight);
    
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);

    let random = Math.random() * totalWeight;

    for (let i = 0; i < symbolKeys.length; i++) {
        random -= weights[i];
        if (random <= 0) {
            return symbolKeys[i];
        }
    }

    return symbolKeys[symbolKeys.length - 1];
}

function rollMachine () {
    slotDisplay.querySelectorAll(".symbol").forEach(s => {
        s.textContent = getRandomSymbol();
    });
}

function paylineCheck() {
    // 5 x 3 grid
    const reels = slotDisplay.querySelectorAll(".reel");
    const grid = [];

    reels.forEach((reel, reelIndex) => {
        const symbols = reel.querySelectorAll(".symbol");
        symbols.forEach((symbol, rowIndex) => {
            if (!grid[rowIndex]) grid[rowIndex] = [];
            grid[rowIndex][reelIndex] = symbol.textContent;
        });
    });

    console.log("Grid:", grid);

    // Check horizontal paylines
    for (let row = 0; row < 3; row++) {
        const firstSymbol = grid[row][0];
        let allMatch = true;
        for (let col = 1; col < 5; col++) {
            if (grid[row][col] !== firstSymbol) {
                allMatch = false;
                break;
            }
        }
        if (allMatch) {
            console.log(`Payline win on row ${row + 1} with symbol ${firstSymbol}`);
        }
    }

    // Check diagonal paylines
    if (grid[0][0] === grid[1][1] && 
        grid[0][0] === grid[2][2] && 
        grid[0][0] === grid[1][3] && 
        grid[0][0] === grid[0][4]) {
        console.log(`Payline win on diagonal (top-left to bottom-right) with symbol ${grid[0][0]}`);
    }

    if (grid[2][0] === grid[1][1] && 
        grid[2][0] === grid[0][2] && 
        grid[2][0] === grid[1][3] &&
        grid[2][0] === grid[2][4]) {
        console.log(`Payline win on diagonal (bottom-left to top-right) with symbol ${grid[2][0]}`);
    }
}

spinButton.addEventListener("click", () => {
    rollMachine();
    paylineCheck();
});