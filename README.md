Сайт с подобием NFT + админка. (Python и Flask).
Перед первым запуском необходимо установить необходимые пакеты:

pip install -r requirements.txt

Программа запускается скриптом main.py

После запуска реклама выводит ссылку на страницу: http://127.0.0.1:5000 после перехода на неё, открывается главная
страница сайта:
<div align="center">
<img src="mdimages/image1.png">
</div>
<div align="center">
<img src="mdimages/image2.png">
</div>
Для вывода предметов и авторизации пользователей используется база данных состоящая из трёх таблиц:

1. Image - Таблица со всеми загруженными предметами:

* Номер (id);
* Название (name);
* Цена(price);
* Путь к файлу(path)

2. User - Таблица с пользователями сайта:
* Номер (id);
* Имя (name);
* Почта (email);
* Пароль (hashed_password)
3. Zip - Таблица с загруженными архивами
* Номер (id);
* Имя файла (name);
* Путь к архиву (path)

Для авторизации необходимо нажать кнопки "Авторизация" и затем "Войти"
<div align="center">
<img src="mdimages/image3.png">
</div>

Откроется форма авторизации:
<div align="center">
<img src="mdimages/image4.png">
</div>
Для ознакомления можно ввести:
<div align="center">
Логин: email2@mail.ru<br>
Пароль: 123456
</div>

После входа, кнопки навбара поменяются:
<div align="center">
<img src="mdimages/image5.png">
</div>

После того как пользователь зашел, у каждой карточки появится кнопка "Скачать":
<div align="center">
<img src="mdimages/image6.png">
</div>

Если пользователь впервые на сайте, он может зарегистрироваться:
<div align="center">
<img src="mdimages/image7.png">
</div>
После регистрации, данные пользователя попадут в базу данных и он в любой момент сможет зайти под своими данными.

После входа, появляется возможность загрузить файл на сайт, после чего он отобразится на странице.
Это можно сделать с помощью кнопки "Загрузить", после чего откроется форма:
<div align="center">
<img src="mdimages/image15.png">
</div>
Так же, имеется возможность загрузить zip файл с помощью кнопки "Загрузить zip файл":
<div align="center">
<img src="mdimages/image16.png">
</div>

<div align="center">
<h3> Панель администратора</h3>
</div>
Переход на страницу осуществляется с помощью ввода ссылки: http://127.0.0.1:5000/admin
<div align="center">
<img src="mdimages/image14.png">
</div>
<div align="center">
<img src="mdimages/image8.png">
</div>
Тестовые данные для входа:
<div align="center">
Логин: admin<br>
Пароль: 12345
</div>

После входа, откроется главная страница:
<div align="center">
<img src="mdimages/image9.png">
</div>
С помощью панели админа можно редактировать предметы на сайте и пользователей
Страница редактирования предметов:
<div align="center">
<img src="mdimages/image10.png">
</div>

Форма редактирования предмета:
<div align="center">
<img src="mdimages/image11.png">
</div>

Страница редактирования пользователей:
<div align="center">
<img src="mdimages/image12.png">
</div>
Форма редактирования пользователя:
<div align="center">
<img src="mdimages/image13.png">
</div>
