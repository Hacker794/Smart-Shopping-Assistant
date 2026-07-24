const PRODUCTS = [
    {
        id: 1,
        name: "Oat Milk 1L",
        price: 1.35,
        aisle: "Dairy Alternatives",
        image: "🥛"
    },
    {
        id: 2,
        name: "Sourdough Loaf",
        price: 2.20,
        aisle: "Bakery",
        image: "🥖"
    },
    {
        id: 3,
        name: "Bananas 5 Pack",
        price: 1.10,
        aisle: "Fruit and Vegetables",
        image: "🍌"
    },
    {
        id: 4,
        name: "Free Range Eggs",
        price: 2.75,
        aisle: "Dairy",
        image: "🥚"
    },
    {
        id: 5,
        name: "Penne Pasta 500g",
        price: 1.25,
        aisle: "Cupboard",
        image: "🍝"
    },
    {
        id: 6,
        name: "Tomato Pasta Sauce",
        price: 1.80,
        aisle: "Cupboard",
        image: "🍅"
    },
    {
        id: 7,
        name: "Chicken Breast 500g",
        price: 4.50,
        aisle: "Meat",
        image: "🍗"
    },
    {
        id: 8,
        name: "Greek Yoghurt",
        price: 1.95,
        aisle: "Dairy",
        image: "🥣"
    },
    {
        id: 9,
        name: "Orange Juice 1L",
        price: 2.10,
        aisle: "Drinks",
        image: "🧃"
    },
    {
        id: 10,
        name: "Dark Chocolate",
        price: 1.60,
        aisle: "Snacks",
        image: "🍫"
    },
    {
        id: 11,
        name: "Avocado Twin Pack",
        price: 1.85,
        aisle: "Fruit and Vegetables",
        image: "🥑"
    },
    {
        id: 12,
        name: "Cheddar Cheese 350g",
        price: 3.25,
        aisle: "Dairy",
        image: "🧀"
    },
    {
        id: 13,
        name: "Still Water 1.5L",
        price: 0.85,
        aisle: "Drinks",
        image: "💧"
    },
    {
        id: 14,
        name: "Salted Crisps",
        price: 1.50,
        aisle: "Snacks",
        image: "🥔"
    },
    {
        id: 15,
        name: "Plant-Based Burgers",
        price: 3.75,
        aisle: "Dairy Alternatives",
        image: "🍔"
    },
    {
        id: 16,
        name: "Frozen mixed berries",
        price: 3.40,
        aisle: "Frozen",
        image: "🫐"
    }
];

const productResults = document.querySelector("#product-results");
const searchInput = document.querySelector("#search");
const aisleFilter = document.querySelector("#aisle-filter");
const sortProducts = document.querySelector("#sort-products");

const resultCount = document.querySelector("#result-count");
const heroProductCount = document.querySelector("#hero-product-count");

const basketItems = document.querySelector("#basket-items");
const basketCount = document.querySelector("#basket-count");
const summaryItemCount = document.querySelector(
    "#summary-item-count"
);
const basketTotal = document.querySelector("#basket-total");

const emptyBasketMessage = document.querySelector(
    "#empty-basket-message"
);

const clearBasketButton = document.querySelector(
    "#clear-basket"
);

let basket = [];

function formatPrice(price) {
    return `£${price.toFixed(2)}`;
}

function populateAisleFilter() {
    const aisles = [
        ...new Set(
            PRODUCTS.map(function (product) {
                return product.aisle;
            })
        )
    ].sort();

    aisles.forEach(function (aisle) {
        const option = document.createElement("option");

        option.value = aisle;
        option.textContent = aisle;

        aisleFilter.appendChild(option);
    });
}

