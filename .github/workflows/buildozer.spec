[app]
# Имя приложения
title = Vismon

# Имя пакета (обязательно уникальное для публикации)
package.name = vismon

# Домен пакета
package.domain = com.example

# Основной файл приложения
source.main = vismon.py

# Поддерживаемые расширения файлов
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 1.0

# Минимальная поддерживаемая версия iOS
ios.min_version = 12.0

# Описание приложения
description = Приложение для контроля медицинских представителей.

# Автор
author = Ваше Имя

# Контактный email
author.email = example@example.com

# Лицензия приложения
license = MIT

# Значок приложения
icon.filename = %(source.dir)s/data/icon.png

# Экран загрузки
presplash.filename = %(source.dir)s/data/presplash.png

# Разрешения (если требуются дополнительные)
# Например: интернет, доступ к камере и т.д.
permissions = 

[buildozer]
# Платформы для сборки
target = ios

# Локализация
log_level = 2

# Файлы исключения из сборки
ignore_files = .git/*,*.zip,*.tar.gz,*.rar

# Зависимости, которые нужно включить
requirements = python3,kivy

[ios]
# URL-репозиторий Kivy-iOS
kivy_ios_url = https://github.com/kivy/kivy-ios

# Ветка Kivy-iOS
kivy_ios_branch = master

# Идентификатор разработчика (должен быть добавлен вручную)
ios.codesign.allowed = True
ios.codesign.identity = "iPhone Developer: your_email@example.com (TEAM_ID)"

# Формат сборки
ios.archs = arm64,x86_64

# Папка, где будет находиться .ipa
ios.build_folder = %(source.dir)s/bin/ios

# Имя выходного файла
ios.package_name = vismon

# Укажите дополнительные библиотеки, если требуются
# ios.frameworks = UIKit, Foundation

