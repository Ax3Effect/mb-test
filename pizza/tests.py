from django.test import TestCase
from rest_framework.test import APIClient
from nose.tools import ok_, eq_
from pizza.models import MenuItem, MenuItemSize
from decimal import Decimal
from rest_framework.test import APITestCase
# Create your tests here.

class OrdersTestCase(APITestCase):

    def setUp(self):
        self.order_url = '/api/v1/orders/'
        self.customer_url = '/api/v1/customers/'
        self.menu_url = '/api/v1/menu/'


    def setCustomer(self):
        customer_data = {
            "full_name":"Richard Hendriks",
            "phone":"+447594392684",
            "address":"17 Canal St",
            "email":"test@test.net"
        }
        r = self.client.post(self.customer_url, data=customer_data, format='json')
        return r.json()

    def setMenu(self):
        sizes = [
                MenuItemSize.objects.create(name="Small", price=Decimal(0), slug="small"),
                MenuItemSize.objects.create(name="Medium", price=Decimal(2.99), slug="medium"),
                MenuItemSize.objects.create(name="Large", price=Decimal(4.99), slug="large"),
                MenuItemSize.objects.create(name="Extra Large", price=Decimal(6.99), slug="extralarge"),
                MenuItemSize.objects.create(name="Super Extra Large", price=Decimal(9.99), slug="superextralarge")
            ]

        pizza1 = MenuItem.objects.create(name="Pepperoni", description="Pepperoni pizza", price=Decimal(5))
        pizza2 = MenuItem.objects.create(name="Mozzarella", description="Cheese pizza", price=Decimal(4))

        for size in sizes:
            pizza1.size.add(size)
            pizza2.size.add(size)


    def setOrder(self):
        r_customer = self.client.get(self.customer_url)
        if r_customer.json()["count"] == 0:
            self.setCustomer()
        r_menu = self.client.get(self.menu_url)
        if r_menu.json()["count"] == 0:
            self.setMenu()
        r_customer = self.client.get(self.customer_url).json()
        r_menu = self.client.get(self.menu_url).json()


        order_data = {
                    "customer_id":r_customer["results"][0]["id"],
                    "items": [{
                            "id":r_menu["results"][0]["id"],
                            "quantity":2,
                            "size":"small"
                            }, {
                                "id":r_menu["results"][0]["id"],
                                "quantity":1,
                                "size":"large"
                            },
                            {
                                "id":r_menu["results"][1]["id"],
                                "quantity":3,
                                "size":"medium"
                            }
                        ]
                    }

        r = self.client.post(self.order_url, order_data, format='json')
        return r.json()



    def test_zero_orders(self):

        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_create_customer(self):
        self.setCustomer()
        #self.assertEqual(r.json()['full_name'], customer_data["full_name"])
        r2 = self.client.get(self.customer_url)
        self.assertEqual(r2.json()['results'][0]["full_name"], "Richard Hendriks")
        self.assertEqual(r2.json()['count'], 1)

    def test_menu(self):
        self.setMenu()
               
        r = self.client.get(self.menu_url)
        data = r.json()["results"]
        self.assertEqual(data[0]["name"], "Pepperoni")
        self.assertEqual(data[0]["description"], "Pepperoni pizza")
        self.assertEqual(data[0]["price"], "5.00")
        self.assertEqual(data[0]["available"], True)
        self.assertEqual(data[0]["size"][0]["name"], "Small")
        self.assertEqual(data[0]["size"][0]["price"], "0.00")

        self.assertEqual(data[1]["name"], "Mozzarella")
        self.assertEqual(data[1]["description"], "Cheese pizza")
        self.assertEqual(data[1]["price"], "4.00")
        self.assertEqual(data[1]["available"], True)
        self.assertEqual(data[1]["size"][1]["name"], "Medium")
        self.assertEqual(data[1]["size"][1]["price"], "2.99")

    def test_add_order(self):
        data = self.setOrder()
        
        self.assertEqual(data["customer"]["full_name"], "Richard Hendriks")
        self.assertEqual(data["status"], "draft")
        self.assertEqual(data["items"][0]["item"]["name"], "Pepperoni")
        self.assertEqual(data["items"][1]["item"]["name"], "Pepperoni")
        self.assertEqual(data["items"][2]["item"]["name"], "Mozzarella")
        # $5 + small (0) * 2 qty = 10
        self.assertEqual(data["items"][0]["total"], 10.0)
        # $5 + large $4.99 * 1 qty = 9.99
        self.assertEqual(data["items"][1]["total"], 9.99)
        # $4 + medium $2.99 * 3 qty = 20.97
        self.assertEqual(data["items"][2]["total"], 20.97)

    def test_edit_items_allowed(self):
        order = self.setOrder()
        r_menu = self.client.get(self.menu_url).json()
        
        new_order_url = self.order_url + "{}/".format(order["id"])
        new_items = {
            "items":[{
                "id":r_menu["results"][0]["id"],
                "quantity":10,
                "size":"superextralarge"
            }]
        }

        r2 = self.client.put(new_order_url, data=new_items, format='json').json()

        self.assertEqual(r2["items"][0]["item"]["id"], r_menu["results"][0]["id"])
        self.assertEqual(r2["items"][0]["quantity"], 10)
        self.assertEqual(r2["items"][0]["size"], "Super Extra Large")
        # (5 + super extra large 9.99) * 10 = 149.9
        self.assertEqual(r2["items"][0]["total"], 149.9)

    def test_set_status(self):
        order = self.setOrder()
        new_order_url = self.order_url + "{}/set_status/".format(order["id"])
        
        status_data = {"status":"delivered"}
        r2 = self.client.post(new_order_url, status_data, format='json')
        self.assertEqual(r2.status_code, 201)

    def test_edit_while_not_allowed(self):
        order = self.setOrder()
        status_url = self.order_url + "{}/set_status/".format(order["id"])
        new_order_url = self.order_url + "{}/".format(order["id"])
        
        r_menu = self.client.get(self.menu_url).json()
        status_data = {"status":"delivered"}
        r_status = self.client.post(status_url, data=status_data, format='json')
        self.assertEqual(r_status.status_code, 201)
        new_items = {
            "items":[{
                "id":r_menu["results"][0]["id"],
                "quantity":10,
                "size":"superextralarge"
            }]
        }

        r = self.client.put(new_order_url, new_items, format='json').json()
        self.assertEqual(r, ["Order is already past prep, items can't be edited"])

        