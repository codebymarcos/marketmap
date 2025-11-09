from cli.title import print_banner
from InquirerPy import inquirer
from colorama import init, Fore, Style
from functs.gerardb import generate_db
from functs.cleardb import clear_data

# Inicializar colorama
init(autoreset=True)

def main():
	print_banner("marketmap")
	print("\n\n")

	# menu inicial
	answer = inquirer.select(
		message="Escolha uma opção",
		choices=["criar base de dados", "limpar base de dados", "Opção 3"],
		default="criar base de dados"
	).execute()

	if answer == "criar base de dados":
		print(Fore.GREEN + "Você escolheu criar base de dados" + Style.RESET_ALL)
		generate_db()
	elif answer == "limpar base de dados":
		print(Fore.BLUE + "Você escolheu limpar base de dados" + Style.RESET_ALL)
		clear_data()
	elif answer == "Opção 3":
		print(Fore.YELLOW + "Você escolheu a Opção 3" + Style.RESET_ALL)

if __name__ == "__main__":
	main()