name: Build iOS App with Buildozer

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-ios:
    runs-on: macos-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install buildozer cython

    - name: Install Xcode Command Line Tools (if not already installed)
      run: |
        if ! xcode-select -p; then
          sudo xcode-select --install
          sudo xcodebuild -license accept
        else
          echo "Xcode Command Line Tools already installed"
        fi

    - name: Create or Update Buildozer Spec File
      run: |
        if [ ! -f buildozer.spec ]; then
          buildozer init  # Создание buildozer.spec, если его нет
        fi
        # Устанавливаем правильный путь к исходным файлам
        echo 'source.dir = vismon' >> buildozer.spec

    - name: Prepare Buildozer for iOS
      run: |
        buildozer -v ios debug

    - name: Archive the IPA
      uses: actions/upload-artifact@v3
      with:
        name: vismon-ios-app
        path: bin/ios/*debug.ipa
