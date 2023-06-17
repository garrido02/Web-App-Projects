document.addEventListener("DOMContentLoaded", function(){
  // Global variables
  window.user = document.querySelector('#user').value;
  const author = document.querySelector('#author').value;

  // Load user page
  get_author_info(author); 
  
});


function get_author_info(author){

  // Gather Profile info
  fetch(`/profile/${author}`)
  .then(response => response.json())
  .then(profile => {

    // Create a header
    const prof = document.querySelector('#header');
    prof.className = 'prof_header';
    prof.innerHTML = `
    <div id="profile-header">
      <image src="/static/network/noimage.png" alt="no-image">
      <h4>${author}<h4>
    </div>
    <div id="profile-counters">
      <div id="left">
        <p class="followers">Followers</p>
        <p class="follower-count">${profile[0].followers.length}</p>
      </div>
      <div id="right">
        <p class="following">Following</p>
        <p class="following-count">${profile[0].following.length}</p>
      </div>
    </div>
    `;

    // Add follow button
    follow_button(author, profile);
  })
  .catch(error => {
    console.log('Error:', error);
  })
}


// Add follow button
function follow_button(author, profile) {

  // Set variable equal to followers
  const followers = profile[0].followers;

  // Check if user is following author and change button html accordingly 
  const container = document.createElement('div');
  container.className = 'button-container';

  const follow = document.createElement('button');
  follow.className ="btn btn-primary";
  follow.innerHTML = followers.includes(user) ? 'Unfollow' : 'Follow';
    
  // Append button only if user is not author
  if (user != author && user != 'AnonymousUser'){
    document.querySelector('#header').append(container);
    document.querySelector('.button-container').append(follow);
  }

  follow.addEventListener('click', () => {

    // Implement follow button action
    fetch(`/profile/${author}/${follow.innerHTML}`)
    .then(response => response.json())
    .then(() => {

      // Update follow count
      if (follow.innerHTML === 'Follow') {
        profile[0].followers.length += 1;
        document.querySelector('.follower-count').innerHTML = profile[0].followers.length;
      } else {
        profile[0].followers.length -= 1;
        document.querySelector('.follower-count').innerHTML = profile[0].followers.length;
      }

      // Change button to display correct action
      follow.innerHTML = (follow.innerHTML === 'Unfollow') ? 'Follow': 'Unfollow';
    })
    .catch(error => {
      console.log(error);
    })
  });
} 


// Function to handle edits
function edit(id){
  
  // Get post
  const post = document.querySelector(`.post_${id}`);

  // Get body (b) variable, replace with textarea
  const b = post.firstElementChild;
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
        post.innerHTML = `<p class="body body_${ id }">${t.value}</p>
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
function like(id){

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