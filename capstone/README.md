# Capstone
#### Distinctiveness and Complexity:
This project was built with the goal of completing CS50W. My topic of choice for the last project was create a website for my own buisiness. There should be noted that this website is not a sales platform, but a storefront to generate leads, allow users to see all ou services and information of the brand.
The complexity of this somewhat on the medium difficulty, mostly because most errors and problems that could be encountered through lack of experience were already figured out in previous projects, I can admit that the implementation of certain fuctions and characteristics was a bit faster than anticipated.

The following text will describe the website in order to justify its complexity.

As I said before, the goal is to create a website to generate leads. On the website we can see the information about the brand, the team, and services and a contact form in order to get in contact with the team (in order to generate leads). 
If we choose to see a pack, we will be reedirected to a page where we can see all the info about that pack, and other info about how to install the product's aplication as well as a link to buy the pack.

The option to add other packs was created via a django model, and can only be done on the admin website, since the website will be used by others persons other than me (the programmer), we thought it would suffice to have the django admin page layout to create packs. Nevertheless, other options were included on the website since they are not exclusive to the admin's account (described further down).

We opted to allow users to create their own accounts, the main purpose is to eventually migrate from the third party app we use to the website, and thus users have acess to their workout plans through the website without requiring a third party app. As I said previously, other functions that are not exclusive to the admin were adeed to the main website. Such as an option to change a user nickname and password.

Each user can acess their account profile by clicking on their name, and only the admin will be able to see on their profile all the pending tickets (requiring response). As explained on the video, the main objetive of the website and ticket system is not to directly awnser through this method, but get the prospect email in order to answer their ticket via email and eventually send commercials. After the admin repplied to the ticket, a "close ticket" button can be clicked in order to change the ticket from pending to solved.

This is the main funcionability of the website, allow to gather leads, provide a usefull and visually appealing explanation to the user about the products we are selling as well as the brand goals and objectives.

All the back-end was developed with django, and the front-end with javascript, so that after changing passwords or nicknames for instance, the website would display the information without the need to fully reaload the page. Other functions were done using javascript aswell, such as reedirecting the user to the respective team members instagram after clicking a button and allowing the navbar to colapse if the user scrolls down.

Through django, the website will get acess to the django data base where it will read all information about every pack, team member, every user, every ticket submitted, and will complete the html templates in order to display all the information that was asked for.

Cybersecurity was kept in mind, so that no other user could change another user's password or nickname.

As per specifications, the website was constructed having in mind mobile responsiveness, as such the <meta> and viewport tags were used to allow a better responsiveness from the website. When a pack is clicked i created a flexbox that shows a video and some information. Since this flexbox won't appear exactly the same on the desktop view and mobile view, through the use of some css we found a way to hide certain parts of the html depending on the device utilized, showing a version of this video and information that can be properly visualized on mobile devices.

A w3-school library was used to allow the use of css files.

After the explanation above, I can safely say that this project is different from anything created on CS50W, and that the functions created and utilized were a result of all the experience and knowledge learned throughout the course.

All images and videos on the website are from out buisiness brand.

The 'capstone' file includes the django settings and other setup files. The 'finalproject' is essencially the website. Inside, 'static/finalproject' includes all videos, photos, javascript and css utilized. 'migrations' is a django default folder that saves all migrations done, 'templated/finalproject' is the template folder than contains the overall layout and every html file utilized.

No other packages appart from the cs50w required ones were utilized on this project. Python3 was used.

In order to run the application the following command should be used 'python3 manage.py runserver' 

Thank you cs50 for yet another great course.

I wish you the best,

best regards,
Sérgio Garrido
