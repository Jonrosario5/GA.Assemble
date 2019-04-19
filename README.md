# Project-03-JBB

# App Name: GA.ASSEMBLE()

GA.Assemble was designed for students of all kinds. Are you a wiz kid and know all your material? Then create events to showoff your knowledge base. Are you struggling in one particular lesson? Then attend an event that is based on that topic and learn from your peers. At GA.Assemble we want to build a community of learning and sharing.

---

## Technologies Used

- bcrypt==3.1.6
  -cffi==1.12.2
- Click==7.0
- Flask==1.0.2
- Flask-Bcrypt==0.7.1
- Flask-Login==0.4.1
- Flask-WTF==0.14.2
- itsdangerous==1.1.0
- Jinja2==2.10
- MarkupSafe==1.1.1
- peewee==3.9.2
- pycparser==2.19
- six==1.12.0
- Werkzeug==0.14.1
- WTForms==2.2.1

CSS Styling

Bulma.io

---

## Existing Features

Landing Page

- Authentication (User Log-In & Sign-Up)
  Sign-Up - On submission, will redirect to the login page
  Login - On submission, will redirec to user page

User Page

- Renders information based on Logged in User
  Displays
  Funcitionality

  - Username
  - User Image
  - Events User is hosting
    - Renders to the page based on events the user had created on the Main Page (Event Title, Location, Detail, Time)
    - Able to Read, Delete, and Update hosted events
  - Events User is Attending

    - Renders events the user has chosen to attend (Event Title, Location, Detail, Time)
    - Able to remove yourself from the event with an "Unattend" button

  - User Topics

    - Renders topics the user is following, with the ability to remove topics

  - Recommended Topics
    - Renders topics that the user can add to their interest list

Main Page

- Displays Upcoming Events in order of date( Sorted by nearest date - to furtherest date)
- Also displays whether a user is an attendee or host on the events card
- Displayed a tag for the event topic
- Displays current attendees on event card

  Funcitionality

  - User is also able to create an event
  - User is able to toggle Upcoming events by topics
  - User is able to subscibe(attend) events
  - User is able to unattend events they are attending

---

## Planned Features

Changes we would make to our project if we continued to work on it:

- Have user see "default" profile photo on their profile page before adding their own photo
- Include functionality for user to update their profile photo
- Send user a welcome email after creating an account
- More CSS Styling
- Add external API

---

##### Screenshot

---

#### Biggest Wins and Challenges

Wins

- Delivering on our MVP
- Displaying number of students interested in a topic
- Displaying attendees in the event card
- User-Topics table and editing User-Events (Due to the fact that 3 ids from 3 tables where needed to make the edit)

Challenges

- Deleting User-Event.
- Css Styling
- Heroku.

---
