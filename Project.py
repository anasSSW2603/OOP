from fasthtml.common import *

app, rt = fast_app()

class System:
    def __init__(self):
        self.__acc_lst = []
        self.__product_lst = []

    def search_acc_by_id(self, user_id):
        for acc in self.__acc_lst:
            if acc.get_acc_id() == user_id:
                return acc
        return None

    def search_acc_by_email(self, email):
        for acc in self.__acc_lst:
            if acc.get_acc_email() == email:
                return acc
        return None
    
    def search_product_by_name(self, name):
        for product in self.__product_lst:
            if product.get_name_product() == name:
                return product
        return None

    def get_acc_lst(self):
        return self.__acc_lst
    
    def get_product_lst(self):
        return self.__product_lst

    def add_cart(self, product_name, quantity, acc_id):
        product = self.search_product_by_name(product_name)
        acc = self.search_acc_by_id(acc_id)

        if not product:
            return f"Product '{product_name}' not found."
        if not acc:
            return f"Account ID '{acc_id}' not found."

        item = Cartitem(product, quantity)
        acc.add_cart_shopping(item)
        return f"Added {quantity} x {product_name} to {acc.get_name()}'s cart."
    
    def add_account(self, account):
        self.__acc_lst.append(account)

    def view_cart(self, acc_id):
        acc = self.search_acc_by_id(acc_id)
        if acc:
            return acc.view_cart()
        return "Account not found."
    
    def check_login(self, email, password):
        acc = self.search_acc_by_email(email)
        if acc and acc.get_password() == password:
            return acc  # ถ้าตรงกัน ส่งบัญชีกลับไป
        return None  # ไม่ตรงกัน

class Account:
    def __init__(self, user_id, name, email, age, password):
        self.__id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__age = age
        self.__myCart_shopping = Cart()

    def get_acc_id(self):
        return self.__id
    
    def get_acc_email(self):
        return self.__email
    
    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name
    
    def add_cart_shopping(self, cart_item):
        self.__myCart_shopping.add_cart_item(cart_item)

    def get_cart_shopping(self): 
        return self.__myCart_shopping
    
    def view_cart(self): 
        cart_items = self.__myCart_shopping.get_cart_items()
        if not cart_items:
            return f"Cart of {self.__name} is empty."
        
        result = f"Cart of {self.__name}:\n"
        for item in cart_items:
            result += f"- {item.get_product().get_name_product()} : {item.get_quantity()}\n"
        return result

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, Email: {self.__email}, Age: {self.__age}, pass {self.__password}"
    
class Product:
    def __init__(self, product_id, name):
        self.__product_id = product_id
        self.__name = name
    
    def get_name_product(self):
        return self.__name

class Cart:
    def __init__(self):
        self.__cart_item_lst = []

    def add_cart_item(self, cart_item):
        self.__cart_item_lst.append(cart_item)
        
    def get_cart_items(self):  
        return self.__cart_item_lst

    def __str__(self):
        return f'{[[i.get_product().get_name_product(), i.get_quantity()] for i in self.__cart_item_lst]}'

class Cartitem:
    def __init__(self, product, quantity):
        self.__product = product
        self.__quantity = quantity

    def get_product(self):
        return self.__product
    
    def get_quantity(self):
        return self.__quantity

    def __str__(self):
        return f'{self.__product.get_name_product()} : {self.__quantity}'

system = System()  

@rt("/")
def get():
    return Container(
        H1("Banana", style="text-align: center; color: black; margin: 20px 0;"),
        Div(
            A("Cart", href="/Cart", _class="nav-link"),
            A("Login", href="/login", _class="nav-link"),
            A("Register", href="/register", _class="nav-link")
        ),
        Style(
            """
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .nav-link {
                margin: 10px;
                text-decoration: none;
                color: white;
                background: #007bff;
                padding: 10px;
                border-radius: 5px;
            }
            .nav-link:hover {
                background: #0056b3;
            }
            """
        )
    )

