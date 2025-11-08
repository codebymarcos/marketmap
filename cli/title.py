import pyfiglet

def print_banner(text: str):
	"""Imprime texto em ASCII art centralizado, azul e negrito, sempre na fonte 'big'."""
	import shutil
	ascii_banner = pyfiglet.figlet_format(text, font="big")
	width = shutil.get_terminal_size((80, 20)).columns
	BLUE_BOLD = "\033[1;94m"
	RESET = "\033[0m"
	for line in ascii_banner.splitlines():
		print(f"{BLUE_BOLD}{line.center(width)}{RESET}")

# Exemplo de uso:
if __name__ == "__main__":
	print_banner("marketmap")