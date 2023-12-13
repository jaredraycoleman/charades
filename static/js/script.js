document.addEventListener("DOMContentLoaded", function() {
    const getTopicBtn = document.getElementById('get-topic-btn');
    const resetScoreBtn = document.getElementById('reset-score-btn');
    const topicDisplay = document.getElementById('topic-display');
    const scoreDisplay = document.getElementById('score-display');

    let score = parseInt(getCookie('score')) || 0;
    updateScoreDisplay();

    getTopicBtn.addEventListener('click', function() {
        fetch('/get-topic', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            topicDisplay.innerHTML = `English: ${data.topic_en} - Portuguese: ${data.topic_pt}`;
            updateScore(1);
        });
    });

    resetScoreBtn.addEventListener('click', function() {
        updateScore(-score);
    });

    let team1Score = parseInt(getCookie('team1')) || 0;
    let team2Score = parseInt(getCookie('team2')) || 0;
    updateScoreDisplay();

    team1WinBtn.addEventListener('click', function() {
        updateScore('team1');
    });

    team2WinBtn.addEventListener('click', function() {
        updateScore('team2');
    });

    resetScoreBtn.addEventListener('click', function() {
        fetch('/reset-score', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                team1Score = 0;
                team2Score = 0;
                updateScoreDisplay();
            }
        });
    });

    function updateScore(team) {
        fetch('/update-score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ team: team })
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                if (team === 'team1') {
                    team1Score++;
                } else {
                    team2Score++;
                }
                updateScoreDisplay();
            }
        });
    }

    function updateScoreDisplay() {
        team1ScoreDisplay.innerHTML = `Team 1 Score: ${team1Score}`;
        team2ScoreDisplay.innerHTML = `Team 2 Score: ${team2Score}`;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