@rt("/Cart")
def get():
    return Div(
        H1('ตะกร้าสินค้า (3)', _class='cart-header'),
        Div(
            Div(
                Img(src='1.jpg', alt='คีย์บอร์ด', _class='cart-item-img'),
                Div('Mouse', _class='cart-item-info'),
                Span('฿990', _class='cart-item-price'),
                Div(
                    Button('-', _class='qty-btn'),
                    Input(type='text', value='2', _class='qty-input'),
                    Button('+', _class='qty-btn'),
                    _class='cart-item-controls'
                ),
                Button('🗑️', _class='delete-btn'),
                _class='cart-item'
            ),
            Div(
                Img(src='1.jpg', alt='เคส iPad', _class='cart-item-img'),
                Div('เคส JTLEGEND iPad Air 11" M2 (2024) Youth Dark Blue', _class='cart-item-info'),
                Span('฿990', _class='cart-item-price'),
                Div(
                    Button('-', _class='qty-btn'),
                    Input(type='text', value='1', _class='qty-input'),
                    Button('+', _class='qty-btn'),
                    _class='cart-item-controls'
                ),
                Button('🗑️', _class='delete-btn'),
                _class='cart-item'
            ),
            _class='cart-items'
        ),
        Div(
            Div('ยอดรวม: ฿2,970'),
            Div('ส่วนลด: - ฿0'),
            Hr(),
            Div(B('ยอดรวมสุทธิ: ฿2,970')),
            Button('ดำเนินการสั่งซื้อ', _class='checkout-btn'),
            _class='cart-summary'
        ),
        Style(
            """
            body {
                background-color: rgb(245, 245, 245);
                height: 100vh;
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
            }

            .cart-header {
                color: #333;
                font-size: 32px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
                padding-top: 20px;
            }

            .cart-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                background: #fff;
                border-radius: 8px;
                transition: transform 0.3s ease;
            }

            .cart-item:hover {
                transform: translateX(10px);
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }

            .cart-item-img {
                width: 70px;
                height: 70px;
                margin-right: 15px;
                border-radius: 8px;
            }

            .cart-item-info {
                flex: 1;
                color: #333;
                font-weight: 500;
                font-size: 18px;
            }

            .cart-item-price {
                color: #e74c3c;
                font-weight: 600;
                font-size: 20px;
                margin-right: 20px;
            }

            .cart-item-controls {
                display: flex;
                align-items: center;
            }

            .qty-input {
                background-color: gray;
                width: 40px;
                height: 30px;
                text-align: center;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 0 10px;
            }

            .qty-btn {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            .qty-btn:hover {
                background-color: #e67e22;
            }

            .delete-btn {
                background: none;
                border: none;
                cursor: pointer;
                font-size: 18px;
                color: #e74c3c;
                font-weight: bold;
                transition: color 0.3s ease;
            }

            .delete-btn:hover {
                color: #c0392b;
            }

            .cart-items {
                padding: 0 20px;
            }

            .cart-summary {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                font-size: 18px;
                color: #333;
            }

            .checkout-btn {
                background-color: #27ae60;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            .checkout-btn:hover {
                background-color: #2ecc71;
            }
            """
        ),
        Script(
            """
            document.getElementById('increase-1').onclick = function() {
                var qtyInput = document.getElementById('qty-1');
                qtyInput.value = parseInt(qtyInput.value) + 1;
            };
            
            document.getElementById('decrease-1').onclick = function() {
                var qtyInput = document.getElementById('qty-1');
                if (parseInt(qtyInput.value) > 1) {
                    qtyInput.value = parseInt(qtyInput.value) - 1;
                }
            };

            document.getElementById('increase-2').onclick = function() {
                var qtyInput = document.getElementById('qty-2');
                qtyInput.value = parseInt(qtyInput.value) + 1;
            };
            
            document.getElementById('decrease-2').onclick = function() {
                var qtyInput = document.getElementById('qty-2');
                if (parseInt(qtyInput.value) > 1) {
                    qtyInput.value = parseInt(qtyInput.value) - 1;
                }
            };
            """
        )
    )
    

    
@rt("/login")
def get():
    return Div(
        H2('Login', _class='login-title'),
        Div(
            Form(
                Input(type='email', name='email', placeholder='อีเมล', required=True),
                Input(type='password', name='password', placeholder='รหัสผ่าน', required=True),
                Button('Login', type='submit', _class='signup-btn'),
                action='/loginCheck', method='post', 
                _class='login-form'
            ),
            _class='signup-container'
        ),
        Style(
            """
            body {
                background-color:rgb(255, 255, 255);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .login-title {
                color: rgb(0, 0, 0);
                text-align: center;
                font-size: 50px;
                margin: 20px 0;
            }
            .signup-container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgb(187, 187, 187);
                width: 300px;
                text-align: center;
            }
            .signup-btn {
                width: 100%;
                padding: 8px;
                background-color:rgb(255, 170, 0);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .signup-btn:hover {
                background-color:rgb(255, 132, 0);
            }
            .login-form input {
                color: rgb(0, 0, 0);
                background-color:rgb(239, 239, 239);
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            """
        )
    )

@rt("/loginCheck")
def post(email: str, password: str):
    acc = system.check_login(email, password)
    if acc:
        print(f"✅ Login Success: {acc}")
        return Redirect("/")  # กลับไปหน้าแรกถ้า Login สำเร็จ
    return "❌ Login Failed! กรุณาตรวจสอบอีเมลหรือรหัสผ่าน", 401  # แจ้งเตือนถ้าข้อมูลผิด

@rt("/register")
def get():
    return Div(
        H2('Register', _class='register-title'),
        Div(
            Form(
                Input(Id='Fullname', type='text', name='Fullname', placeholder='Fullname', required=True),
                Input(Id='email', type='email', name='email', placeholder='E-mail', required=True),
                Input(Id='password', type='password', name='password', placeholder='password', required=True),
                Input(Id='age', type='number', name='age', min='18', max='100',placeholder='Age'),
                Button('Register', type='submit', _class='register-btn'),
                action='/add', method='post',
                _class='register-form'
            ),
            _class='register-container'
        ),
        Style(
            """
            body {
                background-color:rgb(255, 255, 255);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .register-title {
                color: rgb(0, 0, 0);
                text-align: center;
                font-size: 50px;
                margin: 20px 0;
            }
            .register-container {
               background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgb(187, 187, 187);
                width: 300px;
                text-align: center;
            }
            .register-btn {
                width: 100%;
                padding: 8px;
                background-color:rgb(255, 170, 0);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .register-btn:hover {
                background-color:rgb(255, 132, 0);
            }
            .register-form input, .register-form select {
                color: rgb(0, 0, 0);
                background-color:rgb(239, 239, 239);
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            """
        )
    )
    
@rt("/add")
def post(Fullname: str, email: str, password: str, age: str):
    user_id = len(system.get_acc_lst()) + 1 
    account = Account(user_id, Fullname, email, age, password)
    system.add_account(account)
    
    print(f"✅ Register Success: {account}") 
    
    return Redirect("/login")
    



    

serve()

