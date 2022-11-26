addEventListener('DOMContentLoaded', (event) =>{


    const like_button = document.querySelector('#post-like');

    let likes = document.querySelector('#post-likes');
    likes = likes.value.slice(0,1)
    

    like_button.addEventListener('click', () => {

        fetch(`/network/`, {
            method : 'PUT',
            likes : +1,
        })
        .then(response => response.json())
        .then(results => {

        })
    })



} )