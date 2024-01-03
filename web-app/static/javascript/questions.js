function addQuestion() {
    // get all question containers and clone the last one 
    var allQuestions = document.querySelectorAll('.question-container');
    var questionNumber = allQuestions.length + 1;
    var questionContainer = allQuestions[questionNumber-2]
    var newQuestionContainer = questionContainer.cloneNode(true);
    newQuestionContainer.querySelector('.card-title').textContent = 'Question ' + questionNumber;
    newQuestionContainer.querySelectorAll('textarea').forEach((text)=>text.value='');
    //remove previous add question button 
    console.log(allQuestions);
    console.log(questionNumber);
    const last_add_btn = allQuestions[questionNumber-2].querySelector('.add-another-question');
    last_add_btn.classList.add('hidden');
    //append new question
    document.getElementById('question-list').appendChild(newQuestionContainer);
}
function isTextareasEmpty() {
    var questionContainers = document.querySelectorAll('.question-container');
    var isEmpty = false;
    questionContainers.forEach(function(container, index) {
        var questionTextarea = container.querySelector('textarea[name="question"]');
        var answerTextarea = container.querySelector('textarea[name="answer"]');
        if (questionTextarea.value.trim() === '' || answerTextarea.value.trim() === '') {
            isEmpty = true;
            questionTextarea.classList.add('empty');
            answerTextarea.classList.add('empty');
        } else {
            questionTextarea.classList.remove('empty');
            answerTextarea.classList.remove('empty');
        }
    });
    return isEmpty;
}
function submit_question_set(evt) {
    console.log("evt",evt);
    evt.preventDefault();
    if (isTextareasEmpty()) {
        var messageParagraph = document.createElement('p');
        messageParagraph.textContent = 'Please fill in all textareas.';
        messageParagraph.style.color = 'red'; 
        document.getElementById('question-list').appendChild(messageParagraph);
        setTimeout(function () {
            messageParagraph.remove();
        }, 10000); 
        return 
    }
    var questionContainers = document.querySelectorAll('.question-container');
    // Array to store question objects
    var questionsArray = [];
    questionContainers.forEach(function(container, index) {
        console.log(container);
        var question = container.querySelector('textarea[name="question"]').value;
        var answer = container.querySelector('textarea[name="answer"]').value;
        var questionObject = {
            question: question,
            answer: answer,
        };
        questionsArray.push(questionObject);
    });
    // get name and description 
    const ps_name = document.querySelector('.form-name').value || 'new problem set';
    const ps_des = document.querySelector('.form-des').value || '';
    const url = '/upload';
    const options = {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'questions':questionsArray, 'name':ps_name, 'description':ps_des}),
    }
    fetch(url,options).then(()=>console.log('answers uploaded!')).then(()=>{window.location.href = "/";});
}

const submit_btn = document.getElementById('question-set-submit');
submit_btn.addEventListener('click',submit_question_set);