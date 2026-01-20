import json
import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

class AIAssistant:
    def __init__(self, api_key: str, max_history: int):
        self.llm = ChatOpenAI(
            model = "meta-llama/llama-3.3-70b-instruct:free",
            openai_api_key = api_key,
            openai_api_base = "https://openrouter.ai/api/v1",
            temperature = 0.8   
        )
        self.max_history = max_history
        self.history = []
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты полезный личный ассистент."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        self.templates = {
            "code_explainer": PromptTemplate.from_template("""
            Ты опытный программист.

            Объясни следующий код простым языком:
            ```{language}
            {code}
            ```

            Объяснение должно быть понятно новичку.
            """),
            
            "code_reviewer": PromptTemplate.from_template("""
            Ты code reviewer.

            Проанализируй код:
            ```{language}
            {code}
            ```

            Найди:
            1. Потенциальные баги
            2. Проблемы производительности
            3. Нарушения best practices

            Предложи улучшения.
            """),
            
            "test_generator": PromptTemplate.from_template("""
            Ты тестировщик.
            
            Сгенерируй юнит-тесты для следующего кода:
            ```{language}
            {code}
            ```
            
            Тесты должны покрывать основные сценарии использования.
            """),
            
            "refactorer": PromptTemplate.from_template("""
            Ты опытный разработчик.
            
            Проведи рефакторинг следующего кода:
            ```{language}
            {code}
            ```
            
            Улучшения должны повысить читаемость и производительность.
            """),
            
            "documenter": PromptTemplate.from_template("""
            Ты технический писатель.
            
            Сгенерируй docstring для следующего кода:
            ```{language}            
            {code}
            ```
            
            Docstring должен быть подробным и соответствовать стандартам.
            """),
        }
    
    def chat(self, message: str) -> str:
        response = self.chain.invoke({
            "input": message,
            "chat_history": self.history
        })
        self.history.append(HumanMessage(content=message))
        self.history.append(AIMessage(content=response))
        self.history = self.history[-self.max_history:]
        return response
    
    def use_template(self, template_name: str, **kwargs) -> str:
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Шаблон с именем '{template_name}' не найден.")
        prompt = template.format(**kwargs)
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def get_history(self) -> List[Dict[str, str]]:
        formatted_history = []
        for msg in self.history:
            role = "User" if isinstance(msg, HumanMessage) else "AI"
            formatted_history.append({"role": role, "content": msg.content})
        return formatted_history
    
    def list_templates(self) -> List[str]:
        """Список доступных шаблонов"""
        return list(self.templates.keys())
    
    def save_conversation(self, filename: str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(self.get_history(), f, ensure_ascii=False, indent=2)
        print(f"История чата сохранена в {full_path}")
        return self
    
    def load_conversation(self, filename: str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        
        if not os.path.exists(full_path):
            print(f"Файл {full_path} не найден.")
            return self
        
        with open(full_path, 'r', encoding='utf-8') as f:
            loaded_history = json.load(f)
            self.history = []
            for msg in loaded_history:
                if msg['role'] == 'User':
                    self.history.append(HumanMessage(content=msg['content']))
                else:
                    self.history.append(AIMessage(content=msg['content']))
        print(f"История чата загружена из {full_path}")
        return self
    
    def clear_history(self):
        self.history = []
        return self
    
    def get_stats(self) -> Dict[str, int]:
        num_user_msgs = sum(1 for msg in self.history if isinstance(msg, HumanMessage))
        num_ai_msgs = sum(1 for msg in self.history if isinstance(msg, AIMessage))
        return {
            "total_messages": len(self.history),
            "user_messages": num_user_msgs,
            "ai_messages": num_ai_msgs,
            "memory_usage": f"{len(self.history)}/{self.max_history} messages"
        } 
        
    
    
    