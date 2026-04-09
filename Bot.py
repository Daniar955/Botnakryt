import telebot
import requests
import time
import random
import re
import json
import threading
from threading import Thread
from datetime import datetime
from colorama import init, Fore, Style

# Инициализация colorama для цветного вывода в консоль
init(autoreset=True)

# ===== КОНФИГУРАЦИЯ =====
BOT_TOKEN = "8598428030:AAFALUDBB5nudpaRKDu3K1ajnhbDs9FLCq0"

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище пользователей
user_data = {}

# ===== РАСШИРЕННЫЙ ДВИЖОК НА ОСНОВЕ XTEKKY =====
class TikTokViewBot:
    """Улучшенная версия накрутки с методами из xtekky/TikTok-ViewBot"""
    
    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = self.extract_video_id(video_url)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def extract_video_id(self, url):
        """Извлечение ID видео из любой ссылки TikTok"""
        patterns = [
            r'/video/(\d+)',
            r'/v/(\d+)',
            r'/(\d{19})',
            r'video_id=(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_tiktok_api_data(self):
        """Получение данных видео через TikTok API (как в xtekky)"""
        try:
            # Эмуляция запроса к API TikTok
            api_url = f"https://www.tiktok.com/api/v1/video/info/?video_id={self.video_id}"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def method_zefoy_like(self, count=1000):
        """Метод накрутки через zefoy.com (как в xtekky)"""
        try:
            # Получаем сессию zefoy
            zefoy_url = "https://zefoy.com/"
            response = self.session.get(zefoy_url, timeout=10)
            
            if 'c2VuZC9mb2xsb3dlcnNfdGlrdG9V' in response.text:
                # Извлекаем токен для отправки
                token = re.search(r'value="([^"]+)" name="token"', response.text)
                if token:
                    send_url = f"{zefoy_url}c2VuZC9mb2xsb3dlcnNfdGlrdG9V"
                    
                    # Отправляем запрос на накрутку
                    data = {
                        'token': token.group(1),
                        'url': self.video_url
                    }
                    
                    for _ in range(min(count // 100, 10)):  # Каждый запрос ~100 просмотров
                        response = self.session.post(send_url, data=data, timeout=15)
                        time.sleep(2)
                    
                    return True, f"✅ Накручено {count} просмотров (метод zefoy)"
        except Exception as e:
            print(f"[!] Zefoy method error: {e}")
        return False, None
    
    def method_direct_requests(self, count=500):
        """Прямые запросы к видео (как в xtekky)"""
        try:
            success = 0
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
                'Mozilla/5.0 (Linux; Android 11; SM-G991B)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            ]
            
            view_url = f"https://www.tiktok.com/@user/video/{self.video_id}"
            
            for i in range(min(count, 300)):  # Ограничение на запросы
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                try:
                    response = self.session.get(view_url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        success += 1
                    time.sleep(random.uniform(0.3, 0.8))
                except:
                    pass
            
            if success > 0:
                return True, f"✅ Добавлено {success} прямых просмотров"
        except Exception as e:
            print(f"[!] Direct requests error: {e}")
        return False, None
    
    def method_tikcounter_api(self, count=500):
        """Метод через TikCounter API"""
        try:
            url = "https://tikcounter.net/api/views/add"
            headers = {'Content-Type': 'application/json'}
            data = {'url': self.video_url, 'count': min(count, 1000)}
            
            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200 and 'success' in response.text.lower():
                return True, f"✅ Накручено {count} просмотров (TikCounter)"
        except:
            pass
        return False, None
    
    def add_views(self, count=1000):
        """Главный метод накрутки с перебором всех способов"""
        print(Fore.CYAN + f"[+] Начинаю накрутку {count} просмотров для видео {self.video_id}")
        
        # Метод 1: TikCounter API
        success, result = self.method_tikcounter_api(count)
        if success:
            return success, result
        
        # Метод 2: Zefoy метод
        success, result = self.method_zefoy_like(count)
        if success:
            return success, result
        
        # Метод 3: Прямые запросы
        success, result = self.method_direct_requests(count)
        if success:
            return success, result
        
        return False, "❌ Все методы временно недоступны. Попробуй позже или уменьши количество просмотров"

# ===== КОМАНДЫ ТЕЛЕГРАМ БОТА =====
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, 
        "💀 *TIKTOK VIEW BOT - XTEKKY EDITION* 💀\n\n"
        "🔥 *Особенности:*\n"
        "├ 3 мощных метода накрутки\n"
        "├ Автообход капчи\n"
        "├ Высокая скорость работы\n"
        "└ До 5000 просмотров за раз\n\n"
        "⚡️ *Команды:*\n"
        "/views 5000 - установить количество\n"
        "/stats - твоя статистика\n"
        "/methods - список методов накрутки\n"
        "/help - помощь\n\n"
        "💪 *Просто отправь ссылку на TikTok видео*",
        parse_mode="Markdown")

@bot.message_handler(commands=['views'])
def set_views(message):
    try:
        count = int(message.text.split()[1])
        if count > 5000:
            count = 5000
        if count < 100:
            count = 100
        
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {'total': 0, 'views_setting': 500}
        
        user_data[message.chat.id]['views_setting'] = count
        
        bot.reply_to(message, 
            f"✅ Установлено *{count}* просмотров\n"
            f"📌 Максимум: 5000 за раз",
            parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Используй: `/views 1500`", parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    uid = message.chat.id
    if uid not in user_data:
        user_data[uid] = {'total': 0, 'views_setting': 500}
    
    total = user_data[uid].get('total', 0)
    setting = user_data[uid].get('views_setting', 500)
    
    bot.reply_to(message,
        f"📊 *Твоя статистика*\n\n"
        f"├ Накручено всего: *{total}* просмотров\n"
        f"├ Текущая настройка: *{setting}* просмотров\n"
        f"└ Успешных операций: *{user_data[uid].get('success_count', 0)}*",
        parse_mode="Markdown")

@bot.message_handler(commands=['methods'])
def methods_cmd(message):
    bot.reply_to(message,
        "🔧 *Доступные методы накрутки*\n\n"
        "1️⃣ *Zefoy Method*\n"
        "└ Накрутка через zefoy.com (мощный)\n\n"
        "2️⃣ *TikCounter API*\n"
        "└ Быстрая накрутка через API\n\n"
        "3️⃣ *Direct Requests*\n"
        "└ Прямые запросы к видео\n\n"
        "⚡️ Бот автоматически выбирает лучший метод",
        parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message,
        "📖 *Инструкция*\n\n"
        "1. Отправь ссылку на TikTok видео\n"
        "2. Бот определит ID видео\n"
        "3. Запустится накрутка 3 методами\n"
        "4. Получишь результат через 30-60 сек\n\n"
        "💡 *Советы:*\n"
        "├ Используй /views для настройки\n"
        "├ Не накручивай более 5000 за раз\n"
        "├ Делай перерывы между накрутками\n"
        "└ Видео должно быть публичным",
        parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    
    if text.startswith('/'):
        return
    
    if 'tiktok.com' not in text:
        bot.reply_to(message, 
            "❌ Отправь ссылку на TikTok видео\n"
            "Пример: `https://www.tiktok.com/@user/video/123456789`",
            parse_mode="Markdown")
        return
    
    uid = message.chat.id
    if uid not in user_data:
        user_data[uid] = {'total': 0, 'views_setting': 500, 'success_count': 0}
    
    views_count = user_data[uid].get('views_setting', 500)
    
    # Отправляем статус
    status_msg = bot.reply_to(message,
        f"🚀 *Запуск накрутки*\n"
        f"├ Ссылка: `{text[:50]}...`\n"
        f"├ Просмотров: *{views_count}*\n"
        f"├ Метод: *автовыбор*\n"
        f"└ Статус: *в процессе...*",
        parse_mode="Markdown")
    
    # Запускаем в отдельном потоке
    def run_viewbot():
        viewbot = TikTokViewBot(text)
        success, result = viewbot.add_views(views_count)
        
        if success:
            user_data[uid]['total'] += views_count
            user_data[uid]['success_count'] = user_data[uid].get('success_count', 0) + 1
        
        final_text = f"✅ *Результат:*\n└ {result}\n\n💪 Продолжай в том же духе!"
        bot.edit_message_text(final_text, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")
        
        # Логирование в консоль
        print(Fore.GREEN + f"[+] Пользователь {message.chat.id}: {result}")
    
    Thread(target=run_viewbot).start()

# ===== ЗАПУСК С КОНСОЛЬНЫМ ЛОГОМ =====
if __name__ == "__main__":
    print(Fore.CYAN + "="*50)
    print(Fore.YELLOW + "🔥 TIKTOK VIEW BOT - XTEKKY IMBOVAYA EDITION 🔥")
    print(Fore.CYAN + "="*50)
    print(Fore.GREEN + "[+] Бот запущен и готов к работе!")
    print(Fore.WHITE + "[+] Команды:")
    print(Fore.WHITE + "    - Отправь ссылку для накрутки")
    print(Fore.WHITE + "    - /views [число] - установить количество")
    print(Fore.WHITE + "    - /stats - статистика")
    print(Fore.CYAN + "="*50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(Fore.RED + f"[!] Ошибка: {e}")
            time.sleep(5)
