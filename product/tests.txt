from django.test import TestCase
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from product.factories import ProductFactory, CategoryFactory


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(
            title="Fiction",
            slug="fiction",
            description="Fiction books",
            active=True,
        )
        self.assertEqual(category.title, "Fiction")
        self.assertEqual(category.slug, "fiction")
        self.assertEqual(category.description, "Fiction books")
        self.assertTrue(category.active)

    def test_category_active_default_is_true(self):
        category = Category.objects.create(title="Sci-Fi", slug="sci-fi")
        self.assertTrue(category.active)

    def test_category_slug_is_unique(self):
        Category.objects.create(title="Fiction", slug="fiction")
        with self.assertRaises(Exception):
            Category.objects.create(title="Fiction 2", slug="fiction")

    def test_category_description_is_optional(self):
        category = Category.objects.create(title="History", slug="history")
        self.assertIsNone(category.description)


class ProductModelTest(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            title="The Great Gatsby",
            description="A classic novel",
            price=15,
            active=True,
        )
        self.assertEqual(product.title, "The Great Gatsby")
        self.assertEqual(product.description, "A classic novel")
        self.assertEqual(product.price, 15)
        self.assertTrue(product.active)

    def test_product_active_default_is_true(self):
        product = Product.objects.create(title="Some Book")
        self.assertTrue(product.active)

    def test_product_description_is_optional(self):
        product = Product.objects.create(title="No Desc Book")
        self.assertIsNone(product.description)

    def test_product_price_is_optional(self):
        product = Product.objects.create(title="Free Book")
        self.assertIsNone(product.price)

    def test_product_category_many_to_many(self):
        cat1 = Category.objects.create(title="Fiction", slug="fiction")
        cat2 = Category.objects.create(title="Classic", slug="classic")
        product = Product.objects.create(title="Gatsby", price=10)
        product.category.add(cat1, cat2)
        self.assertEqual(product.category.count(), 2)
        self.assertIn(cat1, product.category.all())
        self.assertIn(cat2, product.category.all())

    def test_product_category_blank_allowed(self):
        product = Product.objects.create(title="No Category Book")
        self.assertEqual(product.category.count(), 0)


class CategorySerializerTest(TestCase):

    def test_serializes_all_fields(self):
        category = Category.objects.create(
            title="Fiction", slug="fiction", description="Fiction books", active=True
        )
        serializer = CategorySerializer(category)
        self.assertEqual(serializer.data["title"], "Fiction")
        self.assertEqual(serializer.data["slug"], "fiction")
        self.assertEqual(serializer.data["description"], "Fiction books")
        self.assertTrue(serializer.data["active"])

    def test_serializer_fields(self):
        serializer = CategorySerializer()
        self.assertEqual(
            set(serializer.fields.keys()),
            {"title", "slug", "description", "active"},
        )


class ProductSerializerTest(TestCase):

    def test_serializes_product_with_categories(self):
        category = Category.objects.create(
            title="Fiction", slug="fiction", description="Fiction books", active=True
        )
        product = Product.objects.create(title="Gatsby", description="A novel", price=15)
        product.category.add(category)
        serializer = ProductSerializer(product)
        self.assertEqual(serializer.data["title"], "Gatsby")
        self.assertEqual(serializer.data["price"], 15)
        self.assertEqual(len(serializer.data["category"]), 1)
        self.assertEqual(serializer.data["category"][0]["title"], "Fiction")

    def test_serializer_fields(self):
        serializer = ProductSerializer()
        self.assertEqual(
            set(serializer.fields.keys()),
            {"title", "description", "price", "active", "category"},
        )


class CategoryFactoryTest(TestCase):

    def test_creates_valid_category(self):
        category = CategoryFactory()
        self.assertIsNotNone(category.pk)
        self.assertIsNotNone(category.title)
        self.assertIsNotNone(category.slug)


class ProductFactoryTest(TestCase):

    def test_creates_valid_product(self):
        product = ProductFactory()
        self.assertIsNotNone(product.pk)
        self.assertIsNotNone(product.title)
        self.assertIsNotNone(product.price)

    def test_creates_product_with_categories(self):
        cat = CategoryFactory()
        product = ProductFactory(category=[cat])
        self.assertIn(cat, product.category.all())