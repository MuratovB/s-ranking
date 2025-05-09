const startSessionBtn = document.getElementById('startSessionBtn');
const chooseFirstBtn = document.getElementById('chooseFirst');
const chooseSecondBtn = document.getElementById('chooseSecond');

if (startSessionBtn) {
    startSessionBtn.addEventListener('click', function() {
        startSessionBtn.disabled = true;
        const sessionName = document.getElementById('sessionName').value;
        const playlistIdInput = document.getElementById('playlistId').value;
        const playlistId = extractId(playlistIdInput);

        if (!playlistId) {
            alert("No playlist id found");
            startSessionBtn.disabled = false;
            return;
        }

        if (sessionName.length < 4 || sessionName.length > 64) {
            alert("Session name is not correct length");
            startSessionBtn.disabled = false;
            return;
        }

        fetch('/start_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ playlist_id: playlistId, session_name: sessionName })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            localStorage.setItem('session_name', data.session_name);
            console.log(data);
            updateRankingUI(data.first_video, data.second_video, data.final_result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

function getVideos() {
    const sessionName = localStorage.getItem('session_name');

    return fetch(`/get_videos?session_name=${encodeURIComponent(sessionName)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateRankingUI(firstVideo, secondVideo, finalResult) {
    if (finalResult && finalResult.length > 0) {
        // Display final results using the same structure as your HTML template
        let resultsHTML = `
            <h1>Final Results</h1>
            <ul class="results-list">
        `;
        
        finalResult.forEach((video, index) => {
            resultsHTML += `
                <li class="result-item">
                    <span class="result-number">${index + 1}</span>
                    <img class="result-thumbnail" src="${video.thumbnail_url}" alt="${video.title}">
                    <a class="video-title" href="https://www.youtube.com/watch?v=${video.videoId}" target="_blank">
                        ${video.title}
                    </a>
                </li>
            `;
        });

        resultsHTML += `</ul>`;
        document.body.innerHTML = resultsHTML;
    } else {
        // Display the two videos for comparison
        document.body.innerHTML = `
            <div class="video-container">
                <div class="video-item">
                    <iframe 
                        width="560" 
                        height="315" 
                        src="https://www.youtube.com/embed/${firstVideo.videoId}" 
                        frameborder="0" 
                        allowfullscreen>
                    </iframe>
                    <a class="video-title" href="https://www.youtube.com/watch?v=${firstVideo.videoId}" target="_blank">
                        ${firstVideo.title}
                    </a>
                </div>
                <div class="video-item">
                    <iframe 
                        width="560" 
                        height="315" 
                        src="https://www.youtube.com/embed/${secondVideo.videoId}" 
                        frameborder="0" 
                        allowfullscreen>
                    </iframe>
                    <a class="video-title" href="https://www.youtube.com/watch?v=${secondVideo.videoId}" target="_blank">
                        ${secondVideo.title}
                    </a>
                </div>
            </div>
            <div class="button-container">
                <button id="chooseFirst">Choose First</button>
                <button id="chooseSecond">Choose Second</button>
            </div>
        `;

        const chooseFirstBtn = document.getElementById('chooseFirst');
        const chooseSecondBtn = document.getElementById('chooseSecond');

        chooseFirstBtn.disabled = false;
        chooseSecondBtn.disabled = false;

        // Reattach event listeners to the new buttons
        chooseFirstBtn.addEventListener('click', () => {
            sendRankingChoice(1);
        });

        chooseSecondBtn.addEventListener('click', () => {
            sendRankingChoice(0);
        });
    }
}

function sendRankingChoice(winner) {
    const sessionName = localStorage.getItem('session_name');

    const chooseFirstBtn = document.getElementById('chooseFirst');
    const chooseSecondBtn = document.getElementById('chooseSecond');
    
    if (chooseFirstBtn && chooseSecondBtn) {
        chooseFirstBtn.disabled = true;
        chooseSecondBtn.disabled = true;
    }

    fetch('/process_choice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ session_name: sessionName, winner: winner })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(() => {
        getVideos().then(dataObj => {
            console.log(dataObj);
            updateRankingUI(dataObj.first_video, dataObj.second_video, dataObj.final_result);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function extractId(playlistIdInput) {
    const regex = /[&?]list=([^&]+)/i;
    const match = playlistIdInput.match(regex);

    if (match) {
        const playlistId = match[1];
        return playlistId;
    } else if (!playlistIdInput.includes('&') && !playlistIdInput.includes('=') && playlistIdInput.length === 34) {
        return playlistIdInput;
    } else {
        return null;
    }
}
