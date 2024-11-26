[app]
# Название приложения
title = Vismon
# Пакетное имя приложения (используйте уникальное имя)
package.name = vismon
package.domain = org
# Версия приложения
version = 1.0.0
# Описание
description = Medical Representative Control App
# Путь к исходным кодам приложения
source.dir = .  # Указывает на текущую директорию, где находятся ваши файлы
# Директории и расширения файлов для включения
source.include_exts = py,png,jpg,kv,atlas
# Зависимости
dependencies = python3,kivy

# Настройки для сборки iOS
ios.kivy_ios = true
ios.apple_sdk_version = 15.0  # Убедитесь, что версия SDK совместима с вашим проектом
ios.min_ios_version = 12.0

# Иконка приложения
package.icon = icon.png  # Укажите путь к изображению иконки вашего приложения (если оно есть)

# Установка Xcode версии для сборки
xcode = 15  # Версия Xcode для вашего проекта

# Другие настройки могут быть добавлены, если нужно
