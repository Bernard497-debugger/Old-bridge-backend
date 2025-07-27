import os
from flask import Flask, request, render_template_string, redirect, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

products = []

@app.route('/')
def store():
    return render_template_string("""
    <html>
    <head>
        <title>Khali Commerce</title>
        <style>
            body {
                background: #111;
                color: #eee;
                font-family: 'Segoe UI', sans-serif;
                padding: 20px;
                font-size: 18px;
            }
            h2, h3 { font-size: 28px; }
            .product {
                display: inline-block;
                width: 200px;
                background: #222;
                border: 1px solid #333;
                margin: 15px;
                padding: 15px;
                border-radius: 12px;
                cursor: pointer;
                transition: 0.3s;
            }
            .product:hover {
                background: #333;
                transform: scale(1.03);
            }
            .product img {
                width: 100%;
                height: 130px;
                object-fit: cover;
                border-radius: 8px;
            }
            .cart {
                margin-top: 40px;
                padding: 25px;
                background: #1b1b1b;
                border-radius: 12px;
            }
            input, button {
                padding: 14px;
                margin: 8px 0;
                border-radius: 6px;
                border: none;
                width: 100%;
                font-size: 16px;
            }
            button {
                background: #00aaff;
                color: white;
                cursor: pointer;
                font-weight: bold;
            }
            footer {
                margin-top: 60px;
                padding: 20px;
                background: #000;
                text-align: center;
                font-size: 16px;
                color: #aaa;
                border-top: 1px solid #444;
            }
        </style>
    </head>
    <body>
        <h2>💻 Khali Commerce Tech Store</h2>
        <p>🖱️ Tap any item to add to cart</p>

        <div id="product-list">
            {% for p in products %}
            <div class="product" onclick="addToCart('{{ p['name'] }}', '{{ p['price'] }}')">
                <img src="/uploads/{{ p['image'] }}" alt="{{ p['name'] }}">
                <b>{{ p['name'] }}</b><br>{{ p['price'] }} Pula
            </div>
            {% endfor %}
        </div>

        <div class="cart">
            <h3>🛒 Cart</h3>
            <ul id="cart-items"></ul>
            <form onsubmit="checkout(); return false;">
                <input id="username" placeholder="Your Name" required><br>
                <input id="location" placeholder="Your Location" required><br>
                <button type="submit">Checkout via WhatsApp</button>
            </form>
        </div>

        <footer>
            &copy; {{year}} Khali Digital Industry | Powered by Flask
        </footer>

        <script>
            let cart = [];

            function addToCart(name, price) {
                cart.push({ name, price });
                renderCart();
            }

            function renderCart() {
                const list = document.getElementById('cart-items');
                list.innerHTML = '';
                cart.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item.name} - ${item.price} Pula`;
                    list.appendChild(li);
                });
            }

            function checkout() {
                const name = document.getElementById('username').value;
                const location = document.getElementById('location').value;
                let msg = `Hi, I'm ${name} from ${location}. I'd like to buy:%0A`;
                cart.forEach(i => msg += `• ${i.name} - ${i.price} Pula%0A`);
                window.open(`https://wa.me/26772927417?text=${msg}`, '_blank');
            }
        </script>
    </body>
    </html>
    """, products=products, year=2025)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        products.append({'name': name, 'price': price, 'image': filename})
        return redirect('/admin')
    return '''
    <h2 style="font-family: sans-serif;">Admin Panel – Upload Product</h2>
    <form method="post" enctype="multipart/form-data">
        Name: <input type="text" name="name" required><br>
        Price: <input type="text" name="price" required><br>
        Image: <input type="file" name="image" accept="image/*" required><br><br>
        <button type="submit">Upload</button>
    </form>
    <br><a href="/">Back to Store</a>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)