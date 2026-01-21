# 🎮 Где разместить игру для скачивания (без Google Drive)

## Проблема с Google Drive
- Для больших файлов показывает страницу подтверждения
- Ограничение скорости скачивания
- Может блокировать при большом количестве загрузок

## ✅ Рекомендуемые варианты

### 1. GitHub Releases (бесплатно, до 2 ГБ)

**Плюсы:**
- ✅ Прямые ссылки без редиректов
- ✅ Быстрая скорость
- ✅ Надёжность
- ✅ Бесплатно

**Как использовать:**

1. Создайте репозиторий на GitHub
2. Перейдите в Releases → "Create a new release"
3. Загрузите ваш ZIP файл как Asset
4. Опубликуйте релиз
5. Получите прямую ссылку на ZIP:

```
https://github.com/username/repo/releases/download/v1.0/game.zip
```

**Пример для versions.json:**
```json
{
  "name": "Twix Game v1.0",
  "download_url": "https://github.com/yourusername/TwixGame/releases/download/v1.0/game.zip"
}
```

---

### 2. Mega.nz (бесплатно, до 50 ГБ)

**Плюсы:**
- ✅ Большой лимит хранения
- ✅ Хорошая скорость
- ✅ Нет страниц подтверждения

**Как использовать:**

1. Зарегистрируйтесь на [mega.nz](https://mega.nz)
2. Загрузите файл
3. Нажмите ПКМ → "Get link"
4. Выберите "Link" (не "Decryption key")
5. Используйте библиотеку `mega.py` или конвертер ссылок

**Для простого использования через API:**
```python
# Установите: pip install mega.py
from mega import Mega

mega = Mega()
m = mega.login(email, password)
file = m.upload('game.zip')
link = m.get_upload_link(file)
```

---

### 3. Собственный HTTP сервер (лучший вариант)

**Плюсы:**
- ✅ Полный контроль
- ✅ Нет ограничений
- ✅ Самая быстрая скорость
- ✅ Прямые ссылки

**Варианты размещения:**

#### A) VPS/Dedicated Server
- DigitalOcean (от $5/мес)
- Hetzner (от €3/мес)
- Contabo (от €4/мес)

#### B) Бесплатные хостинги для статических файлов
- Netlify (100 ГБ трафика/мес)
- Vercel (100 ГБ/мес)
- Cloudflare Pages (безлимит!)

**Пример с Nginx на VPS:**

```bash
# 1. Установите Nginx
apt install nginx

# 2. Создайте папку для игр
mkdir -p /var/www/games

# 3. Загрузите game.zip в /var/www/games/

# 4. Настройте Nginx (/etc/nginx/sites-available/games)
server {
    listen 80;
    server_name yourdomain.com;

    location /games/ {
        root /var/www;
        autoindex off;
    }
}

# 5. Перезапустите Nginx
systemctl restart nginx
```

**Прямая ссылка:**
```
http://yourdomain.com/games/game.zip
```

---

### 4. MediaFire (бесплатно, до 10 ГБ)

**Плюсы:**
- ✅ Простой интерфейс
- ✅ Прямые ссылки
- ✅ Без ограничения скачиваний

**Как использовать:**

1. Зарегистрируйтесь на [mediafire.com](https://www.mediafire.com)
2. Загрузите файл
3. Получите ссылку для скачивания
4. Извлеките прямую ссылку из HTML

**Пример прямой ссылки:**
```
http://download1234.mediafire.com/xxxxx/game.zip
```

---

### 5. Dropbox (бесплатно, 2 ГБ)

**Плюсы:**
- ✅ Надёжность
- ✅ Простая конвертация ссылок

**Как использовать:**

1. Загрузите файл в Dropbox
2. Получите ссылку для общего доступа:
   ```
   https://www.dropbox.com/s/xxxxx/game.zip?dl=0
   ```
3. Конвертируйте в прямую ссылку:
   ```
   https://dl.dropboxusercontent.com/s/xxxxx/game.zip
   ```

**Правило конвертации:**
- Замените `www.dropbox.com` → `dl.dropboxusercontent.com`
- Уберите `?dl=0` в конце

---

### 6. Discord CDN (хак, не рекомендуется)

**Плюсы:**
- ✅ Очень быстро
- ✅ Прямые ссылки
- ✅ Бесплатно

**Минусы:**
- ❌ Лимит 25 МБ (или 500 МБ с Nitro)
- ❌ Нарушение TOS
- ❌ Может быть удалено

**Как использовать:**
1. Создайте приватный сервер Discord
2. Загрузите файл в чат
3. Скопируйте ссылку на файл
4. Используйте эту ссылку

---

## 🚀 Рекомендация для вашего проекта

### Лучший выбор: GitHub Releases + Cloudflare

1. **Разместите на GitHub Releases** - для основного хостинга
2. **Используйте Cloudflare Pages** - как зеркало/CDN
3. **Резервная копия на Mega.nz** - на случай проблем

### Пример конфигурации с резервными ссылками:

```json
{
  "versions": [
    {
      "name": "Twix Game v1.0",
      "description": "Основная версия игры",
      "download_url": "https://github.com/yourusername/TwixGame/releases/download/v1.0/game.zip",
      "mirrors": [
        "https://yourdomain.pages.dev/game.zip",
        "https://mega.nz/file/xxxxx#yyyyy"
      ],
      "installed": false
    }
  ]
}
```

---

## 📦 Простой Python HTTP сервер (для тестирования)

Если хотите быстро протестировать скачивание локально:

```bash
# 1. Поместите game.zip в папку
cd /path/to/folder

# 2. Запустите сервер
python -m http.server 8000

# 3. Используйте в versions.json:
"download_url": "http://localhost:8000/game.zip"
```

**Для доступа из интернета используйте ngrok:**
```bash
# 1. Скачайте ngrok с ngrok.com
# 2. Запустите
ngrok http 8000

# 3. Получите публичный URL
https://xxxx-xx-xxx-xxx-xx.ngrok-free.app/game.zip
```

---

## 🔒 Безопасность

**Для любого метода:**
- ✅ Используйте HTTPS (где возможно)
- ✅ Проверяйте целостность файла (SHA256)
- ✅ Не размещайте исходный код вместе с игрой
- ✅ Используйте обфускацию JAR если нужно

**Пример проверки целостности:**
```json
{
  "name": "Twix Game v1.0",
  "download_url": "https://...",
  "sha256": "abc123def456...",
  "size_mb": 150
}
```

---

## 💰 Стоимость

| Сервис | Лимит | Цена | Скорость |
|--------|-------|------|----------|
| GitHub Releases | 2 ГБ/файл | Бесплатно | ⭐⭐⭐⭐⭐ |
| Mega.nz | 50 ГБ | Бесплатно | ⭐⭐⭐⭐ |
| Cloudflare Pages | Безлимит | Бесплатно | ⭐⭐⭐⭐⭐ |
| DigitalOcean | Безлимит | $5/мес | ⭐⭐⭐⭐⭐ |
| MediaFire | 10 ГБ | Бесплатно | ⭐⭐⭐ |
| Dropbox | 2 ГБ | Бесплатно | ⭐⭐⭐⭐ |

---

## ❓ Что выбрать для вашей игры?

**Если игра < 100 МБ:**
→ GitHub Releases (самый простой вариант)

**Если игра 100 МБ - 2 ГБ:**
→ GitHub Releases + Mega.nz (основа + зеркало)

**Если игра > 2 ГБ:**
→ Mega.nz или собственный сервер

**Если у вас VPS:**
→ Nginx + прямой HTTP (лучшая производительность)

---

## 📞 Нужна помощь?

Если нужна помощь с настройкой хостинга:
- Telegram: t.me/TwixClient
- GitHub Issues: создайте issue в репозитории

---

**Следующий шаг:** Выберите подходящий хостинг и обновите `versions.json` с прямой ссылкой на вашу игру!
