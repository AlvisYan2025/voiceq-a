function get_problem_sets(){
    const res = fetch('/ps').then((res)=>res.json()).then(data=>{
        const problem_sets = data['problem_sets']
        console.log(problem_sets)
        problem_sets.forEach(problem_set => {
            //create a new container to display each problem set
            const cardContainer = document.createElement('div');
            cardContainer.className = 'col-md-4';
            const card = document.createElement('div');
            card.className = 'card';
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';
            const title = document.createElement('h5');
            title.className = 'card-title';
            title.textContent = problem_set.name;
            const description = document.createElement('p');
            description.className = 'card-text';
            description.textContent = problem_set.description;
            const viewDetailsButton = document.createElement('a');
            viewDetailsButton.className = 'btn btn-primary';
            viewDetailsButton.href = `/question?qid=${problem_set.qid||'0000'}`;  
            viewDetailsButton.textContent = 'View Details';
            // Append elements to the card body
            cardBody.appendChild(title);
            cardBody.appendChild(description);
            cardBody.appendChild(viewDetailsButton);
            // Append card body to the card
            card.appendChild(cardBody);
            // Append the card to the card container
            cardContainer.appendChild(card);
            const card_list = document.getElementById("recent-ps-list");
            card_list.appendChild(cardContainer);
        });
    })
    
}
document.addEventListener('DOMContentLoaded',get_problem_sets)