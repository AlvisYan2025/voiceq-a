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


document.addEventListener('DOMContentLoaded', function () {
    const questions = document.querySelectorAll('.question');

    questions.forEach((question, index) => {
        if (index !== 0) {
            question.style.display = 'none';
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const recordButton = document.getElementById('microphone-button');
    
    let recording = false; 
    let audioContext;
    let input;
    let rec;
    let gumStream;

    // Event listener for the "Record" button
    recordButton.addEventListener('click', () => {
        recordButton.classList.toggle('recording');
        if (recording===true){
            rec.stop();
            gumStream.getAudioTracks()[0].stop();
            rec.exportWAV(sendAudioToServer);
            return 
        }
        recording =true;
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
            console.log('received transcript', transcript);
            const transcript_section = document.getElementById('transcript');
            transcript_section.innerText = transcript;
            const wr = document.getElementById('wr');
            const questions = document.querySelectorAll('.question');
            const currQuestion = questions[currentQuestionIndex];
            const correct_answer = currQuestion.id;
            if (correct_answer === transcript){
                wr.innerText = "correct!";
            }
            else{
                wr.innerText = "wrong!";
            }
        })  
        .catch(error => console.error(error));
    }
});