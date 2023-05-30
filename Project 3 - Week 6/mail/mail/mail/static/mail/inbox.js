document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // If form is submitted, redirect to send mail function
  document.querySelector('#compose-form').onsubmit = send_mail;
});

function compose_email(entry) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#inside-view').style.display = 'none';

  // Check if is reply
  if (entry['id'] === undefined) {
    // Clear out composition fields if no entry
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    
  } else {
    document.querySelector('#compose-recipients').value = `${entry['sender']}`;
    // Check if it's first reply
    if (entry['subject'].includes('Re:')) {
      document.querySelector('#compose-subject').value = `${entry['subject']}`;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${entry['subject']}`;
    }
    document.querySelector('#compose-body').value = `On ${entry['timestamp']} ${entry['sender']} wrote: ${entry['body']}`;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#inside-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Each email corresponds to a entry and redirects to add_mail, passing the correspondent mailbox
    emails.forEach(function(email) {
      email = add_mail(email, mailbox)
    });
  })
  .catch(error => {
    console.log('Error:', error);
  });
}

function add_mail(entry, mailbox) {

  // Create new div and insert contents
  const mail = document.createElement('div');
  mail.className = 'mail';
  mail.innerHTML = `From: ${entry['sender']} | Subject: ${entry['subject']} | ${entry['timestamp']}`;
  mail.addEventListener('click', () => {

    // Listen for email click, pass email id and correspondent mailbox 
    view_mail(entry['id'], mailbox);
  });

  // Change colors depending on read status
  if (entry['read'] === false) {
    mail.style.background = "white";  
  } else {
    mail.style.background = "#909090";
  }

  // Add to view
  document.querySelector('#emails-view').append(mail);
}

function send_mail() {

  // Set variables
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Post request to /emails, pass recipients, subject, body
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    // print
    console.log(result);
    load_mailbox('sent');
  })
  .catch(error => {
    console.log('Error:', error);
  });
  return false;
}

function view_mail(id, mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#inside-view').style.display = 'block';

  // Get email through the id
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(entry => {
    
    // Add email content to div
    const mail = document.querySelector('#inside-view');
    mail.className = "inside-content"
    mail.innerHTML = 
    `<h2>${entry['subject']}</h2>
    <br>
    <div class="list-group-item"><b>From:</b> ${entry['sender']}</div>
    <div class="list-group-item"><b>To:</b> ${entry['recipients']}</div>
    <div class="list-group-item"><b>Date:</b> ${entry['timestamp']}</div>
    <div class="list-group-item"><b>Subject:</b> ${entry['subject']}</div>
    <br><br>
    <div id="body">${entry['body']}</div>
    <br><br>
    `;

    // Update read to true
    if (!entry['read']) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    // Archive button
    const archive = document.createElement('button');
    archive.innerHTML = entry['archived'] ? 'Unarchive' : 'Archive';
    archive.className = 'btn-primary btn';

    // Make archive button only available in inbox and archive
    if(mailbox !== 'sent') {
      document.querySelector('#inside-view').append(archive);
    }

    // Archive (on click) handler, change value to False or True
    archive.addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !entry['archived']
        })
      })
      .then(() => {
        load_mailbox('inbox')
      })
    })

    // Add Reply button
    const reply = document.createElement('button');
    reply.className = 'btn btn-primary';
    reply.innerHTML = 'Reply';

    // Make reply button only available on inbox and archive
    if (mailbox !== 'sent') {
      document.querySelector('#inside-view').append(reply);
    }
    
    // Add reply on click handler
    reply.addEventListener('click', () => {
      compose_email(entry);
    })
  })

  .catch(error => {
    console.log('Error:', error);
  });
}