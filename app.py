from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import os
from models import db, Product, Category

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'

# Initialisation de la DB
db.init_app(app)

def init_db():
    """Peuplement initial de la base de données"""
    categories = [
        Category(name="Dresses"),
        Category(name="T-shirts"),
        Category(name="Jeans"),
        Category(name="Shoes"),
        Category(name="Accessories")
    ]
    db.session.add_all(categories)
    db.session.commit()
    products = [
        # Dresses
        Product(name="Pink Floral Dress", description="Long pink floral silk dress, perfect for evenings.", price=79.99, category_id=1, featured=True, image="dr/dress1.jpg"),
        Product(name="Red Dress", description="Short red dress with floral patterns.", price=59.99, category_id=1, featured=False, image="dr/dress2.jpg"),
        Product(name="Cute Pink Dress", description="Light and comfortable pink summer dress.", price=49.99, category_id=1, featured=False, image="dr/dress3.jpg"),
        Product(name="Blue Floral Dress", description="Elegant blue floral cocktail dress.", price=89.99, category_id=1, featured=False, image="dr/dress4.jpg"),
        Product(name="Vintage Dress", description="White vintage lace dress.", price=69.99, category_id=1, featured=False, image="dr/dress5.jpg"),
        Product(name="Classic Pink Dress", description="Classic pink wrap dress.", price=74.99, category_id=1, featured=False, image="dr/dress6.jpg"),
        Product(name="White Korean Dress", description="Trendy white Korean-style dress.", price=64.99, category_id=1, featured=False, image="dr/dress7.jpg"),
        Product(name="Green Dress", description="Navy blue strapless dress.", price=84.99, category_id=1, featured=False, image="dr/dress8.jpg"),
        Product(name="Black Dress", description="Elegant black pleated dress.", price=54.99, category_id=1, featured=False, image="dr/dress9.jpg"),
        Product(name="White Berries Dress", description="Beige long-sleeved dress with berry print.", price=99.99, category_id=1, featured=False, image="dr/dress10.jpg"),
        # T-shirts
        Product(name="Basic T-shirt 1", description="Classic fit white cotton t-shirt.", price=19.99, category_id=2, featured=True, image="t-shirt/t-shirt1.jpg"),
        Product(name="Basic T-shirt 2", description="Black crew neck t-shirt.", price=21.99, category_id=2, featured=False, image="t-shirt/t-shirt2.jpg"),
        Product(name="Graphic T-shirt 1", description="T-shirt with original print.", price=24.99, category_id=2, featured=False, image="t-shirt/t-shirt3.jpg"),
        Product(name="Sport T-shirt 1", description="Breathable sports t-shirt.", price=29.99, category_id=2, featured=False, image="t-shirt/t-shirt4.jpg"),
        Product(name="Oversize T-shirt 1", description="Trendy oversize t-shirt.", price=22.99, category_id=2, featured=False, image="t-shirt/t-shirt5.jpg"),
        Product(name="Striped T-shirt 1", description="Blue striped t-shirt.", price=23.99, category_id=2, featured=False, image="t-shirt/t-shirt6.jpg"),
        Product(name="V-neck T-shirt 1", description="Light gray v-neck t-shirt.", price=20.99, category_id=2, featured=False, image="t-shirt/t-shirt7.jpg"),
        Product(name="Long Sleeve T-shirt 1", description="Khaki long sleeve t-shirt.", price=25.99, category_id=2, featured=False, image="t-shirt/t-shirt8.jpg"),
        Product(name="Vintage T-shirt 1", description="Vintage style t-shirt.", price=27.99, category_id=2, featured=False, image="t-shirt/t-shirt9.jpg"),
        Product(name="Printed T-shirt 1", description="Tropical print t-shirt.", price=26.99, category_id=2, featured=False, image="t-shirt/t-shirt10.jpg"),
        # Jeans
        Product(name="Slim Jeans 1", description="Dark blue slim jeans.", price=49.99, category_id=3, featured=True, image="pantalon/1.jpg"),
        Product(name="Skinny Jeans 1", description="Black skinny jeans.", price=54.99, category_id=3, featured=False, image="pantalon/2.jpg"),
        Product(name="Straight Jeans 1", description="Classic straight cut jeans.", price=44.99, category_id=3, featured=False, image="pantalon/3.jpg"),
        Product(name="Boyfriend Jeans 1", description="Faded boyfriend jeans.", price=59.99, category_id=3, featured=False, image="pantalon/4.jpg"),
        Product(name="Mom Jeans 1", description="High-waisted mom jeans.", price=52.99, category_id=3, featured=False, image="pantalon/5.jpg"),
        Product(name="Bootcut Jeans 1", description="Light blue bootcut jeans.", price=48.99, category_id=3, featured=False, image="pantalon/6.jpg"),
        Product(name="Flare Jeans 1", description="70s flare jeans.", price=56.99, category_id=3, featured=False, image="pantalon/7.jpg"),
        Product(name="Destroyed Jeans 1", description="Worn effect destroyed jeans.", price=53.99, category_id=3, featured=False, image="pantalon/8.jpg"),
        Product(name="Cropped Jeans 1", description="Ankle cropped jeans.", price=47.99, category_id=3, featured=False, image="pantalon/9.jpg"),
        Product(name="Wide Jeans 1", description="Comfortable wide jeans.", price=51.99, category_id=3, featured=False, image="pantalon/10.jpg"),
        # Shoes
        Product(name="New Balance Sneakers", description="Timeless white sneakers.", price=69.99, category_id=4, featured=True, image="shoes/sh1.jpg"),
        Product(name="Summer Sandals", description="Flat leather sandals.", price=39.99, category_id=4, featured=False, image="shoes/sh2.jpg"),
        Product(name="Air Force White", description="High suede boots.", price=99.99, category_id=4, featured=False, image="shoes/sh3.jpg"),
        Product(name="Brown Heels", description="Black heeled pumps.", price=79.99, category_id=4, featured=False, image="shoes/sh4.jpg"),
        Product(name="Black Heels", description="Brown leather loafers.", price=59.99, category_id=4, featured=False, image="shoes/sh5.jpg"),
        Product(name="Adidas Campus Gray", description="Lightweight running sneakers.", price=74.99, category_id=4, featured=False, image="shoes/sh6.jpg"),
        Product(name="Beach Flip Flops 1", description="Colorful summer flip flops.", price=14.99, category_id=4, featured=False, image="shoes/sh7.jpg"),
        Product(name="Adidas Samba White", description="Elegant dress shoes.", price=89.99, category_id=4, featured=False, image="shoes/sh8.jpg"),
        Product(name="Ballet Flats", description="Comfortable ballet flats.", price=34.99, category_id=4, featured=False, image="shoes/sh9.jpg"),
        Product(name="White Sandals", description="Trendy high-top sneakers.", price=64.99, category_id=4, featured=False, image="shoes/sh10.jpg"),
        # Accessories
        Product(name="Handbag", description="Black leather handbag.", price=49.99, category_id=5, featured=True, image="accessoires/sac.jpg"),
        Product(name="Classic Belt", description="Brown leather belt.", price=19.99, category_id=5, featured=False, image="accessoires/ceinture.jpg"),
        Product(name="Elegant Watch", description="Gold watch for women.", price=89.99, category_id=5, featured=False, image="accessoires/montre.jpg"),
        Product(name="Sunglasses", description="Round sunglasses.", price=29.99, category_id=5, featured=False, image="accessoires/lunette.jpg"),
        Product(name="Summer Hat", description="Light straw hat.", price=24.99, category_id=5, featured=False, image="accessoires/chap.jpg"),
        Product(name="Winter Scarf", description="Hand-knitted warm winter scarf.", price=27.99, category_id=5, featured=False, image="accessoires/echarpe.jpg"),
        Product(name="Wallet", description="Practical small wallet.", price=14.99, category_id=5, featured=False, image="accessoires/pm.jpg"),
        Product(name="Earrings", description="Gold-plated stainless steel teardrop earrings.", price=17.99, category_id=5, featured=False, image="accessoires/boucle.jpg"),
        Product(name="Chic Bracelet", description="Our Gold and White Clover Flower Charm Bracelet.", price=22.99, category_id=5, featured=False, image="accessoires/bracelet.jpg"),
        Product(name="Parisian Beret", description="Red wool beret.", price=18.99, category_id=5, featured=False, image="accessoires/beret.jpg"),
    ]
    db.session.add_all(products)
    db.session.commit()

# Routes principales
@app.route('/')
def home():
    featured_products = Product.query.filter_by(featured=True).limit(4).all()
    categories = Category.query.all()
    return render_template('index.html', featured_products=featured_products, categories=categories)

# Route dynamique pour toutes les catégories
@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, products=products)

# Routes produits
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('category.html', products=all_products, category_name="All Products")

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Autres routes
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart', methods=['GET'])
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0.0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_items.append({'product': product, 'quantity': quantity})
            total_price += product.price * quantity
    categories = Category.query.all()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Identifiants fictifs pour la démo
        if email == 'admin@example.com' and password == 'admin':
            return redirect(url_for('home'))
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not name or not email or not password or not confirm_password:
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            # Ici, tu pourrais ajouter l'utilisateur à la base
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Ici, tu pourrais enregistrer la commande dans la base de données
    session.pop('cart', None)
    return render_template('cart.html', cart_items=[], total_price=0.0)

# API Endpoint
@app.route('/api/cart/count')
def get_cart_count():
    return jsonify({'count': 0})

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        init_db()
    app.run(debug=True)