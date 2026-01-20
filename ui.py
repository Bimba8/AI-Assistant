import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

class UI:
    """Класс для красивого вывода в терминале"""
    
    @staticmethod
    def header():
        ascii_art = pyfiglet.figlet_format("AI Assistant", font="slant")
        print(Fore.CYAN + Style.BRIGHT + ascii_art)
        print(Fore.GREEN + "Welcome to AI Assistant!")
        print(Fore.MAGENTA + "Powered by Bimba")
        print(Fore.YELLOW + "v1.0.0 | Made with ❤️")
        
    @staticmethod
    def menu():
        """Главное меню"""
        print("\n" + Fore.YELLOW + "="*70)
        print(Fore.GREEN + Style.BRIGHT + "ГЛАВНОЕ МЕНЮ" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*70)
        print(Fore.GREEN + "1. 💬 Чат с ассистентом")
        print(Fore.BLUE + "2. 📝 Использовать шаблон")
        print(Fore.CYAN + "3. 📋 Список шаблонов")
        print(Fore.MAGENTA + "4. 💾 Сохранить разговор")
        print(Fore.LIGHTMAGENTA_EX + "5. 📂 Загрузить разговор")
        print(Fore.LIGHTBLUE_EX + "6. 📊 Статистика")
        print(Fore.LIGHTYELLOW_EX + "7. 🗑️  Очистить историю")
        print(Fore.LIGHTCYAN_EX + "8. 🔄 Сменить модель")
        print(Fore.RED + "9. 🚪 Выход")
        print(Fore.YELLOW + "="*70 + Style.RESET_ALL)
        
    @staticmethod
    def templates_menu(templates: list):
        """Меню шаблонов"""
        print("\n" + Fore.CYAN + "="*70)
        print(Fore.CYAN + Style.BRIGHT + "ДОСТУПНЫЕ ШАБЛОНЫ" + Style.RESET_ALL)
        print(Fore.CYAN + "="*70)
        for i, name in enumerate(templates, 1):
            display_name = name.replace("_", " ").title()
            print(Fore.GREEN + f"{i}. {display_name}")
        print(Fore.CYAN + "="*70 + Style.RESET_ALL)
        
    @staticmethod
    def success(msg: str):
        """Сообщение об успехе"""
        print(Fore.GREEN + Style.BRIGHT + "✓ " + msg + Style.RESET_ALL)
    
    @staticmethod
    def error(msg: str):
        """Сообщение об ошибке"""
        print(Fore.RED + Style.BRIGHT + "✗ " + msg + Style.RESET_ALL)
    
    @staticmethod
    def warning(msg: str):
        """Предупреждение"""
        print(Fore.YELLOW + "⚠️  " + msg + Style.RESET_ALL)
    
    @staticmethod
    def info(msg: str):
        """Информация"""
        print(Fore.BLUE + "ℹ️  " + msg + Style.RESET_ALL)
    
    @staticmethod
    def loading(msg: str = "Думаю..."):
        """Индикатор загрузки"""
        print(Fore.CYAN + "⏳ " + msg + Style.RESET_ALL, end=" ", flush=True)
    
    @staticmethod
    def input_prompt(prompt: str = "Выбор") -> str:
        """Запрос ввода"""
        return input(Fore.CYAN + f"\n{prompt}: " + Style.RESET_ALL).strip()
    
    @staticmethod
    def user_message(text: str):
        """Сообщение пользователя"""
        print(Fore.BLUE + Style.BRIGHT + "Вы: " + Style.RESET_ALL + text)
    
    @staticmethod
    def ai_message(text: str):
        """Ответ AI"""
        print(Fore.MAGENTA + Style.BRIGHT + "AI: " + Style.RESET_ALL + text)
    
    @staticmethod
    def divider():
        """Разделитель"""
        print(Fore.YELLOW + "-"*70 + Style.RESET_ALL)
    
    @staticmethod
    def clear_screen():
        """Очистка экрана (опционально)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')