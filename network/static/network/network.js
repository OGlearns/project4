document.addEventListener('DOMContentLoaded', function() {

    let post_view = document.querySelector('#posts-view');
    let follower_details = document.querySelector('#user-profile-details');
    
    post_view.addEventListener('click', (event) =>  {
        const is_like_img = event.target.nodeName === 'IMG';
        const is_button = event.target.nodeName === 'BUTTON';
        // const edit_button = event.target.parentNode.className === 'post-content';
        console.log(event.target.parentNode.className);
        if (is_like_img){
            update_likes(event);
        }
        else if (is_button) {
            // if (edit_button) {
            //     return
            // }
            // else {
                update_post(event);
            // }
        }
        else {
            return
        }
    });
    
    follower_details.addEventListener('click', (event) => {
        const is_button = event.target.nodeName === 'BUTTON';
        if (!is_button){
            return
        }
        else {
            follow(event);
        }
    });



});

function update_likes(event){
    
    // Get username of logged in user
    const username = document.querySelector('#username').innerHTML;

    let post_id = event.target.id
    console.log(post_id);
    console.log(username);

    fetch(`/update_likes`, {
        method : 'POST',
        body : JSON.stringify({
            username : username,
            id : post_id
        })
    })
    .then(response => response.json())
    .then(results => {
        // Do stuff depending on the message sent back.
        console.log(results);
        location.reload();
    });

}


function follow(event) {

    // Get the username of both the requesting user and the requested user
    const requesting_username = document.querySelector('#username').innerHTML.trim();
    console.log(requesting_username);
    const requested_username = document.querySelector('#user-profile-name').innerHTML.trim();
    // Fetch to the following url/function
    fetch(`/follow`, {
        method: 'POST',
        body : JSON.stringify({
            requesting_username: requesting_username,
            requested_username: requested_username,
        })
    })
    .then(response => response.json())
    .then(results => {
        console.log(results);
        location.reload();
    });
}


function update_post(event) {

    // Get the post ID
    const post_id = event.target.id;

    // clear edit button
    edit_button = document.querySelector(`.edit-post-${post_id}`);
    edit_button.style.display = 'none';

    // Get post content
    let post_details_div = event.target.parentNode;
    let content_div = post_details_div.previousElementSibling;

    let content = content_div.innerHTML.trim();
    
    let input_field = document.createElement('textarea');
    input_field.setAttribute('type','text');
    input_field.setAttribute('id',`new_content_${post_id}`);
    input_field.setAttribute('class','post-content input-group input-group-sm');
    input_field.style.width = '80%';
    input_field.style.display = 'inline-block';
    input_field.style.paddingBottom = '0px';
    // input_field.style.height = '45px';
    input_field.value = content;
    input_field.style.position = 'relative';
    input_field.setAttribute('maxlength', '200')

    let save_button = document.createElement('button');
    save_button.addEventListener('click', function () {
        save_post(post_id);
    });
    save_button.setAttribute('type', 'button');
    save_button.setAttribute('id', `save-post-${post_id}`);
    save_button.setAttribute('class','btn');
    save_button.style.position = 'absolute';
    save_button.innerHTML = 'Save';
    save_button.style.position = 'relative';
    
    let delete_button = document.createElement('button');
    delete_button.addEventListener('click', function () {
        cancel_update(content,post_id)} 
        );
    delete_button.setAttribute('type', 'button');
    delete_button.setAttribute('id', `cancel_update_${post_id}`);
    delete_button.setAttribute('class','btn');
    delete_button.innerHTML = 'Cancel';
    delete_button.style.position = 'relative';
     
    content_div.innerHTML = '';
    content_div.appendChild(input_field);
    content_div.appendChild(save_button);
    content_div.appendChild(delete_button);

    // Hide Edit button

    // Grow the post box to accomodate edit function
    let post_box = document.querySelector(`.post-box-${post_id}`);
    // post_box.style.height = '120%';

}

function cancel_update(content,post_id){
    // shrink back the post box 
    let post_box = document.querySelector(`.post-box-${post_id}`);
    // post_box.style.height = '90px';

    let content_div = document.querySelector(`#post-content-${post_id}`);
    content_div.innerHTML = content;

    // show edit button
    edit_button = document.querySelector(`.edit-post-${post_id}`);
    edit_button.style.display = 'block';
    

}

function save_post(post_id) {
    
    //GET new content
    const new_content = document.querySelector(`#new_content_${post_id}`).value;    
    console.log(new_content);
        // On submit, update post via fetch request
    fetch(`edit_post`, {
        method: 'PUT',
        body : JSON.stringify({
            post_id: post_id,
            new_content: new_content,
        })
    })
    .then(response => response.text())
    .then(results => {
        console.log(results);
        // location.reload();
    });
    
    // Set submit function attribute to SAVE link
    
    // Display the new content of the post as the content
    
    let post_details_div = document.querySelector(`#post-content-${post_id}`);

    post_details_div.innerHTML = new_content;

    // show edit button
    edit_button = document.querySelector(`.edit-post-${post_id}`);
    edit_button.style.display = 'block';

}