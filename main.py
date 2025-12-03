# from flask import Flask, render_template, abort, url_for, session, redirect
from flask import Flask, render_template, abort, url_for, session, redirect, request, jsonify
from db import insert_order

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# --- Product Data ---
products = {
    1: {
        "id": 1,
        "title": "Flower Vase (Blue)",
        "slug": "flower-vase-blue",
        "image": "FlowerVaseBlue.png",
        "price": 350,
        "currency": "₹",
        "short": "Elegant decorative vase for any room.",
        "description": """
A beautiful blue flower vase made from ceramic. Perfect for dining tables, shelves,
or as a centerpiece. Height: 20cm. Hand-wash recommended.
""",
    },
    2: {
        "id": 2,
        "title": "Honey Comb Puzzle",
        "slug": "honey-comb-puzzle",
        "image": "HoneyComb.png",
        "price": 450,
        "currency": "₹",
        "short": "Fun and creative puzzle toy.",
        "description": """
Honey-comb shaped wooden puzzle — great for brain training and decorative display.
Made with smooth edges and safe paint.
""",
    },
    3: {
        "id": 3,
        "title": "Hot Wheels Stand",
        "slug": "hot-wheels-stand",
        "image": "HotWheelsStand.png",
        "price": 350,
        "currency": "₹",
        "short": "Perfect for car collectors.",
        "description": """
A stylish display stand for Hot Wheels and model cars. Durable acrylic with a sleek finish.
Holds up to 8 cars in a compact footprint.
""",
    },
}

# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def index():
    featured = list(products.values())
    return render_template("index.html", featured=featured)

@app.route("/products")
def product_list():
    items = list(products.values())
    return render_template("products.html", products=items)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = products.get(product_id)
    if not product:
        abort(404)
    related = [p for p in products.values() if p["id"] != product_id]
    return render_template("product.html", product=product, related=related)


# ---------------------------
# CART SYSTEM
# ---------------------------

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in products:
        abort(404)

    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart

    return redirect("/cart")

@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        pid = int(pid)
        product = products.get(pid)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            items.append({"product": product, "qty": qty, "subtotal": subtotal})

    return render_template("cart.html", items=items, total=total)

@app.route("/remove/<int:product_id>")
def remove_item(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect("/cart")


@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = session.get("cart", {})

    # form keys are product ids (as strings); values are desired quantities
    for key, val in request.form.items():
        try:
            pid = int(key)
            qty = int(val)
        except ValueError:
            continue

        if qty <= 0:
            cart.pop(str(pid), None)
        else:
            cart[str(pid)] = qty

    session["cart"] = cart
    return redirect("/cart")


# ---------------------------
# CONTEXT PROCESSOR (image + cart count)
# ---------------------------

@app.context_processor
def utility_processor():
    def image_url(filename):
        return url_for("static", filename=f"images/{filename}")

    def cart_count():
        cart = session.get("cart", {})
        return sum(cart.values())

    return dict(image_url=image_url, cart_count=cart_count)


# New code for placing order
@app.route("/place-order", methods=["POST"])
def place_order():
    cart = session.get("cart", {})
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    orders_saved = []
    grand_total = 0

    for pid, qty in cart.items():
        pid = int(pid)
        product = products.get(pid)

        if not product:
            continue

        success, msg = insert_order(
            product_id=pid,
            quantity=qty,
            price=product["price"]
        )

        subtotal = product["price"] * qty
        grand_total += subtotal

        orders_saved.append({
            "product_id": pid,
            "product_title": product.get("title"),
            "quantity": qty,
            "subtotal": subtotal,
            "status": msg,
            "success": success,
        })

    # Clear cart after attempting to save orders
    session["cart"] = {}

    # Render a friendly HTML confirmation page
    return render_template(
        "order_success.html",
        message="Order placed",
        details=orders_saved,
        total=grand_total,
    )


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
