const wordForm = document.querySelector('[data-form="word-form"]');
const wordTable = document.querySelector('#table-body');
let totalScore = 0;
wordForm.addEventListener('submit', handleWordFormSubmit);
gameController();

async function handleWordFormSubmit(e) {
	e.preventDefault();
	const word = document.querySelector('#guess').value;
	console.log(word);
	const response = await axios.post('/', { word });
	document.querySelector('#guess-response').innerText = response.data[0].message;
	let wordScore = getScoreForWord(word, response);
	setTimeout(function () {
		document.querySelector('#guess-response').innerText = '';
	}, 2000);
	if (!response.data[0].duplicate) updateWordTable(word, wordScore);
	document.querySelector('#total-score').innerText = `Total score: ${updateTotalScore(word, response)}`;
}

function updateWordTable(word, score) {
	let bonusMessage = score >= 8 ? "<a style='color: red'>Multiplier!</a>" : '';
	const newHTML = `
    <tr> 
        <td>
            ${word}  
        </td>
        <td>
            ${score} ${bonusMessage}
        </td>
    </tr>
`;
	wordTable.insertAdjacentHTML('afterbegin', newHTML);
}

function updateTotalScore(word, response) {
	totalScore += getScoreForWord(word, response);
	return totalScore;
}

function getScoreForWord(word, response) {
	const wordLength = word.length < 4 ? word.length : word.length * 2;
	return response.data[0].message == 'Your word was ok' ? wordLength : 0;
}

function gameController() {
	let gameTimeRemaining = 60;
	let gameTimerEl = document.querySelector('#game-timer');
	let gameTimer = setInterval(async function () {
		gameTimeRemaining--;
		gameTimerEl.innerText = `Time remaining: ${gameTimeRemaining}`;
		if (gameTimeRemaining === 0) {
			clearInterval(gameTimer);
			gameTimerEl.style.color = 'red';
			document.querySelector('#guess').disabled = true;
			document.querySelector('#guess').placeholder = 'Game over!';
			document.querySelector('#submit-button').classList.toggle('hidden');
			document.querySelector('[data-form="reset-form"]').classList.toggle('hidden');
			const res = await passServerGameResults();
			console.log(`high score is ${res.data.high_score}`);
		}
	}, 1000);
}

async function passServerGameResults() {
	return await axios.post('/', { score: totalScore });
}
