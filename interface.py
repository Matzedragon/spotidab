from spotidab import *
from colorama import Fore, init, Style
from random import randrange


class interface:

    #Starting up + getting liked song/genres
    def __init__(self):
        choix = [""]
        tableau_couleur = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]
        self.title =( "\r\n" +
					"               _____             __  _     __      __  \r\n" +
					"              / ___/____  ____  / /_(_)___/ /___ _/ /_ \r\n" +
					"              \\__ \\/ __ \\/ __ \\/ __/ / __  / __ `/ __ \\\r\n" +
					"             ___/ / /_/ / /_/ / /_/ / /_/ / /_/ / /_/ /\r\n" +
					"            /____/ .___/\\____/\\__/_/\\__,_/\\__,_/_.___/ \r\n" +
					"                /_/                                    \r\n" +
					"")
        for line in self.title.splitlines():
            print(tableau_couleur[randrange(len(tableau_couleur))] + line)
        print(Style.RESET_ALL)

        print(Fore.WHITE + "\nplease write the username for this session you'll be redirected to a confirmation page: ", end='')
        username = input()
        self.myApp = spotidab(username)
        print(Fore.YELLOW + "getting all songs from liked...")
        print(Fore.GREEN)
        self.myApp.get_liked()
        print(Fore.YELLOW + "Getting all artists...\n")
        self.myApp.get_all_artist()
        print(Fore.GREEN + "Done\n")
        print(Fore.YELLOW + "Finding genres...(this may take a while)\n")
        self.myApp.find_genre()
        print(Fore.GREEN + "Done\n")
        self.myApp.clean()
        print("\n")

    def Menu_playlist(self):
        print(Fore.GREEN)
        self.myApp.afficher_genre()
        print(Fore.WHITE + "\nPlease chose what genre playlist u wanna create with the format (1 2 3 4 ...), type \"all\" if you wanna create a playlist for each genre")
        print("answer : ", end='')
        answerPlaylist = input()
        tableau_answer = getAnswer(answerPlaylist)
        self.myApp.create_playlist(tableau_answer)
        print(Fore.GREEN + "Done")
        self.suite()

    def suite(self):
        print(Fore.WHITE + "Do you want to create another playlist ? Y/N")
        answer = input()
        if answer == "Y" or answer == "y":
            self.Menu_playlist()
        elif answer != "N" and answer != "n":
            print(Fore.RED + "invalid input")
            self.suite()


def getAnswer(answer):
    tableau = answer.split()
    for i in range(len(tableau)):
        tableau[i] = int(tableau[i])
    return tableau

init()
myInterface = interface()
myInterface.Menu_playlist()
