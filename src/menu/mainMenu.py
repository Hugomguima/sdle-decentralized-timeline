import inquirer
from src.message import Header, Message

class MainMenu:
    @staticmethod
    def menu():
        print('--- Main Menu ---')
        questions = [
            inquirer.List('action', message="Please choose an action", choices=['follow', 'post', 'view', 'logout'],),
        ]

        answers = inquirer.prompt(questions)
        action = answers['action']

        result = {'action': action, 'information': {}}

        if action == 'post':
            print('Post message')
            message = input('New Post: ')
            result['information']['message'] = message
        
        elif action == 'follow':
            print('Follow user')
            username = input('User to follow: ')
            result['information']['username'] = username
        
        elif action == 'view':
            print('View message')
        
        elif action == 'logout':
            print('Logout')

        return result