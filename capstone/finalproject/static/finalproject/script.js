
// Function Defining Section

//1. Tabbed Menu defining
function openMenu(evt, menuName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("menu");
    for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" w3-black", "");
    }
    document.getElementById(menuName).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-black";
}


//3. Toggle between showing and hiding the sidebar when clicking the menu icon
function w3_open() {
    var mySidebar = document.getElementById("mySidebar");
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
    } else {
        mySidebar.style.display = 'block';
    }
}

//4. Close the sidebar with the close button
function w3_close() {
mySidebar.style.display = "none";
}



//6. redirect to instagram in both instgram icons
function instagram(){
    location.href="https://www.instagram.com/maxyourworkout/?theme=dark";
}

//7. redirect to trainers instagram depending on who they click on
function trainer(trainerLink){
   location.href="https://www.instagram.com/"
   +trainerLink
   +"/?theme=dark";
}


//9. redirect to page to buy
function buyPack(pack_name){
    location.href="http://127.0.0.1:5000/"
    +pack_name
    +"/buy";
}

//10. redirect to app instalation
function app_install(fitr_code){
    location.href="https://app.fitr.training/plan/"
    +fitr_code
    +"/purchase?";
}

//11. navbar scroll hide
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
    } else {
        document.getElementById("navbar").style.top = '-300px';
    }
    prevScrollpos = currentScrollPos;
}


function change_nick() {
    const user = document.querySelector("#user").value;
    const nickname = document.querySelector("#nickname").value;
    document.querySelector("#profile-user").innerHTML = nickname;
    document.querySelector("#user-name-item").innerHTML = nickname;
    event.preventDefault();
    document.querySelector("#nickname").value = "";
    fetch(`nick/${user}`, {
        method: 'PUT',
        body: JSON.stringify({
            nickname: nickname
        })
    })
}

function close_ticket() {
    const id = document.querySelector("#id-ticket").value; 
    document.querySelector("#ticket-solved").innerHTML = "Status: Solved";
    document.querySelector("#close-button").remove();
    event.preventDefault();
    fetch(`/ticket/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            solved: true
        })
    })
}


function change_pass() {
    event.preventDefault();
    if (document.querySelector(".message-pass") !== null) {
        document.querySelector(".message-pass").remove()
    }
    const user = document.querySelector("#user").value;
    const password = document.querySelector("#password").value;
    const confirm = document.querySelector("#con_password").value;
    if (password != confirm) {
        const p = document.createElement('p');
        p.className = "message-pass";
        p.innerHTML = "Passwords did not match"
        document.querySelector("#password-form").append(p)

    }
    fetch(`search/pass/${user}`, {
        method: 'PUT',
        body: JSON.stringify({
            password: password
        })
    })
    .then(() => {
        const p = document.createElement('p');
        p.className = "message-pass";
        p.innerHTML = "Password changed"
        document.querySelector("#password-form").append(p)    
        document.querySelector("#con_password").value = '';
        document.querySelector("#password").value = '';
    })
    return false
}