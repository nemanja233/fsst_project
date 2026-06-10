import mysql.connector 
import pygame
import sys 
import pygame_textinput
import pygame_widgets
from pygame_widgets.button import Button 
from pygame_widgets.textbox import TextBox
from getpass import getpass

state = "main_menu"

def get_credentials():
    global params
    username = textinput.getText()
    password = pwd_input.getText()
    params=(username,password)
    return params

def new_user_credentials():
    global nu_params
    new_username = newuser.getText()
    new_password = newpwd.getText()
    nu_params=(new_username,new_password)
    print(f"New user credentials: {nu_params}")
    return nu_params

def main_menu():
    global login_button, new_user_button, guest_button, quit_button, state
    state = "main_menu"
    login_button = Button(screen, 100,100,150,50, text="Login", fontSize=30, onClick=show_login_screen)
    new_user_button = Button(screen, 300,100,150,50, text="New User", fontSize=30, onClick=create_user)
    guest_button = Button(screen, 500,100,150,50, text="Guest", fontSize=30, onClick=guest_access)
    quit_button = Button(screen, 0,height - 50,150,50, text="Quit", fontSize=30, onClick=sys.exit)

def show_login_screen():
    global textinput, pwd_input, state, new_login_button
    state = "login_screen"
    textinput = TextBox(screen, width//2 - 100, height//2 - 50, 200, 50, fontSize=30,onSubmit=get_credentials, placeholderText="Username")
    pwd_input = TextBox(screen, width//2 - 100, height//2 + 50, 200, 50, fontSize=30,onSubmit=get_credentials, placeholderText="Password")
    login_button.hide()
    new_user_button.hide()
    guest_button.hide()
    new_login_button = Button(screen, width//2 - 75, height//2 + 120, 150, 50, text="Login", fontSize=30, onClick=login_db)



def create_user():
    global newuser, newpwd, state, create_user_button
    state = "create_user"
    newuser = TextBox(screen, width//2 - 100, height//2 - 50, 200, 50, fontSize=30,onSubmit=new_user_credentials, placeholderText="Username")
    newpwd = TextBox(screen, width//2 - 100, height//2 + 50, 200, 50, fontSize=30,onSubmit=new_user_credentials, placeholderText="Password")
    login_button.hide()
    new_user_button.hide()
    guest_button.hide()
    create_user_button = Button(screen, width//2 - 75, height//2 + 120, 150, 50, text="Create User", fontSize=30,onClick=create_user_db)


def guest_access():
    global state
    state = "guest_access"
    login_button.hide()
    new_user_button.hide()
    guest_button.hide()


def connect_db():
    global connection
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='game',
                                             user='root',
                                             password='')

        if connection.is_connected():
            print("Connected to database")   
    except mysql.connector.Error as e:
        print(f"Failed to connect to database: {e}")

def close_db():
    if connection.is_connected():
        connection.close()
        print("Database connection closed")



def create_user_db():
    global state
    if connection.is_connected():
        cursor = connection.cursor()
        query = "INSERT INTO players (username, password) VALUES (%s, %s)"
        cursor.execute(query, new_user_credentials())           # Einfachste lösung den tupel weiter zu bekommen über den button ging es nicht es war buggy
        connection.commit()
        print("User created successfully")
        state = "created"
    else:
        print("Not connected to database")


def login_db():
    global state
    if connection.is_connected():
        cursor = connection.cursor()
        query = "SELECT * FROM players WHERE username=%s AND password=%s"
        cursor.execute(query, get_credentials())
        result = cursor.fetchone()
        if result:
            print(f"Login successful, welcome {result[1]}")
            state = "logged"
        else:
            print("Invalid credentials")
        close_db()  
        
            
pygame.init()
res=(720,360)
screen = pygame.display.set_mode(res)
clock=pygame.time.Clock()

width=screen.get_width()
height=screen.get_height()

def play_menu():            # Play or quit menu nach dem login oder guest access
    global play_button, quit_button, state
    if state == "logged":
        new_login_button.hide()
        textinput.hide()
        pwd_input.hide()
    elif state == "created":
        create_user_button.hide()
        newuser.hide()
        newpwd.hide()
    else:
        print("No valid state for play_menu")
    state = "play_menu"
    play_button = Button(screen, width//2 - 75, height//2 - 25, 150, 50, text="Play", fontSize=30, onClick=game)
    quit_button = Button(screen, width//2 - 75, height//2 + 50, 150, 50, text="Quit", fontSize=30, onClick=sys  .exit)


def start_menu():
    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                close_db()
            if state=="logged" or state=="created":
                play_menu()
            if state=="guest_access":
                play_menu()
            if state=="play_menu":
                pass
        screen.fill("blue")
        pygame_widgets.update(events)

        pygame.display.flip()
        clock.tick(60) / 1000


def game():
    global state
    running = True
    state = "game"
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                close_db()

        play_button.hide()      #Hide buttons when game starts
        quit_button.hide()      #------------||---------------


        

        screen.fill("green")
        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(60) / 1000


def main():
    connect_db()
    main_menu()
    start_menu()
    play_menu()

if __name__ == "__main__":
    main()