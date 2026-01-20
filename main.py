from colorama import Fore, Style
from ai_assistant import AIAssistant
from ui import UI
from config import (
    OPENROUTER_API_KEY, 
    HISTORY_DIR, 
    DEFAULT_MAX_HISTORY, 
    AVAILABLE_MODELS
)

def get_api_key() -> str:
    """Получить API ключ"""
    if OPENROUTER_API_KEY:
        return OPENROUTER_API_KEY
    
    UI.warning("API ключ не найден в переменных окружения.")
    key = UI.input_prompt("Пожалуйста, введите ваш OpenRouter API ключ: ")
    if not key:
        UI.error("API ключ обязателен для работы ассистента.")
        exit(1)
    return key

def chat_mode(assistant:AIAssistant):
    """Режим чата с ассистентом"""
    UI.info("Вход в режим чата. Введите 'exit' для выхода.")
    UI.divider()
    
    while True:
        message = UI.input_prompt("Вы: ")
        
        if message.lower() == 'exit':
            UI.info("Выход из режима чата.")
            break
        
        if not message:
            UI.warning("Пустое сообщение. Пожалуйста, введите текст.")
            continue
        
        try:
            UI.loading()
            response = assistant.chat(message)
            print()
            UI.ai_message(response)
            UI.divider()
        except Exception as e:
            UI.error(f"Ошибка при общении с ассистентом: {e}")
            
def template_mode(assistant:AIAssistant):
    """Режим использования шаблонов"""
    templates = assistant.list_templates()
    UI.templates_menu(templates)
    
    choice = UI.input_prompt("Выберите шаблон по номеру (или 'exit' для выхода): ")
    
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(templates):
            UI.error("Неверный выбор шаблона.")
            return
        
        template_name = templates[idx]
        
        # Запрашиваем параметры
        language = UI.input_prompt("Введите язык программирования (например, python, javascript): ")
        print(Fore.CYAN + "Введите код (завершите ввод пустой строкой):")
        
        code_lines = []
        while True:
            line = input()
            if line == "":
                break
            code_lines.append(line)
        
        code = "\n".join(code_lines)
        
        if not code:
            UI.warning("Код не может быть пустым.")
            return
        
        UI.loading("Генерация результата...")
        result = assistant.use_template(template_name, language=language, code=code)
        print()
        UI.ai_message(result)
        
    except ValueError:
        UI.error("Пожалуйста, введите корректный номер шаблона.")
    except Exception as e:
        UI.error(f"Ошибка при использовании шаблона: {e}")
        
def save_conversation(assistant: AIAssistant):
    """Сохранить разговор"""
    filename = UI.input_prompt("Имя файла (без расширения)")
    if not filename:
        UI.warning("Имя файла не может быть пустым")
        return
    
    filepath = HISTORY_DIR / f"{filename}.json"
    try:
        assistant.save_conversation(str(filepath))
        UI.success(f"Разговор сохранен: {filepath}")
    except Exception as e:
        UI.error(f"Ошибка сохранения: {e}")

def load_conversation(assistant: AIAssistant):
    """Загрузить разговор"""
    # Показать доступные файлы
    files = list(HISTORY_DIR.glob("*.json"))
    
    if not files:
        UI.warning("Нет сохраненных разговоров")
        return
    
    print(Fore.CYAN + "\nДоступные файлы:")
    for i, file in enumerate(files, 1):
        print(Fore.GREEN + f"{i}. {file.stem}")
    
    choice = UI.input_prompt("Выберите файл (номер или имя)")
    
    try:
        # Попробуем как номер
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            filepath = files[idx]
        else:
            UI.error("Неверный номер")
            return
    except ValueError:
        # Если не номер, то имя файла
        filepath = HISTORY_DIR / f"{choice}.json"
        if not filepath.exists():
            UI.error(f"Файл не найден: {filepath}")
            return
    
    try:
        assistant.load_conversation(str(filepath))
        UI.success(f"Разговор загружен: {filepath.stem}")
    except Exception as e:
        UI.error(f"Ошибка загрузки: {e}")

def show_stats(assistant: AIAssistant):
    """Показать статистику"""
    try:
        stats = assistant.get_stats()
        
        UI.divider()
        print(Fore.CYAN + Style.BRIGHT + "📊 СТАТИСТИКА" + Style.RESET_ALL)
        UI.divider()
        print(Fore.GREEN + f"Всего сообщений: {stats['total_messages']}")
        print(Fore.BLUE + f"Сообщений пользователя: {stats['user_messages']}")
        print(Fore.MAGENTA + f"Ответов AI: {stats['ai_messages']}")
        print(Fore.YELLOW + f"Использование памяти: {stats['memory_usage']}")
        UI.divider()
    except Exception as e:
        UI.error(f"Ошибка получения статистики: {e}")

def change_model(assistant: AIAssistant):
    """Сменить модель"""
    print(Fore.CYAN + "\nДоступные модели:")
    for key, (model, desc) in AVAILABLE_MODELS.items():
        print(Fore.GREEN + f"{key}. {desc}")
    
    choice = UI.input_prompt("Выберите модель")
    
    if choice in AVAILABLE_MODELS:
        model_id, model_name = AVAILABLE_MODELS[choice]
        assistant.llm.model_name = model_id
        UI.success(f"Модель изменена на: {model_name}")
    else:
        UI.error("Неверный выбор")

def main():
    """Главная функция"""
    UI.header()
    
    # Получить API ключ
    api_key = get_api_key()
    
    # Создать ассистента
    try:
        assistant = AIAssistant(api_key, max_history=DEFAULT_MAX_HISTORY)
        UI.success("AI Assistant инициализирован!")
        UI.info("Модель: Llama 3.3 70B")
        UI.info(f"Максимум истории: {DEFAULT_MAX_HISTORY} сообщений")
    except Exception as e:
        UI.error(f"Ошибка инициализации: {e}")
        return
    
    # Главный цикл
    while True:
        UI.menu()
        choice = UI.input_prompt()
        
        if choice == "1":
            chat_mode(assistant)
        
        elif choice == "2":
            template_mode(assistant)
        
        elif choice == "3":
            templates = assistant.list_templates()
            UI.templates_menu(templates)
        
        elif choice == "4":
            save_conversation(assistant)
        
        elif choice == "5":
            load_conversation(assistant)
        
        elif choice == "6":
            show_stats(assistant)
        
        elif choice == "7":
            confirm = UI.input_prompt("Точно очистить? (yes/no)")
            if confirm.lower() == "yes":
                assistant.clear_history()
                UI.success("История очищена")
            else:
                UI.info("Отменено")
        
        elif choice == "8":
            change_model(assistant)
        
        elif choice == "9":
            UI.info("До встречи! 👋")
            break
        
        else:
            UI.error("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        UI.info("Программа прервана пользователем. До встречи! 👋")
    except Exception as e:
        UI.error(f"Критическая ошибка: {e}")