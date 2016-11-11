CREATE TABLE category (
    category_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_name NVARCHAR(255) NOT NULL UNIQUE,
    category_url NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE product (
    product_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_name NVARCHAR(255) NOT NULL,
    product_url NVARCHAR(255) NOT NULL,
    product_price NVARCHAR(255),
    product_image_url NVARCHAR(1500),
    category_id BIGINT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    UNIQUE KEY my_unique_key (product_name, product_url, category_id)
);