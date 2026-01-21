# 🚀 КАК ПОЛУЧИТЬ ГОТОВЫЙ .EXE ФАЙЛ

## ⚡ САМЫЙ БЫСТРЫЙ СПОСОБ (3 шага, 5 минут)

### Шаг 1: Перейдите в GitHub Releases

Откройте эту ссылку в браузере:
```
https://github.com/lysenkofelix-del/Twiz/releases
```

### Шаг 2: Создайте новый Release

1. Нажмите кнопку **"Create a new release"**

2. Заполните форму:
   ```
   Tag version: v1.0.0
   Release title: TwixClient Launcher v1.0.0
   Description: Первый релиз лаунчера TwixClient
   ```

3. **НЕ загружайте никакие файлы!**

4. Нажмите **"Publish release"**

### Шаг 3: Дождитесь автосборки

1. Перейдите во вкладку **"Actions"**:
   ```
   https://github.com/lysenkofelix-del/Twiz/actions
   ```

2. Вы увидите процесс **"Build Twix Launcher"**

3. Подождите **3-5 минут** (зелёная галочка = готово!)

4. Вернитесь в **"Releases"**:
   ```
   https://github.com/lysenkofelix-del/Twiz/releases
   ```

5. В релизе `v1.0.0` появится файл:
   ```
   TwixLauncher-v1.0.0.zip
   ```

6. **СКАЧАЙТЕ ЕГО!** ✅

---

## 📦 Что внутри архива:

```
TwixLauncher-v1.0.0.zip
├── TwixLauncher.exe              ← ГОТОВЫЙ ЛАУНЧЕР!
├── ИНСТРУКЦИЯ_ПОЛЬЗОВАТЕЛЯ.txt   ← Для игроков
└── versions.json.example         ← Пример конфига
```

---

## 🎯 ЧТО ДАЛЬШЕ?

### 1. Протестируйте лаунчер:

- Запустите `TwixLauncher.exe`
- Нажмите "УСТАНОВИТЬ"
- Проверьте что игра скачивается
- Нажмите "ЗАПУСТИТЬ"
- Убедитесь что игра запускается

### 2. Поделитесь с игроками:

**Дайте им ссылку:**
```
https://github.com/lysenkofelix-del/Twiz/releases/latest
```

**Telegram пост:**
```
🎮 НОВЫЙ TWIX CLIENT LAUNCHER!

Скачать: https://github.com/lysenkofelix-del/Twiz/releases/latest

✨ Возможности:
• Автоматическая установка
• Настройка RAM
• Красивый интерфейс

💬 Поддержка: https://t.me/TwixClient
```

---

## ❓ Что делать если...

### GitHub Actions не запустился?

1. Проверьте что тег начинается с `v` (v1.0.0, v1.0.1...)
2. Зайдите в Settings → Actions → разрешите Actions
3. Попробуйте создать Release заново

### Сборка упала с ошибкой?

1. Кликните на failed workflow в Actions
2. Посмотрите логи
3. Скорее всего проблема с зависимостями
4. Попробуйте создать новый тег: `v1.0.1`

### Нужно срочно, не хочу ждать?

Соберите на Windows компьютере:
```bash
pip install -r requirements.txt
python build_exe.py
```

Готовый файл: `dist/TwixLauncher.exe`

---

## ✅ ГОТОВО!

После этих 3 шагов у вас будет готовый `TwixLauncher.exe`!

**Ссылка для начала:**
https://github.com/lysenkofelix-del/Twiz/releases/new

---

**Удачи! 🎉**
