document.addEventListener('DOMContentLoaded', function() {
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
        // Send an AJAX request to your Flask server to add the book to the cart
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
            'book_title': book_title,
            'book_author': book_author,
            'book_description': book_description,
        };
        xhr.send(JSON.stringify(data));
    }
});