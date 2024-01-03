let currentQuestionIndex = 0;
function showNextQuestion() {
        const questions = document.querySelectorAll('.question');
        questions[currentQuestionIndex].style.display = 'none';
        currentQuestionIndex = (currentQuestionIndex + 1) % questions.length;
        questions[currentQuestionIndex].style.display = 'block';
}

function showPreviousQuestion() {
        const questions = document.querySelectorAll('.question');
        questions[currentQuestionIndex].style.display = 'none';
        currentQuestionIndex = (currentQuestionIndex - 1 + questions.length) % questions.length;
        questions[currentQuestionIndex].style.display = 'block';
}

function recordAudio() {
        alert('Recording audio...');
}

document.addEventListener('DOMContentLoaded', function () {
    const questions = document.querySelectorAll('.question');

    questions.forEach((question, index) => {
        if (index !== 0) {
            question.style.display = 'none';
        }
    });
});
    document.addEventListener('DOMContentLoaded', () => {
        const recordButton = document.getElementById('recordButton');
        const stopButton = document.getElementById('stopButton');

        let audioContext;
        let input;
        let rec;
        let gumStream;
        let audioChunks = [];

        // Event listener for the "Record" button
        recordButton.addEventListener('click', () => {
            // Disable the record button and enable the stop button
            recordButton.disabled = true;
            stopButton.disabled = false;

            // Request access to the user's microphone
            navigator.mediaDevices.getUserMedia({ audio: true, video: false })
                .then(stream => {
                    // Create an audio context and set up recording
                    audioContext = new AudioContext();
                    gumStream = stream;
                    input = audioContext.createMediaStreamSource(stream);
                    rec = new Recorder(input, { numChannels: 1 });
                    rec.record();
                })
                .catch(e => console.error(e));
        });

        // Function to stop recording and send the audio to the server
        function stop_record() {
            rec.stop();
            gumStream.getAudioTracks()[0].stop();
            rec.exportWAV(sendAudioToServer);
        }

        // Function to send audio data to the server using fetch API
        function sendAudioToServer(blob) {
            const formData = new FormData();
            formData.append('audio_data', blob, 'audio.wav');

            fetch('/upload-audio', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Display the transcript, correctness, and correct answer
                const transcript = data.transcript;
                const transcript_text = document.getElementById('transcript');
                transcript_text.innerText = transcript;

                const isRight = data.isRight;
                const isRight_text = document.getElementById('isRight');
                isRight_text.innerText = isRight;
                // Update the class based on correctness
                isRight_text.className = 'result ' + (isRight === 'Correct!' ? 'correct' : 'wrong');

                const correct_answer_text = document.getElementById('correct_answer');
                correct_answer_text.innerText = data.correct_answer;

                console.log('received transcript');
            })
            .catch(error => console.error(error));
        }

        // Event listener for the "Stop" button
        stopButton.addEventListener('click', () => {
            // Enable the record button and disable the stop button
            recordButton.disabled = false;
            stopButton.disabled = true;

            // Stop recording and send the audio to the server
            stop_record();
        });

        // Event listener for the "Next Question" button
        nextButton.addEventListener('click', () => {
            // Reload the page when the button is clicked
            location.reload();
        });
    });