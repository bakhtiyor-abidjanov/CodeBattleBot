import sqlite3
import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

TOKEN = '7218896561:AAHgsjCHHyzfHUF54je-KbyHgY-4Jzfi37U'
bot = Bot(token=TOKEN)
dp = Dispatcher()
user_language = {}

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    language TEXT,
    score INTEGER DEFAULT 0
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER
)
''')
conn.commit()

tasks = {
    'Oson': {
        'Sum of Two Numbers': [
            'Given two numbers, return their sum.',
            'def sum(a, b): return a + b',  
            'def sum(a, b): return a * b',  
            'def sum(a, b): return a - b',  
            1,  
            'No'  
        ],
        'Reverse String': [
            'Write a function that reverses a string.',
            'def reverse_string(s): return s[::-1]', 
            'def reverse_string(s): return s',  
            'def reverse_string(s): return s[::-2]',  
            1,  
            'No'  
        ],
        'Add Two Arrays': [
            'Write a function to add corresponding elements of two arrays.',
            'def add_arrays(arr1, arr2): return [a + b for a, b in zip(arr1, arr2)]',  
            'def add_arrays(arr1, arr2): return [a - b for a, b in zip(arr1, arr2)]',  
            'def add_arrays(arr1, arr2): return [a * b for a, b in zip(arr1, arr2)]', 
            1,  
            'No'  
        ],
        'Is Even': [
            'Write a function that checks if a number is even.',
            'def is_even(n): return n % 2 == 0', 
            'def is_even(n): return n % 2 != 0',  
            'def is_even(n): return n // 2',  
            1, 
            'No'  
        ],
        'Count Vowels': [
            'Write a function to count the number of vowels in a string.',
            'def count_vowels(s): return sum(1 for c in s if c in "aeiouAEIOU")',
            'def count_vowels(s): return len(s)',  
            'def count_vowels(s): return sum(1 for c in s if c not in "aeiouAEIOU")', 
            1, 
            'No' 
        ],
        'Find Maximum': [
            'Given an array of numbers, find the maximum value.',
            'def find_max(arr): return max(arr)', 
            'def find_max(arr): return min(arr)', 
            'def find_max(arr): return sum(arr)',  
            1, 
            'No'
        ],  
        'Multiply Numbers': [
            'Write a function that multiplies two numbers.',
            'def multiply(a, b): return a * b', 
            'def multiply(a, b): return a + b',  
            'def multiply(a, b): return a - b', 
            1,  
            'No'  
        ],
        'Check Palindrome': [
            'Write a function to check if a string is a palindrome.',
            'def is_palindrome(s): return s == s[::-1]',  
            'def is_palindrome(s): return s == s[::2]',  
            'def is_palindrome(s): return s != s[::-1]', 
            1,  
            'No'  
        ],
        'Factorial': [
            'Write a function that returns the factorial of a number.',
            'def factorial(n): return 1 if n == 0 else n * factorial(n - 1)', 
            'def factorial(n): return n * n', 
            'def factorial(n): return n + 1',  
            1,  
            'No'  
        ],
        'Fibonacci Sequence': [
            'Write a function to return the nth Fibonacci number.',
            'def fibonacci(n): return n * (n-1)', 
            'def fibonacci(n): return n * n',
            'def fibonacci(n): return fibonacci(n-1) + fibonacci(n-2)', 
            3, 
            'No'  
        ]
    },

    'O\'rtacha': {
        'Find Minimum': [
            'Given an array of numbers, find the minimum value.',
            'def find_min(arr): return max(arr)',
            'def find_min(arr): return min(arr)', 
            'def find_min(arr): return sum(arr)',  
            2,  
            'No' 
        ],
        'Sum of Digits': [
            'Write a function to calculate the sum of digits of a number.',
            'def sum_digits(n): return sum(int(digit) for digit in str(n))',  
            'def sum_digits(n): return int(str(n))',  
            'def sum_digits(n): return len(str(n))',  
            1,  
            'No' 
        ],
        'Count Words': [
            'Write a function to count the number of words in a string.', 
            'def count_words(s): return len(s)',  
            'def count_words(s): return len(s.split("a"))',
            'def count_words(s): return len(s.split())',  
            3,  
            'No'  
        ],
        'Product of Array': [
            'Write a function to find the product of all elements in an array.',
            'def product(arr): return sum(arr)', 
            'def product(arr): return max(arr)',
            'def product(arr): return reduce(lambda x, y: x * y, arr)', 
            3,  
            'No'  
        ],
        'Count Odd Numbers': [
            'Write a function to count how many odd numbers are in an array.',  
            'def count_odd(arr): return len(arr) - sum(1 for x in arr if x % 2 == 0)',  
            'def count_odd(arr): return sum(1 for x in arr if x % 2 != 0)',
            'def count_odd(arr): return len(arr) // 2', 
            2,  
            'No'  
        ],
        'Anagram Check': [
            'Write a function to check if two strings are anagrams.',
            'def are_anagrams(str1, str2): return str1 == str2', 
            'def are_anagrams(str1, str2): return len(str1) == len(str2)',
            'def are_anagrams(str1, str2): return sorted(str1) == sorted(str2)',  
            3, 
            'No'  
        ],
        'Merge Arrays': [
            'Write a function to merge two sorted arrays.',  
            'def merge(arr1, arr2): return arr1 + arr2',
            'def merge(arr1, arr2): return sorted(arr1 + arr2)', 
            'def merge(arr1, arr2): return arr1 * arr2', 
            2,  
            'No'  
        ],
        'Remove Duplicates': [
            'Write a function to remove duplicates from a list.',
            'def remove_duplicates(lst): return list(set(lst))',
            'def remove_duplicates(lst): return lst[::-1]',  
            'def remove_duplicates(lst): return lst',  
            1,  
            'No' 
        ],
        'Find Common Elements': [
            'Write a function to find common elements in two arrays.',  
            'def find_common(arr1, arr2): return list(set(arr1) | set(arr2))',
            'def find_common(arr1, arr2): return list(set(arr1) & set(arr2))', 
            'def find_common(arr1, arr2): return arr1 + arr2', 
            2,  
            'No' 
        ],
        'Find Pair with Given Sum': [
            'Given an array of numbers, find two elements that sum up to a given target.', # Вариант 1
            'def find_pair(arr, target): return [(x, y) for x in arr for y in arr if x - y == target]',  # Вариант 2
            'def find_pair(arr, target): return [(x, y) for x in arr for y in arr if x * y == target]',
            'def find_pair(arr, target): return [(x, y) for x in arr for y in arr if x + y == target]',   # Вариант 3
            3,  
            'No'  
        ]
    },

    'Qiyin': {
        'Longest Substring Without Repeating Characters': [
            'Given a string, find the length of the longest substring without repeating characters.', 
            'def longest_substring(s): return len(s) - len(set(s))',
            'def longest_substring(s): return len(set(s))', 
            'def longest_substring(s): return sum(map(len, s))', 
            2,  
            'No' 
        ],
        'Median of Two Sorted Arrays': [
            'Find the median of two sorted arrays.',
            'def find_median(arr1, arr2): return (arr1[len(arr1)//2] + arr2[len(arr2)//2]) / 2',  
            'def find_median(arr1, arr2): return sum(arr1 + arr2) / len(arr1 + arr2)',  
            'def find_median(arr1, arr2): return max(arr1[0], arr2[0])',  
            1,  
            'No' 
        ],
        'Find the Intersection of Two Arrays': [
            'Write a function to find the intersection of two arrays.',
            'def intersection(arr1, arr2): return list(set(arr1) & set(arr2))', 
            'def intersection(arr1, arr2): return list(set(arr1) | set(arr2))',  
            'def intersection(arr1, arr2): return arr1 + arr2',  
            1,  
            'No'  
        ],
        'Reverse Words in a String': [
            'Write a function to reverse words in a string.',  
            'def reverse_words(s): return s[::-1]', 
            'def reverse_words(s): return s.split() + s.split()[::-1]',
            'def reverse_words(s): return " ".join(s.split()[::-1])',  
            3, 
            'No' 
        ],
        'Find All Pairs That Add Up to a Target Sum': [
            'Given an array of numbers, find all pairs of numbers that add up to a given target sum.',
            'def find_pairs(arr, target): return [(x, y) for x in arr for y in arr if x - y == target]',
            'def find_pairs(arr, target): return [(x, y) for x in arr for y in arr if x + y == target]',
            'def find_pairs(arr, target): return [(x, y) for x in arr for y in arr if x * y == target]',  
            2,  
            'No'  
        ],
        'Unique Paths in a Grid': [
            'In a m x n grid, find the number of unique paths from the top-left corner to the bottom-right corner.',
            'def unique_paths(m, n): return math.comb(m + n - 2, m - 1)',  
            'def unique_paths(m, n): return m * n',  
            'def unique_paths(m, n): return m + n',  
            1,  
            'No'  
        ],
        'Find the kth Largest Element in an Array': [
            'Write a function to find the kth largest element in an array.',
            'def kth_largest(arr, k): return sorted(arr, reverse=True)[k-1]',  
            'def kth_largest(arr, k): return sorted(arr)[k-1]', 
            'def kth_largest(arr, k): return max(arr)',  
            1,  
            'No'  
        ],
        'Find the Longest Common Prefix': [
            'Write a function to find the longest common prefix in an array of strings.',
            'def longest_common_prefix(strs): return os.path.commonprefix(strs)',  
            'def longest_common_prefix(strs): return min(strs)', 
            'def longest_common_prefix(strs): return max(strs)', 
            1, 
            'No' 
        ],
        'Find Missing Number in an Array': [
            'Given an array of n-1 numbers in the range 1 to n, find the missing number.',
            'def find_missing_number(arr, n): return n * (n + 1) // 2 - sum(arr)', 
            'def find_missing_number(arr, n): return min(arr)', 
            'def find_missing_number(arr, n): return max(arr)',
            1,  
            'No'  
        ],
        'Valid Parentheses': [
            'Write a function to check if a string contains valid parentheses.',
            'def is_valid(s): return s.count("(") == s.count(")")',
            'def is_valid(s): return s == s[::-1]', 
            'def is_valid(s): return s[::2] == "()"',  
            2,  
            'No' 
        ]
    }
}

difficulty_map = {
    "Лёгкие": "Oson",
    "Средние": "O'rtacha",
    "Сложные": "Qiyin",
    "Easy": "Oson",
    "Medium": "O'rtacha",
    "Hard": "Qiyin"
}


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Узбекский", callback_data="lang_uz")
    builder.button(text="Русский", callback_data="lang_ru")
    builder.button(text="English", callback_data="lang_en")

    await message.answer("Tilni tanlang / Выберите язык / Choose a language", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def process_language(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_language[user_id]=callback_query.data.split('_')[1]
    language = callback_query.data.split('_')[1]
    

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (id, name, language) VALUES (?, ?, ?)", 
                       (user_id, callback_query.from_user.full_name, language))
        conn.commit()
    builder = InlineKeyboardBuilder()
    await callback_query.answer()
    if language=='ru':
        await callback_query.message.answer(f"Вы выбрали язык: {language.capitalize()}")
        builder.button(text="Решить задачи", callback_data="tasks")
        builder.button(text="Просмотр статистики", callback_data="statistics")
        await callback_query.message.answer("Что вы хотите сделать?", reply_markup=builder.as_markup())
    elif language=='uz':
        await callback_query.message.answer(f"Siz tilni tanladingiz: {language.capitalize()}")
        builder.button(text="Masalalar ishlash", callback_data="tasks")
        builder.button(text="Statistikani ko'rish", callback_data="statistics")
        await callback_query.message.answer("Siz nima qilmoqchisiz?", reply_markup=builder.as_markup())
    else:
        await callback_query.message.answer(f"You have selected a language: {language.capitalize()}")
        builder.button(text="Solve tasks", callback_data="tasks")
        builder.button(text="View Statistics", callback_data="statistics")
        await callback_query.message.answer("What do you want to do?", reply_markup=builder.as_markup())


@dp.callback_query(lambda c: c.data == 'tasks')
async def solve_tasks(callback_query: CallbackQuery):
    builder = InlineKeyboardBuilder()
    user_id=callback_query.from_user.id
    lang=user_language[user_id]
    if lang=='ru':
        builder.button(text="Лёгкие", callback_data="easy")
        builder.button(text="Средние", callback_data="medium")
        builder.button(text="Сложные", callback_data="hard")

        await callback_query.answer()
        await callback_query.message.answer("Выберите уровень сложности задач", reply_markup=builder.as_markup())
    elif lang=='uz':
        builder.button(text="Oson", callback_data="easy")
        builder.button(text="O'rtacha", callback_data="medium")
        builder.button(text="Qiyin", callback_data="hard")

        await callback_query.answer()
        await callback_query.message.answer("Masalaning qiyinlik darajasini tanlang", reply_markup=builder.as_markup())
    else:
        builder.button(text="Easy", callback_data="easy")
        builder.button(text="Medium", callback_data="medium")
        builder.button(text="Hard", callback_data="hard")

        await callback_query.answer()
        await callback_query.message.answer("Choose the difficulty level of the tasks.", reply_markup=builder.as_markup())



TASKS_PER_PAGE=5

async def show_karousel(callback_query, difficulty, page=1):
    task_list = list(tasks[difficulty].keys())
    print(task_list)
    
    total_pages = (len(task_list) + TASKS_PER_PAGE - 1) // TASKS_PER_PAGE
    
    start = (page - 1) * TASKS_PER_PAGE
    end = min(start + TASKS_PER_PAGE, len(task_list))
    tasks_to_display = task_list[start:end]

    builder = InlineKeyboardBuilder()

    for task in tasks_to_display:
        builder.row(InlineKeyboardButton(text=task, callback_data=f"task_{difficulty}_{task}"))

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"nav_{difficulty}_{page-1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"nav_{difficulty}_{page+1}"))
    
    if navigation_buttons:
        builder.row(*navigation_buttons)
    user_id=callback_query.from_user.id
    lang=user_language[user_id]
    if lang=='ru':
        new_text = f"Выберите задачу (страница {page} из {total_pages})"
    elif lang=='uz':
        new_text = f"Masalani tanlang ({total_pages}-ta betdan {page}-si)"
    else:
        new_text = f"Choose a task (page {page} of {total_pages})"
    await callback_query.message.answer(new_text, reply_markup=builder.as_markup())


@dp.callback_query(lambda c: c.data.startswith('nav_'))
async def handle_carousel_navigation(callback_query):
    data = callback_query.data.split('_')  
    difficulty = data[1]  
    page = int(data[2])  
    await show_karousel(callback_query, difficulty, page)




async def show_carousel(callback_query, difficulty, page=1):
    task_list = list(tasks[difficulty].keys())
    print(task_list)

    total_pages = (len(task_list) + TASKS_PER_PAGE - 1) // TASKS_PER_PAGE
    
    start = (page - 1) * TASKS_PER_PAGE
    end = min(start + TASKS_PER_PAGE, len(task_list))
    tasks_to_display = task_list[start:end]

    builder = InlineKeyboardBuilder()

    for task in tasks_to_display:  
        builder.row(InlineKeyboardButton(text=task, callback_data=f"task_{difficulty}_{task}"))

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"navigate_{difficulty}_{page-1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"navigate_{difficulty}_{page+1}"))
    
    if navigation_buttons:
        builder.row(*navigation_buttons)

    current_text = callback_query.message.text
    user_id=callback_query.from_user.id
    lang=user_language[user_id]
    if lang=='ru':
        new_text = f"Выберите задачу (страница {page} из {total_pages})"
    elif lang=='uz':
        new_text = f"Masalani tanlang ({total_pages}-ta betdan {page}-si)"
    else:
        new_text = f"Choose a task (page {page} of {total_pages})"
    if current_text != new_text:
        await callback_query.message.edit_text(new_text, reply_markup=builder.as_markup())
    else:
        await callback_query.message.edit_reply_markup(reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith('navigate_'))
async def handle_carousel_navigation(callback_query):
    data = callback_query.data.split('_')  
    difficulty = data[1]  
    page = int(data[2])  
    await show_carousel(callback_query, difficulty, page)

@dp.callback_query(lambda c: c.data in ['easy', 'medium', 'hard', 'Лёгкие', 'Средние', 'Сложные'])
async def show_task(callback_query):
    difficulty = callback_query.data
    difficulty_map = {
        'easy': 'Oson',
        'medium': 'O\'rtacha',
        'hard': 'Qiyin',
        'Лёгкие': 'Oson',
        'Средние': 'O\'rtacha',
        'Сложные': 'Qiyin'
    }

    mapped_difficulty = difficulty_map.get(difficulty)

    if mapped_difficulty and mapped_difficulty in tasks:  
        await show_carousel(callback_query, mapped_difficulty, page=1)
    else:
        await callback_query.message.answer("Неверный выбор сложности или задач.")







@dp.callback_query(lambda c: c.data.startswith('task_'))
async def show_task(callback_query: CallbackQuery):
    difficulty, task_name = callback_query.data.split('_')[1], '_'.join(callback_query.data.split('_')[2:])
    task = tasks[difficulty][task_name]
    
    if task[-1] == 'Yes':
        user_id=callback_query.from_user.id
        lang=user_language[user_id]
        if lang=='ru':
            await callback_query.message.answer('Вы уже пробовали решить эту задачу\nПо правилам нашего бота решать заново её нельзя\nПожалуйста выберите другую задачу:')
        elif lang=='uz':
            await callback_query.message.answer("Siz bu masalani allaqachon yechishga harakat qilgansiz\nBizning bot qoidalariga ko'ra uni qayta yechish mumkin emas\nIltimos, boshqa masalani tanlang:")
        else:
            await callback_query.message.answer("You have already attempted to solve this problem\nAccording to our bot's rules, you cannot solve it again\nPlease choose another problem:")
        await show_karousel(callback_query, difficulty, page=1)
    else:
        description = task[0]
        options = task[1:4]
        correct_answer = task[4]
        
        builder = InlineKeyboardBuilder()
        for i, option in enumerate(options, 1):
            builder.button(text=str(i), callback_data=f"answer_{difficulty}_{task_name}_{i}")
        
        await callback_query.message.answer(f'{description}\n\nTarjima uchun/ Для перевода/ For translate:  https://translate.google.com/?sl=ru&tl=uz&op=translate')
        await callback_query.message.answer(f'1.{options[0]}\n2.{options[1]}\n3.{options[2]}', reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith('answer_'))
async def check_answer(callback_query: CallbackQuery):
    difficulty, task_name, answer = callback_query.data.split('_')[1], '_'.join(callback_query.data.split('_')[2:-1]), int(callback_query.data.split('_')[-1])
    task = tasks[difficulty][task_name]
    correct_answer = task[4]
    
    if answer == correct_answer:
        score = {'Oson': 1, 'O\'rtacha': 2, 'Qiyin': 3}[difficulty]
        user_id = callback_query.from_user.id
        cursor.execute("UPDATE users SET score = score + ? WHERE id = ?", (score, user_id))
        conn.commit()

        user_id=callback_query.from_user.id
        lang=user_language[user_id]
        if lang=='ru':
            await callback_query.message.answer(f"Вы правильно решили задачу! Вы получили {score} балла!")
        elif lang=='uz':
            await callback_query.message.answer(f"Siz masalani to‘g‘ri yechdingiz! Siz {score} ball oldingiz!")
        else:
            await callback_query.message.answer(f"You solved the problem correctly! You earned {score} points!")
    else:
        user_id=callback_query.from_user.id
        lang=user_language[user_id]
        if lang=='ru':
            await callback_query.message.answer("К сожалению вы ошиблись")
        elif lang=='ru':
            await callback_query.message.answer("Afsuski, siz xatoga yo'l qo'ydingiz")
        else:
            await callback_query.message.answer("Unfortunately, you made a mistake.")
    tasks[difficulty][task_name][-1]='Yes'
    builder = InlineKeyboardBuilder()
    if lang=='ru':
        builder.button(text="Решить задачи", callback_data="tasks")
        builder.button(text="Просмотр статистики", callback_data="statistics")

        await callback_query.message.answer("Что вы хотите сделать ещё?", reply_markup=builder.as_markup())
    elif lang=='uz':
        builder.button(text="Masalalar ishlash", callback_data="tasks")
        builder.button(text="Statistikani ko'rish", callback_data="statistics")
        await callback_query.message.answer("Siz nima qilmoqchisiz?", reply_markup=builder.as_markup())
    else:
        builder.button(text="Solve tasks", callback_data="tasks")
        builder.button(text="View Statistics", callback_data="statistics")
        await callback_query.message.answer("What do you want to do?", reply_markup=builder.as_markup())


@dp.callback_query(lambda c: c.data == 'statistics')
async def show_statistics(callback_query: CallbackQuery):
    cursor.execute("SELECT name, score FROM users ORDER BY score DESC LIMIT 10")
    top_users = cursor.fetchall()
    user_id=callback_query.from_user.id
    lang=user_language[user_id]
    if lang=='ru':
        result = "Топ 10 пользователей:\n"
        for rank, (name, score) in enumerate(top_users, 1):
            result += f"{rank}. {name} - {score} баллов\n"
        
        user_id = callback_query.from_user.id
        cursor.execute("SELECT name, score FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        result += f"\nВы: {user[0]} - {user[1]} баллов"
    elif lang=='uz':
        result = "Top 10 foydalanuvchilar:\n"
        for rank, (name, score) in enumerate(top_users, 1):
            result += f"{rank}. {name} - {score} ball\n"
        
        user_id = callback_query.from_user.id
        cursor.execute("SELECT name, score FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        result += f"\nSiz: {user[0]} - {user[1]} ball"
    else:
        result = "Top 10 users:\n"
        for rank, (name, score) in enumerate(top_users, 1):
            result += f"{rank}. {name} - {score} баллов\n"
        
        user_id = callback_query.from_user.id
        cursor.execute("SELECT name, score FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        result += f"\nYou: {user[0]} - {user[1]} points"
    
    await callback_query.answer()
    await callback_query.message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
