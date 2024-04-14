import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8388"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    # adds new shit
    input("Press Enter to continue creating products!")
    print("\nAdding a new product: 'Milk Cream' (7.99)")
    post("/api/products/", {"name": "Milk Cream", "price": 7.99})
    
    
    
    #new shit
    print("\nAdding a new product: 'Soy Banana' (4.99)")
    post("/api/products/", {"name": "Soy Banana", "price": 4.99})
    
    
    
    #new shit
    print("\nAdding a new product: 'Chicken Fries' (1009.99)")
    post("/api/products/", {"name": "Chicken Fries", "price": 1009.99})
    
    
    print("\nAdding a new product: 'Turtle Snappers' (10.99)")
    post("/api/products/", {"name": "Chicken Fries", "price": 1009.99})
    
    
    
    
    
    input("\nCheck for new products in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")




 




    # NEW ORDERSS
    
    
    
    input("\n BAD ORDER")
    print("\nTHIS ORDER IS TOO BIG. CUSTOMER 15 WANTS (TOMATOES:  15) AND (BREAD:  20) ")
    post("/api/orders/", 
    {
        "customer_id": 15,
        "items": [
            {
                "name": "tomato",
                "quantity": 15
            },
            {
                "name": "bread",
                "quantity": 20
            }
        ]
    })
    
    
    
    
    
    
    
    
    
    print("\nGOOD ORDERS:(CHEESE : 1),(SOY BANANA: 1)(CHICKEN THIGH: 1) ")
    post("/api/orders/",
    {
        "customer_id": 18,
        "items": [
            {
                "name": "cheese",
                "quantity": 1
            },
            {
                "name": "Soy Banana",
                "quantity": 1
            },
            {
                "name": "chicken thigh",
                "quantity": 1
            }
        ]
    })
    print("\nGOOD ORDERS: {CHICKEN FRIES = 2}, {GROUND BEEF: 3} ")
    post("/api/orders/", 
    {
        "customer_id": 9,
        "items": [
            {
                "name": "Chicken Fries",
                "quantity": 2
            },
            {
                "name": "ground beef",
                "quantity": 3
            }
        ]
    })
    input("\nCHECK WEB.")
    webbrowser.open(FLASK_URL + "/orders")

    input("\nINVALID ORDER, THIS WILL RETURN AN ERROR")
    post("/api/orders/", 
    {
        "customer_id": 4,
        "items": [
            {
                "name": "Chicken Fries",
                "quantity": 10
            },
            {
                "name": "honey",
                "quantity": 10
            }
        ]
    })

    input("\nNO NAME, THIS ONE WILL RETURN AN ERROR. ")
    print("This adds to Customer 8 an order with 7 chicken breast and 45 of an unknown product. This is NOT ALLOWED")
    post("/api/orders/", 
    {
        "customer_id": 8,
        "items": [
            {
                "name": "chicken breast",
                "quantity": 7
            },
            {
                "quantity": 45
            }
        ]
    })

    input("\nADDS PRODUCT WITH AN INVALID PRICE, THIS ONE WILL RETURN AN ERROR")
    print("Adding a new product: 'Silken Banana' (-5.99)")
    post("/api/products/", {"name": "Silken Banana", "price": -5.99})


    input("\n NEW BAD CUSTOMER")
    
    print("\nTHIS PERSON WILL HAVE NEGATIVE VALUE AND WILL ORDER SOMETHING INVALID")
    post("/api/customers/", 
         {
             "name": "Rafeel", 
             "phone": "555-5555-5555", 
             "balance": -1000
            })
    
    input("\n NOW THEY WILL HAVE AN ORDER, BUT THEY HAVE NEGATIVE BALANCE, SO THIS WILL NOT REGISTER OR APPEAR IN ORDER.")
    post("/api/orders/", 
         {
             "customer_id": 21,
             "items": [
                 {
                     "name": "chicken breast",
                     "quantity": 1
                 }
             ]
         })
    
    
    print("\nTHIS PERSON WILL HAVE NEGATIVE VALUE AND WILL ORDER SOMETHING INVALID")
    post("/api/customers/", 
         {
             "name": "BOB", 
             "phone": "555-5555-5555", 
             "balance": 1
            })
    
    input("\n NOW THEY WILL HAVE AN ORDER, BUT THEY HAVE NEGATIVE BALANCE, SO THIS WILL NOT REGISTER OR APPEAR IN ORDER.")
    post("/api/orders/", 
    {
        "customer_id": 22,
        "items": [
            {
                "name": "Chicken Fries",
                "quantity": 1
            }
        ]
    })
    
    
    


if __name__ == "__main__":
    demo()