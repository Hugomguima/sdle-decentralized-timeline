from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import inquirer
from src.utils.logger import Logger


if TYPE_CHECKING:
    from src.api.user import UserActionInfo

class MainMenuAnswer(TypedDict):
    action: str
    information: UserActionInfo

class MainMenu:
    @staticmethod
    def menu() -> MainMenuAnswer:

        logger = Logger()
        
        print('\n--- Main Menu ---')
        questions = [
            inquirer.List('action', message="Please choose an action", choices=['New Post', 'Follow User', 'Unfollow User', 'View Timeline', 'Get Suggestions', 'Logout'],),
        ]

        answers = inquirer.prompt(questions)
        action = answers['action']

        result = {'action': action, 'information': {}}

        if action == 'New Post':
            logger.log("Post","info",'Post message')
            message = input('New Post: ')
            result['information']['message'] = message
        
        elif action == 'Follow User':
            logger.log("Follow","info",'Follow user')
            username = input('User to follow: ')
            result['information']['username'] = username

        elif action == 'Unfollow User':
            logger.log("Unfollow","info",'Unfollow user')
            username = input('User to unfollow: ')
            result['information']['username'] = username

        elif action == 'View Timeline':
            logger.log("View","info",'View Timeline')

        elif action == 'Get Suggestions':
            logger.log("Suggestions","info",'Get Suggestions')
        
        elif action == 'Logout':
            logger.log("Logout","info",'Logout! See you soon on Camellia')

        return result