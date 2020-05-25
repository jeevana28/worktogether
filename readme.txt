------process-------
*****Python3 is required for this program to run*******

****** Better extract project folder from the following github repoitory. 
      As, venv folder here is deleted due to space constraints *********
        https://github.com/mak2812/worktogether
1) If venv is not created then create a virtual environment
    (This step is not required if it is downloaded from github)    
        $python -m venv venv
  
1) Activate virtual environment
    $venv\scripts\activate
2) Check if all the following requirements are satisfied, else install them
    django - 3.0.5      >pip install django
    pillow - 7.1.2      >pip install pillow
    six - 1.14.0        >pip install six
    django-crispy-forms - 1.9.0         >pip install django-crispy-forms
    django-bootstrap-modal-forms - 1.5.0        >pip install django-bootstrap-modal-forms

3) Run the following command to start webserver and open the local host
    python manage.py runserver

4) To register user has to enter his credentials:(Enter correct email as it will be verified)
    1) username
    2) password
    3) email
    4) group
    5) institute
5) User has to confirm his email by activating the link sent  to his email and Login
6) Now user can login with his credentials and open the group he was joined into during registration
7) User can connect with people in that group and message 
8) User can also post or comment if required
9) If you would like to test the options like message or notifications, either you can create other account or
   you can login with the following credentials if your group is App Development
      username = Doggy
      password = user1234
----------------------------