document.addEventListener("DOMContentLoaded", function(){

  // Global variable to make a specific animation
  window.count = 0;

  // Global varible for users
  window.user = document.querySelector('#user').value;

  // Global variable for post creation
  creation = false;

  // Lookout for form submit and handle errors for non authenticated people
  const form = document.querySelector('#post-form');
  if (user !== 'AnonymousUser') {
    document.querySelector('#post-form').onsubmit = create_post;
  } else {
    document.querySelector('#new_post-container').style.border = 'none';
  }
});


// Create a post
function create_post() {

  // Prepare animation for new entry
  creation = true;

  // Set variables
  const body = document.querySelector('#content').value;

  // Post request pass body
  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);

    document.querySelector('#content').value = "";
    load_posts();
  })
  .catch(error => {
    console.log('Error:', error);
  });
  return false;
}


// Load all posts
function load_posts() {

  // Get posts
  fetch(`posts/all`)
  .then(response => response.json())
  .then(posts => {
    // Load a function that just uploads the most recent one
    add_post(posts[0]);
  })
  .catch(error => {
    console.log('Error:', error);
  });
}


// Function to create each individual post
function add_post(entry){
  
  // Create new div to insert post
  const post = document.createElement('div');
  post.className = `post post_${entry.id}`;

  // Only show edit button user is the author of the post
  post.innerHTML = `
  <a class="profile" href="/posts/all/${entry.author}"><h5 class="profile">${entry.author}</h5></a>
  <br>
  <p class="body body_${entry.id}">${entry.body}</p>
  <p class="timestamp">${entry.timestamp}</p>
  <p class="likes likes_${entry.id}"><image class="image" src="/static/network/like.png" alt="like"> ${entry.likes.length}</p>
  <button class="btn btn-primary edit edit_${entry.id}">Edit</button>
  `;

  // Append post
  document.querySelector('#post_container').prepend(post);
  post.style.animationPlayState = 'running';
  post.style.animationName = 'show';
  count ++
  post.addEventListener('animationend', () => {
    post.style.animationPlayState = 'paused';
    post.style.animationName = 'none';
  })

  // Remove last child so post count remains 10
  document.querySelector('#post_container').lastElementChild.remove();

  // Handle Another edit
  document.querySelector(`.edit_${entry.id}`).addEventListener('click', () => edit(entry.id));
}


// Function to handle edits
function edit(id){
  
  // Get post
  const post = document.querySelector(`.post_${id}`);

  // Get body (b) variable, replace with textarea
  const b = post.querySelector(`.body_${id}`);
  const t = document.createElement('textarea');
  t.innerHTML = b.innerHTML;
  t.className = `body body_${id} form-control`;
  b.replaceWith(t);

  // Fetch entry info
  fetch(`/posts/edit/${id}`)
  .then(response => response.json())
  .then(entry => {

    // Get the button and change to save
    var button = post.lastElementChild;
    button.innerHTML = 'Save';

    // Listen for the click to save, submit.
    button.addEventListener('click', () => {
      fetch(`/posts/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          body: t.value
        })
      })
      .then(response => response.json())
      .then(result => {
        console.log(result)

        // Change the initial body to be the new value, and replace textarea with the original tag, change button to edit
        post.innerHTML = `
        <a class="profile" href="/posts/all/${entry.author}"><h5 class="profile">${entry.author}</h5></a>
        <br>
        <p class="body body_${id}">${t.value}</p>
        <p class="timestamp">${entry.timestamp}</p>
        <p><image class="image" src="/static/network/like.png" alt="like"> ${entry.likes.length}</p>
        <button class="btn btn-primary edit edit_${id}" onclick="edit('${id}')">Edit</button>`
      })
      .catch(error => {
        console.log('Error', error)
      })
    })
  })
  .catch(error => {
    console.log('Error', error)
  })   
}


// Function to handle post likes
function like(id, author){

  // Fetch information about this post
  fetch(`/posts/get/${id}`)
  .then(response => response.json())
  .then(this_post => {

    // Add logic to handle counter
    var length = this_post.likes.length;
    const likes = this_post.likes;
    const button = document.querySelector(`.like_${id}`);
    const body = document.querySelector(`.body_${id}`).innerHTML;
    const timestamp = document.querySelector(`.timestamp_${id}`).innerHTML;
    const post = document.querySelector(`.post_${id}`);

    // Handle counter logic
    if (button.innerHTML === 'Like') {
      length = length + 1;
      var option = 'like'
    } else {
      length = length - 1;
      var option = 'unlike';
    }

    // Add user to the list of "likes"
    fetch(`/posts/${option}/${id}`)
    .then(response => response.json())
    .then(result => {
      console.log(result)
      
      // Update Content user will view
      post.innerHTML = `
      <a class="profile" href="/posts/all/${author}"><h5 class="profile">${author}</h5></a>
      <br>
      <p class="body body_${ id }"> ${body}</p>
      <p class="timestamp timestamp_${id}">${timestamp}</p>
      <p class="likes likes_${id}"><image class="image body" src="/static/network/like.png" alt"like"> ${length}</p>
      `;

      // Handle button logic
      button.innerHTML = (button.innerHTML === 'Like') ? 'Unlike' : 'Like';
      post.append(button)

    })
    .catch(error => {
      console.log('Error', error)
    })
  })
  .catch(error => {
    console.log('Error:', error);
  })
}