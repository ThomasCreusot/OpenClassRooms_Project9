# OpenClassRooms_Project9
Develop a Web application using Django


# Project presentation
The present project is the ninth one of the training course *Python Application Developer*, offered by OpenClassRooms and aims to *Develop a Web application using Django*.

The main goal is to develop a **Minimum Viable Product of a web application** wich allows users to **ask and post reviews about books/literature objects**.

This program must:
- follow the **specifications and wireframes** provided by LITReview (startup)
- use **venv** to create a virtual environment
- be compliant with **PEP8**
- have registration and login features 

The web applications allows the user to : 
- Signu up and log
- Create a ticket for asking a review
- Post a review (the number of review is limited to one per ticket)
- Follow other users (page dedicated, which displays all followers and followed users, with possibility to stop following a user)
- See a flow of tickets (from all users he/she folows and from him/herself + the corresponding review, no matter the writer) and reviews (from all users he/she folows and from him/herself)
- See a flow of tickets and reviews that the users posted him/herself, with the possibility to modify/delete them


# Project execution
To correctly execute the program, you need to activate the associated virtual environment which has been recorded in the ‘requirements.txt’ file.

## To create and activate the virtual environment 
Please follow theses instructions:

1. Open your Shell 
-Windows: 
>'windows + R' 
>'cmd'  
-Mac: 
>'Applications > Utilitaires > Terminal.app'

2. Find the folder which contains the program (with *cd* command)

3. Create a virtual environment: write the following command in the console
>'python -m venv env'

4. Activate this virtual environment : 
-Linux or Mac: write the following command in the console
>'source env/bin/activate'
-Windows: write the following command in the console 
>'env\Scripts\activate'

5. Install the python packages recorded in the *requirements.txt* file : write in the console the following command
>'pip install -r requirements.txt'

## To launch the server
Please follow this instruction
6. Execute the code : write the following command in the console (Python must be installed on your computer and virtual environment must be activated)
>'python manage.py runserver'

## To access to the web application
7. Open an internet browser and visit local host url ( http://127.0.0.1:8000/ )

8. If you have not an account on the web application yet, click on the 'S'inscrire' button (towards url: http://127.0.0.1:8000/signup/) and fill in the information

9. If you have an account on the web application, write your username and your password in the dedicated fields and then click on the 'Se connecter' button (towards url: http://127.0.0.1:8000/home/) 

10. You are connected, please enjoy the website
