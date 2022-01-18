# E-commerce-web-application

This project deals with developing an E-commerce web application. It provides the user with a list of the various products available for purchase in the store. For the convenience of online shopping, a shopping cart is provided to the user. After the selection of the goods, it is sent for the order confirmation process. 

The system is implemented using Python’s web framework Django.

this project is made with ❤️, in collab with [El hachemy Said](https://www.linkedin.com/in/said-el-hachemy).

🛒Customer Interface:

- Customer search for a product
- Customer changes quantity
- The customer adds an item to the cart
- Customer views cart
- Customer checks out
- Customer sends order
- Customer adds a product review

⚙️Admin Interface:

- Admin logs in
- Admin sees inventory and selling statistics
- Admin inserts item
- Admin removes item
- Admin modifies item

# Screenshots

### Home page

![alt text](https://github.com/DiouaneAbdallah/Django-e-commerce-web-application/blob/main/ScreenShots/Screenshot2.png?raw=true)

### Products serarch page

![alt text](https://github.com/DiouaneAbdallah/Django-e-commerce-web-application/blob/main/ScreenShots/Screenshot3..png?raw=true)

### Product page

![alt text](https://github.com/DiouaneAbdallah/Django-e-commerce-web-application/blob/main/ScreenShots/Screenshot4.png?raw=true)

### Cart page

![alt text](https://github.com/DiouaneAbdallah/Django-e-commerce-web-application/blob/main/ScreenShots/Screenshot5.png?raw=true)

### Admin dashboard

![alt text](https://github.com/DiouaneAbdallah/Django-e-commerce-web-application/blob/main/ScreenShots/Screenshot1.png?raw=true)

# Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with
```
pip install virtualenv
```
Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project
```
virtualenv env
```
That will create a new folder env in your project directory. Next activate it with this command on mac/linux:
```
source env/bin/active
```
Then install the project dependencies with
```
pip install -r requirements.txt
```
Now you can run the project with this command
```
python manage.py runserver
```
