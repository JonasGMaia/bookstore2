

from django.test import TestCase
from django.contrib.auth.models import User

from order.models import Order
from order.serializers import OrderSerializer
from order.factories import OrderFactory, UserFactory
from product.models import Product
from product.factories import ProductFactory, CategoryFactory


class OrderModelTest(TestCase):

    def test_create_order(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        product = Product.objects.create(title="Book", price=10)
        order.product.add(product)
        self.assertEqual(order.user, user)
        self.assertEqual(order.product.count(), 1)

    def test_order_cascade_deletes_with_user(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        order_id = order.pk
        user.delete()
        self.assertFalse(Order.objects.filter(pk=order_id).exists())

    def test_order_multiple_products(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        p1 = Product.objects.create(title="Book A", price=10)
        p2 = Product.objects.create(title="Book B", price=20)
        order.product.add(p1, p2)
        self.assertEqual(order.product.count(), 2)

    def test_deleting_order_does_not_delete_products(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        product = Product.objects.create(title="Book", price=10)
        order.product.add(product)
        order.delete()
        self.assertTrue(Product.objects.filter(pk=product.pk).exists())


class OrderSerializerTest(TestCase):

    def test_serializes_order_with_products(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        p1 = Product.objects.create(title="Book A", price=10)
        p2 = Product.objects.create(title="Book B", price=20)
        order.product.add(p1, p2)
        serializer = OrderSerializer(order)
        self.assertEqual(len(serializer.data["product"]), 2)
        self.assertEqual(serializer.data["total"], 30)

    def test_total_with_single_product(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        order = Order.objects.create(user=user)
        product = Product.objects.create(title="Book", price=25)
        order.product.add(product)
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data["total"], 25)

    def test_serializer_fields(self):
        serializer = OrderSerializer()
        self.assertEqual(set(serializer.fields.keys()), {"product", "total"})


class UserFactoryTest(TestCase):

    def test_creates_valid_user(self):
        user = UserFactory()
        self.assertIsNotNone(user.pk)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)


class OrderFactoryTest(TestCase):

    def test_creates_valid_order(self):
        order = OrderFactory()
        self.assertIsNotNone(order.pk)
        self.assertIsNotNone(order.user)

    def test_creates_order_with_products(self):
        product = ProductFactory()
        order = OrderFactory(product=[product])
        self.assertIn(product, order.product.all())
