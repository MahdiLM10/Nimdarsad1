from Shop.models import Product,Profile
import json


class Cart:
    def __init__(self,request):
        self.session = request.session
        self.request = request

        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        self.cart = cart 

    # def add(self,product,quantity):
    #     product_id = str(product.id)
    #     prduct_qty = str(quantity)

    #     if product_id in self.cart:
    #         pass
    #     else:
    #         self.cart[product_id] = int(prduct_qty)

        
    #     self.session.modified = True

    #     if self.request.user.is_authenticated:
    #         currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #         db_cart = str(self.cart).replace('\'','\"')

    #         currect_user.update(old_cart=str(db_cart))
    def add(self, product, quantity, color):
        product_id = str(product.id)
        product_qty = int(quantity)  # Convert quantity to integer

        # Create a dictionary to hold the product details
        product_details = {
            'quantity': product_qty,
            'color': color
        }

        # Check if the product is already in the cart
        if product_id in self.cart:
            # Update quantity and color if the product exists
            self.cart[product_id]['quantity'] = product_qty  # Update quantity
            self.cart[product_id]['color'] = color  # Update color (optional, if color can change)
        else:
            # Add new product to the cart
            self.cart[product_id] = product_details

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace("'", "\"")  # Convert to JSON-like format
            current_user.update(old_cart=str(db_cart))
            
            
    

    # def clear_cart(self):
    #     if self.request.user.is_authenticated:
    #         # Get the current user's profile
    #         current_user = Profile.objects.get(user=self.request.user)

    #         # Extract the old_cart string
    #         old_cart_str = current_user.old_cart

    #         # Parse the old_cart string into a dictionary
    #         try:
    #             old_cart = json.loads(old_cart_str.replace("'", "\""))  # Convert to a proper JSON format
    #         except json.JSONDecodeError:
    #             old_cart = {}  # In case of an error, initialize as empty

    #         # Get all product IDs from the old_cart
    #         product_ids = list(old_cart.keys())  # Assuming keys are product IDs

    #         # Now, you can delete all items from the cart
    #         for product_id in product_ids:
    #             if product_id in self.cart:
    #                 del self.cart[product_id]  # Remove each product from the cart

    #         # Mark the session as modified
    #         self.session.modified = True

    #         # Optionally, update the old_cart in the database to reflect the changes
    #         current_user.old_cart = str(self.cart).replace("'", "\"")  # Convert back to string
    #         current_user.save()  # Save the changes to the user profile

    # def save(self):
    #     self.session['cart'] = self.cart
    #     self.session.modified = True
    
    # def cart_save_time(self, product, quantity, color):
    #     product_id = str(product)  # Assuming `product` is the product ID or object
    #     product_qty = int(quantity)  # Ensure quantity is an integer

    #     # Create a dictionary to hold product details
    #     product_details = {
    #         'quantity': product_qty,
    #         'color': color  # Store color as well
    #     }

    #     # Replace existing item or add new one
    #     self.cart[product_id] = product_details

    #     self.session.modified = True

    #     if self.request.user.is_authenticated:
    #         current_user = Profile.objects.filter(user__id=self.request.user.id)
            
    #         db_cart_old_save = str(self.cart).replace("'", "\"")  # Convert to JSON-like format
    #         current_user.update(old_save=str(db_cart_old_save))
    
    def clear(self,):
        # clear the cart only
        self.cart.clear()
        
        
        self.session.modified = True
    
    def __len__(self,):
        return len(self.cart)
    
    def get_colors(self,):
        list_get_value = []
        for key,value in self.cart.items():
            list_get_value.append(value['color'])
            
        return list_get_value

    def get_prods(self):
        product_ids = self.cart.keys()  # Get the product IDs from the cart
        if not product_ids:  # Check if there are no product IDs
            return Product.objects.none()  # Return an empty queryset
        products = Product.objects.filter(id__in=product_ids)  # Fetch products from the database
        return products  # Return the queryset of products
    
    
    def get_quants(self):
        quantities = {product_id: item['quantity'] for product_id, item in self.cart.items()}  # Extract quantities
        return quantities  # Return the dictionary of quantities

    def get_color(self,):
        colors = {product_id: item['color'] for product_id ,item in self.cart.items()}
        return colors
        
    def update(self, product_id, quantity, color):
        """Update the quantity and color of a product in the cart."""
        product_id = str(product_id)
        
        # Debugging: Print the incoming values
        print(f"Product ID: {product_id}, Quantity: {quantity}, Color: {color}")
        
        try:
            product_qty = int(quantity)  # Convert quantity to integer
        except ValueError as e:
            print(f"Error converting quantity: {e}")
            return  # Or handle the error appropriately

        # Check if the product exists in the cart
        if product_id in self.cart:
            if product_qty > 0:
                # Update the quantity and color if it's greater than 0
                self.cart[product_id]['quantity'] = product_qty
                self.cart[product_id]['color'] = color  # Update color
            else:
                # If quantity is 0 or less, remove the item from the cart
                del self.cart[product_id]
        else:
            # Optionally, handle the case where the product does not exist
            print(f"Product ID {product_id} not found in the cart.")

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace("'", "\"")  # Convert to JSON-like format
            current_user.update(old_cart=str(db_cart))
            
    


    def delete(self, product):
        product_id = str(product)  # Ensure product_id is a string

        # Check if the product exists in the cart
        if product_id in self.cart:
            del self.cart[product_id]  # Remove the product from the cart

        self.session.modified = True  # Mark the session as modified

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace("'", "\"")  # Convert to JSON-like format
            current_user.update(old_cart=str(db_cart))


    #     return total
    def get_total(self):
        product_ids = self.cart.keys()  # Get the product IDs from the cart
        products = Product.objects.filter(id__in=product_ids)  # Fetch products from the database
        total = 0

        for product in products:
            product_id = str(product.id)  # Ensure product_id is a string to match keys in self.cart
            quantity = self.cart[product_id]['quantity']  # Get the quantity from the cart

            if product.is_sale:
                total += product.sale_price * quantity  # Calculate total for sale price
            else:
                total += product.price * quantity  # Calculate total for regular price

        return total
    

    def db_add(self, product, quantity, color):
        product_id = str(product)  # Assuming `product` is the product ID or object
        product_qty = int(quantity)  # Ensure quantity is an integer

        # Create a dictionary to hold product details
        product_details = {
            'quantity': product_qty,
            'color': color  # Store color as well
        }

        # Replace existing item or add new one
        self.cart[product_id] = product_details

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace("'", "\"")  # Convert to JSON-like format
            current_user.update(old_cart=str(db_cart))
    

    # def add_color(self,product_id,color):
    #     product_id = str(product_id.id)
    #     color_name = str(color)

    #     if product_id in self.cart:
    #         pass
    #     else:
    #         self.cart[product_id] = str(color_name)

        
    #     self.session.modified = True

    #     if self.request.user.is_authenticated:
    #         currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #         db_cart = str(self.cart).replace('\'','\"')

    #         currect_user.update_color(old_color=str(db_cart))
            
            
    # def update_color(self,product,color):
    #     productid = str(product)
    #     color_name = str(color)

    #     ourcart = self.cart
    #     ourcart[productid] = str(color_name)

    #     self.session.modified = True
    #     if self.request.user.is_authenticated:
    #         currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #         db_cart = str(self.cart).replace('\'','\"')

    #         currect_user.update(old_color=str(db_cart))

    #     alaki = self.cart 
    #     return alaki
    
    # def db_add_color(self,product,color):
    #         product_id = str(product)
    #         color_name = str(color)

    #         if product_id in self.cart:
    #             pass
    #         else:
    #             self.cart[product_id] = str(color_name)

            
    #         self.session.modified = True
            
    #         if self.request.user.is_authenticated:
    #             currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #             db_cart = str(self.cart).replace('\'','\"')

    #             currect_user.update(old_color=str(db_cart))
    
    
    
    # def update(self,product,quantity):
    #     productid = str(product)
    #     productqty = int(quantity)

    #     ourcart = self.cart
    #     ourcart[productid] = productqty

    #     self.session.modified = True
    #     if self.request.user.is_authenticated:
    #         currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #         db_cart = str(self.cart).replace('\'','\"')

    #         currect_user.update(old_cart=str(db_cart))

    #     alaki = self.cart 
    #     return alaki
    
    
    # def get_total(self,):
    #     product_ids = self.cart.keys(value.quantity)
    #     products = Product.objects.filter(id__in=product_ids)
    #     total = 0

    #     for key,value in self.cart.items(value.quantity):
    #         key = int(key)
    #         for product in products:
    #             if product.id == key:
    #                 if product.is_sale:
    #                     total = total + (product.sale_price*value)
    #                 else:
    #                     total = total + (product.price*value)
    
    
    # def delete(self,product):
    #     # product_id get 
    #     product_id = str(product)

    #     if product_id in self.cart:
    #         del self.cart[product_id]

    #     self.session.modified = True 
    #     if self.request.user.is_authenticated:
    #         currect_user = Profile.objects.filter(user__id = self.request.user.id)
    #         db_cart = str(self.cart).replace('\'','\"')

    #         currect_user.update(old_cart=str(db_cart))
    
    
    # def get_prods(self,):
    #     product_ids = self.cart.keys()
    #     product = Product.objects.filter(id__in=product_ids)
    #     return product
    
    # def get_quants(self,):
    #     quantitys = self.cart
    #     return quantitys