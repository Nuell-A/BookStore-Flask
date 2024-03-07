// Add to cart button in home page
document.addEventListener('DOMContentLoaded', function() {
    // Identifies button clicked and extracts data passed.
    var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    for (var i = 0; i < addToCartButtons.length; i++) {
        addToCartButtons[i].addEventListener('click', function() {
            var book_title = this.dataset.title;
            var book_author = this.dataset.author;
            var book_description = this.dataset.description;
            addToCart(book_title, book_author, book_description);
        });
    }

    function addToCart(book_title, book_author, book_description) {
        // Sends an AJAX request to routes.py (server) to add the book to the cart
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add-to-cart');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                alert('Book added to cart successfully!');
            } else {
                alert('Failed to add book to cart.');
            }
        };
        var data = {
            "book_title": book_title,
            "book_author": book_author,
            "book_description": book_description,
        };
        xhr.send(JSON.stringify(data));
    }
});

// Checkout button in cart page.
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for the Checkout button
    var checkoutButton = document.querySelector('.checkout-btn');
    checkoutButton.addEventListener('click', function() {
        var books_in_cart = this.dataset.books;
        checkout(books_in_cart);
    });

    function checkout(books_in_cart) {
        // Send an AJAX request to the server to process the checkout
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/checkout');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                alert('Checkout successful!');
                // Optionally, redirect to a different page after successful checkout
                window.location.href = '/thank-you';
            } else {
                alert('Failed to checkout.');
            }
        };
        xhr.send(JSON.stringify({ books_in_cart: books_in_cart }));
    }
});
