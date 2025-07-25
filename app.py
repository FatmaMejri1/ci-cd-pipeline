from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse as url_parse
from models import db, Product, Category, User
from forms import LoginForm, RegistrationForm
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
app.config['LOGIN_DISABLED'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        Product(name="Mocha Lantern Sleeve Mini Dress", description="A chic mocha mini dress featuring lantern sleeves and a ruched bust for a sophisticated silhouette.", price=79.99, category_id=1, featured=True, image="dr/dress1.jpg"),
        Product(name="Red Princess Floral Dress", description="Radiate elegance in this short red dress adorned with delicate floral patterns—perfect for summer occasions.", price=59.99, category_id=1, featured=False, image="dr/dress2.jpg"),
        Product(name="Blush Pink Day Dress", description="A sweet and airy blush pink dress, ideal for casual outings and sunny days.", price=49.99, category_id=1, featured=False, image="dr/dress3.jpg"),
        Product(name="Emerald Casual Midi Dress", description="Effortlessly stylish, this green midi dress is your go-to for relaxed, everyday chic.", price=89.99, category_id=1, featured=False, image="dr/dress4.jpg"),
        Product(name="Vintage Lace White Dress", description="Timeless white dress with intricate lace details, exuding vintage charm and grace.", price=69.99, category_id=1, featured=False, image="dr/dress5.jpg"),
        Product(name="Classic Rose Wrap Dress", description="A soft pink wrap dress that flatters every figure—versatile for any event.", price=74.99, category_id=1, featured=False, image="dr/dress6.jpg"),
        Product(name="Satin Noir Korean Dress", description="Trendy black satin dress inspired by Korean fashion, perfect for evening outings.", price=64.99, category_id=1, featured=False, image="dr/dress7.jpg"),
        Product(name="Olive Strapless Party Dress", description="Make a statement in this chic olive green strapless dress, designed for celebrations.", price=84.99, category_id=1, featured=False, image="dr/dress8.jpg"),
        Product(name="Midnight Pleated Dress", description="Elegant black dress with a pleated skirt, ideal for sophisticated evenings.", price=54.99, category_id=1, featured=False, image="dr/dress9.jpg"),
        Product(name="Winterberry White Maxi Dress", description="Long-sleeved white maxi dress with subtle berry print, perfect for winter elegance.", price=99.99, category_id=1, featured=False, image="dr/dress10.jpg"),
        # T-shirts
        Product(name="Green Cropped Essential Top", description="A classic green cropped t-shirt, soft and comfortable for everyday wear.", price=19.99, category_id=2, featured=True, image="t-shirt/t-shirt1.jpg"),
        Product(name="Retro Green Crew Tee", description="Vintage-inspired green crew neck t-shirt, a timeless wardrobe staple.", price=21.99, category_id=2, featured=False, image="t-shirt/t-shirt2.jpg"),
        Product(name="Scarlet Graphic Tee", description="Bold red t-shirt with a unique graphic print for a standout look.", price=24.99, category_id=2, featured=False, image="t-shirt/t-shirt3.jpg"),
        Product(name="Azure Blue Casual Tee", description="A soft blue t-shirt, perfect for a relaxed and casual style.", price=29.99, category_id=2, featured=False, image="t-shirt/t-shirt4.jpg"),
        Product(name="Maroon Summer Crop Tank", description="Trendy maroon crop tank top, ideal for warm weather and layering.", price=22.99, category_id=2, featured=False, image="t-shirt/t-shirt5.jpg"),
        Product(name="Pink Girly Satin Tee", description="A playful pink satin t-shirt, adding a girly touch to your outfit.", price=23.99, category_id=2, featured=False, image="t-shirt/t-shirt6.jpg"),
        Product(name="Chic Blue V-Neck Tee", description="Light blue v-neck t-shirt, effortlessly chic for any occasion.", price=20.99, category_id=2, featured=False, image="t-shirt/t-shirt7.jpg"),
        Product(name="Rosy Ruched Off-Shoulder Top", description="Rose-colored ruched t-shirt with off-shoulder neckline and bow detail for a feminine flair.", price=25.99, category_id=2, featured=False, image="t-shirt/t-shirt8.jpg"),
        Product(name="Khaki Long Sleeve Tee", description="Classic khaki long sleeve t-shirt, perfect for layering in cooler weather.", price=27.99, category_id=2, featured=False, image="t-shirt/t-shirt9.jpg"),
        Product(name="Vintage Tropic Print Tee", description="Retro-style t-shirt with a vibrant tropical print for a fun, vintage vibe.", price=26.99, category_id=2, featured=False, image="t-shirt/t-shirt10.jpg"),
        # Jeans
        Product(name="Indigo Slim Fit Jeans", description="Slim fit jeans in deep indigo denim, flattering and versatile.", price=49.99, category_id=3, featured=True, image="pantalon/1.jpg"),
        Product(name="Jet Black Skinny Jeans", description="Classic black skinny jeans for a sleek, modern look.", price=54.99, category_id=3, featured=False, image="pantalon/2.jpg"),
        Product(name="Heritage Straight Jeans", description="Timeless straight cut jeans in a classic blue wash.", price=44.99, category_id=3, featured=False, image="pantalon/3.jpg"),
        Product(name="Faded Boyfriend Jeans", description="Relaxed boyfriend jeans with a stylish faded finish.", price=59.99, category_id=3, featured=False, image="pantalon/4.jpg"),
        Product(name="Sky Blue Mom Jeans", description="High-waisted mom jeans in a light sky blue, both trendy and comfy.", price=52.99, category_id=3, featured=False, image="pantalon/5.jpg"),
        Product(name="Light Bootcut Denim", description="Bootcut jeans in a light blue shade, perfect for a retro touch.", price=48.99, category_id=3, featured=False, image="pantalon/6.jpg"),
        Product(name="Seventies Flare Jeans", description="Channel the 70s with these dramatic flare jeans in classic denim.", price=56.99, category_id=3, featured=False, image="pantalon/7.jpg"),
        Product(name="Distressed Edge Jeans", description="Destroyed jeans with a worn-in, edgy look.", price=53.99, category_id=3, featured=False, image="pantalon/8.jpg"),
        Product(name="Cropped Ankle Jeans", description="Trendy cropped jeans that highlight your favorite shoes.", price=47.99, category_id=3, featured=False, image="pantalon/9.jpg"),
        Product(name="Wide Leg Comfort Jeans", description="Relaxed wide leg jeans for ultimate comfort and style.", price=51.99, category_id=3, featured=False, image="pantalon/10.jpg"),
        # Shoes
        Product(name="New Balance Classic Sneakers", description="Timeless white sneakers from New Balance, perfect for everyday wear.", price=69.99, category_id=4, featured=True, image="shoes/sh1.jpg"),
        Product(name="Summer Leather Sandals", description="Flat leather sandals designed for comfort and summer style.", price=39.99, category_id=4, featured=False, image="shoes/sh2.jpg"),
        Product(name="Air Force White Boots", description="High-top white boots with a suede finish for a bold statement.", price=99.99, category_id=4, featured=False, image="shoes/sh3.jpg"),
        Product(name="Espresso Block Heel Pumps", description="Elegant pumps with a block heel in a rich espresso shade.", price=79.99, category_id=4, featured=False, image="shoes/sh4.jpg"),
        Product(name="Chestnut Loafer Heels", description="Classic loafers in brown leather with a modern heel twist.", price=59.99, category_id=4, featured=False, image="shoes/sh5.jpg"),
        Product(name="Adidas Campus Gray Runners", description="Lightweight gray running sneakers from Adidas Campus collection.", price=74.99, category_id=4, featured=False, image="shoes/sh6.jpg"),
        Product(name="Red Classy Sandals", description="Flat red sandals with a classy design, perfect for summer outings.", price=14.99, category_id=4, featured=False, image="shoes/sh7.jpg"),
        Product(name="Adidas Samba White Dress Shoes", description="Elegant white dress shoes from Adidas Samba, ideal for formal occasions.", price=89.99, category_id=4, featured=False, image="shoes/sh8.jpg"),
        Product(name="Ballet Comfort Flats", description="Soft and comfortable ballet flats for all-day wear.", price=34.99, category_id=4, featured=False, image="shoes/sh9.jpg"),
        Product(name="White High-Top Sandals", description="Trendy white sandals with a high-top silhouette for a modern look.", price=64.99, category_id=4, featured=False, image="shoes/sh10.jpg"),
        # Accessories
        Product(name="Cognac Leather Handbag", description="Elegant cognac brown leather handbag, perfect for any occasion.", price=49.99, category_id=5, featured=True, image="accessoires/sac.jpg"),
        Product(name="Classic Brown Belt", description="Timeless brown leather belt with a polished silver buckle.", price=19.99, category_id=5, featured=False, image="accessoires/ceinture.jpg"),
        Product(name="Golden Luxe Watch", description="A luxurious gold watch for women, combining elegance and precision.", price=89.99, category_id=5, featured=False, image="accessoires/montre.jpg"),
        Product(name="Retro Round Sunglasses", description="Trendy round sunglasses with dark lenses for a retro vibe.", price=29.99, category_id=5, featured=False, image="accessoires/lunette.jpg"),
        Product(name="Straw Sun Hat", description="Lightweight straw hat, your perfect companion for sunny days.", price=24.99, category_id=5, featured=False, image="accessoires/chap.jpg"),
        Product(name="Hand-Knit Winter Scarf", description="Warm, hand-knitted scarf to keep you cozy all winter long.", price=27.99, category_id=5, featured=False, image="accessoires/echarpe.jpg"),
        Product(name="Petite Essentials Wallet", description="Compact and practical wallet for your daily essentials.", price=14.99, category_id=5, featured=False, image="accessoires/pm.jpg"),
        Product(name="Gold Teardrop Earrings", description="Elegant gold-plated teardrop earrings for a touch of sophistication.", price=17.99, category_id=5, featured=False, image="accessoires/boucle.jpg"),
        Product(name="Clover Charm Bracelet", description="Delicate gold and white clover flower charm bracelet for a subtle accent.", price=22.99, category_id=5, featured=False, image="accessoires/bracelet.jpg"),
        Product(name="Parisian Red Wool Beret", description="Classic red wool beret, the ultimate Parisian accessory.", price=18.99, category_id=5, featured=False, image="accessoires/beret.jpg"),
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

# Authentication routes
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return render_template('login.html', title='Sign In', form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

# Other routes
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

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process payment logic here
        session.pop('cart', None)
        return redirect(url_for('home'))
    return render_template('payment.html')

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

# API Endpoint
@app.route('/api/cart/count')
def get_cart_count():
    return jsonify({'count': 0})

with app.app_context():
    if not os.path.exists(os.path.join(basedir, 'instance', 'db.sqlite')):
        db.create_all()
        init_db()
if __name__ == '__main__':
    app.run(port=5000, debug=False)