function getFilteredProducts() {
    const searchTerm = searchInput.value
        .trim()
        .toLowerCase();

    const selectedAisle = aisleFilter.value;
    const selectedSort = sortProducts.value;

    let filteredProducts = PRODUCTS.filter(
        function (product) {
            const matchesSearch = product.name
                .toLowerCase()
                .includes(searchTerm);

            const matchesAisle =
                selectedAisle === "all" ||
                product.aisle === selectedAisle;

            return matchesSearch && matchesAisle;
        }
    );

    if (selectedSort === "price-low") {
        filteredProducts.sort(function (firstProduct, secondProduct) {
            return firstProduct.price - secondProduct.price;
        });
    }

    if (selectedSort === "price-high") {
        filteredProducts.sort(function (firstProduct, secondProduct) {
            return secondProduct.price - firstProduct.price;
        });
    }

    if (selectedSort === "name") {
        filteredProducts.sort(function (firstProduct, secondProduct) {
            return firstProduct.name.localeCompare(
                secondProduct.name
            );
        });
    }

    return filteredProducts;
}

function renderProducts() {
    const filteredProducts = getFilteredProducts();

    resultCount.textContent = filteredProducts.length;

    if (filteredProducts.length === 0) {
        productResults.innerHTML = `
            <p class="no-results">
                No products match your search.
                Try another name or aisle.
            </p>
        `;

        return;
    }

    productResults.innerHTML = filteredProducts
        .map(function (product) {
            return `
                <article class="product-card">
                    <div
                        class="product-image"
                        aria-hidden="true"
                    >
                        ${product.image}
                    </div>

                    <div class="product-information">
                        <p class="product-aisle">
                            ${product.aisle}
                        </p>

                        <h3>${product.name}</h3>

                        <p class="product-price">
                            ${formatPrice(product.price)}
                        </p>

                        <button
                            type="button"
                            class="add-button"
                            data-product-id="${product.id}"
                            aria-label="Add ${product.name} to basket"
                        >
                            Add to basket
                        </button>
                    </div>
                </article>
            `;
        })
        .join("");
}

function addProductToBasket(productId) {
    const selectedProduct = PRODUCTS.find(
        function (product) {
            return product.id === productId;
        }
    );

    if (!selectedProduct) {
        return;
    }

    basket.push(selectedProduct);

    renderBasket();
}

function removeProductFromBasket(itemIndex) {
    basket.splice(itemIndex, 1);

    renderBasket();
}

function calculateBasketTotal() {
    return basket.reduce(
        function (runningTotal, product) {
            return runningTotal + product.price;
        },
        0
    );
}

function renderBasket() {
    basketItems.innerHTML = basket
        .map(function (product, index) {
            return `
                <li class="basket-item">
                    <div>
                        <p class="basket-item-name">
                            ${product.name}
                        </p>

                        <p class="basket-item-price">
                            ${formatPrice(product.price)}
                        </p>
                    </div>

                    <button
                        type="button"
                        class="remove-button"
                        data-basket-index="${index}"
                        aria-label="Remove ${product.name} from basket"
                    >
                        Remove
                    </button>
                </li>
            `;
        })
        .join("");

    const itemTotal = basket.length;
    const priceTotal = calculateBasketTotal();

    basketCount.textContent = itemTotal;
    summaryItemCount.textContent = itemTotal;
    basketTotal.textContent = formatPrice(priceTotal);

    emptyBasketMessage.hidden = itemTotal > 0;
    clearBasketButton.disabled = itemTotal === 0;
}

function clearBasket() {
    basket = [];

    renderBasket();
}

productResults.addEventListener(
    "click",
    function (event) {
        const addButton = event.target.closest(
            ".add-button"
        );

        if (!addButton) {
            return;
        }

        const productId = Number(
            addButton.dataset.productId
        );

        addProductToBasket(productId);
    }
);

basketItems.addEventListener(
    "click",
    function (event) {
        const removeButton = event.target.closest(
            ".remove-button"
        );

        if (!removeButton) {
            return;
        }

        const basketIndex = Number(
            removeButton.dataset.basketIndex
        );

        removeProductFromBasket(basketIndex);
    }
);

searchInput.addEventListener(
    "input",
    renderProducts
);

aisleFilter.addEventListener(
    "change",
    renderProducts
);

sortProducts.addEventListener(
    "change",
    renderProducts
);

clearBasketButton.addEventListener(
    "click",
    clearBasket
);

heroProductCount.textContent = PRODUCTS.length;

populateAisleFilter();
renderProducts();
renderBasket();