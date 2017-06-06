# Integration tests for AtomicBoard

Цель данного проекта охватить тестами основные сценарии использования сервиса 
**AtomicBoard**. 
Stage сервер доступен по адресу: 
[atomicboard.devman.org](http://atomicboard.devman.org).
Перед каждым запуском тестов создается новый пользователь на 
[специальной странице](http://atomicboard.devman.org/create_test_user/).

Реализованы следующие тесты:
* Загрузка с сервера и отображение списка актуальных задач
* Перетаскивание задачи из одного столбца в другой
* Редактирование существующей задачи
* Пометка задачи как решенной
* Создание новой задачи

# Перед использованием
Для корректоной работы необходимо установить **Selenium**:
```
pip install -r requirements.txt
```
Все тесты проводятся на платформе **PhantomJS**, которая позволяет работать с 
WebKit из консоли используя JavaScript и без браузера.
Для установки **PhantomJS** необходимо скачать исполняемый файл со страницы 
загрузки [http://phantomjs.org/download.html](http://phantomjs.org/download.html) 
и настроить ОС.

Для правильной работы **PhantomJS** необходимо обновить системные пакеты до 
последних версий и установить следующие пакеты:
```
sudo apt-get update
sudo apt-get install build-essential chrpath libssl-dev libxft-dev
sudo apt-get install libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev
```

Затем загрузить по указанной выше ссылке архив и распаковать его в удобное 
место:
```
$ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2
$ tar xvjf phantomjs-2.1.1-linux-i686.tar.bz2 -C /usr/local/share/
```

Остается создать символическую ссылку на исполняемый файл:
```
$ sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-i686/bin/phantomjs /usr/local/bin
```

Чтобы убедиться, что все сделано верно можно проверить версию **PhantomJS**:
```
$ phantomjs --version

2.1.1
```

# Запуск тестов

Для запуска тестов воспользуйтесь командой:

```
python3 tests.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
