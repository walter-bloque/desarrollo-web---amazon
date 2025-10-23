from django.core.management.base import BaseCommand
from shop.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Carga datos de prueba de categorías y productos'

    def handle(self, *args, **kwargs):
        # Borrar datos existentes (opcional)
        self.stdout.write('Eliminando datos existentes...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Crear categorías
        self.stdout.write('Creando categorías...')
        categories_data = [
            {'name': 'Electrónica', 'slug': 'electronica'},
            {'name': 'Computadoras', 'slug': 'computadoras'},
            {'name': 'Videojuegos', 'slug': 'videojuegos'},
            {'name': 'Hogar y Cocina', 'slug': 'hogar-cocina'},
            {'name': 'Deportes', 'slug': 'deportes'},
            {'name': 'Libros', 'slug': 'libros'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(f'[OK] Categoría creada: {category.name}')

        # Crear productos
        self.stdout.write('\nCreando productos...')
        products_data = [
            # Electrónica
            {
                'category': categories[0],
                'name': 'Audífonos Inalámbricos Sony WH-1000XM5',
                'slug': 'audifonos-sony-wh1000xm5',
                'description': 'Audífonos premium con cancelación de ruido líder en la industria.',
                'price': 349.99,
                'original_price': 399.99,
                'discount_percentage': 12,
                'stock': 45,
                'rating': 4.7,
                'reviews_count': 2847,
                'is_prime': True,
            },
            {
                'category': categories[0],
                'name': 'Smart TV Samsung 55" 4K QLED',
                'slug': 'smart-tv-samsung-55-qled',
                'description': 'Televisor inteligente con tecnología Quantum Dot y HDR10+.',
                'price': 799.99,
                'original_price': 999.99,
                'discount_percentage': 20,
                'stock': 15,
                'rating': 4.6,
                'reviews_count': 1523,
                'is_prime': True,
            },
            {
                'category': categories[0],
                'name': 'Cámara Digital Canon EOS R6',
                'slug': 'camara-canon-eos-r6',
                'description': 'Cámara mirrorless profesional de fotograma completo.',
                'price': 2499.99,
                'stock': 8,
                'rating': 4.9,
                'reviews_count': 456,
                'is_prime': False,
            },
            
            # Computadoras
            {
                'category': categories[1],
                'name': 'Laptop Dell XPS 13 - Intel i7, 16GB RAM',
                'slug': 'laptop-dell-xps-13',
                'description': 'Portátil ultradelgada con procesador de última generación.',
                'price': 1299.99,
                'original_price': 1499.99,
                'discount_percentage': 13,
                'stock': 22,
                'rating': 4.5,
                'reviews_count': 987,
                'is_prime': True,
            },
            {
                'category': categories[1],
                'name': 'Mouse Logitech MX Master 3S',
                'slug': 'mouse-logitech-mx-master-3s',
                'description': 'Mouse ergonómico inalámbrico de alta precisión.',
                'price': 99.99,
                'original_price': 129.99,
                'discount_percentage': 23,
                'stock': 156,
                'rating': 4.8,
                'reviews_count': 5632,
                'is_prime': True,
            },
            {
                'category': categories[1],
                'name': 'Teclado Mecánico Corsair K70 RGB',
                'slug': 'teclado-corsair-k70',
                'description': 'Teclado gaming con switches Cherry MX e iluminación RGB.',
                'price': 159.99,
                'stock': 67,
                'rating': 4.6,
                'reviews_count': 2341,
                'is_prime': True,
            },
            
            # Videojuegos
            {
                'category': categories[2],
                'name': 'PlayStation 5 Console',
                'slug': 'playstation-5-console',
                'description': 'Consola de videojuegos de última generación con gráficos 4K.',
                'price': 499.99,
                'stock': 5,
                'rating': 4.9,
                'reviews_count': 15234,
                'is_prime': False,
            },
            {
                'category': categories[2],
                'name': 'The Legend of Zelda: Tears of the Kingdom',
                'slug': 'zelda-tears-kingdom',
                'description': 'Aventura épica en el mundo de Hyrule.',
                'price': 59.99,
                'original_price': 69.99,
                'discount_percentage': 14,
                'stock': 89,
                'rating': 5.0,
                'reviews_count': 8923,
                'is_prime': True,
            },
            {
                'category': categories[2],
                'name': 'Xbox Wireless Controller - Carbon Black',
                'slug': 'xbox-controller-carbon',
                'description': 'Control inalámbrico con agarre texturizado.',
                'price': 59.99,
                'stock': 145,
                'rating': 4.7,
                'reviews_count': 4567,
                'is_prime': True,
            },
            
            # Hogar y Cocina
            {
                'category': categories[3],
                'name': 'Robot Aspirador Roomba i7+',
                'slug': 'roomba-i7-plus',
                'description': 'Aspiradora inteligente con estación de autovaciado.',
                'price': 599.99,
                'original_price': 799.99,
                'discount_percentage': 25,
                'stock': 34,
                'rating': 4.5,
                'reviews_count': 3456,
                'is_prime': True,
            },
            {
                'category': categories[3],
                'name': 'Cafetera Nespresso Vertuo Plus',
                'slug': 'nespresso-vertuo-plus',
                'description': 'Máquina de café con tecnología de centrifugación.',
                'price': 179.99,
                'stock': 78,
                'rating': 4.4,
                'reviews_count': 2134,
                'is_prime': True,
            },
            {
                'category': categories[3],
                'name': 'Instant Pot Duo 7-en-1',
                'slug': 'instant-pot-duo-7',
                'description': 'Olla a presión eléctrica multifuncional.',
                'price': 89.99,
                'original_price': 119.99,
                'discount_percentage': 25,
                'stock': 123,
                'rating': 4.7,
                'reviews_count': 45678,
                'is_prime': True,
            },
            
            # Deportes
            {
                'category': categories[4],
                'name': 'Bicicleta de Montaña Trek Marlin 7',
                'slug': 'trek-marlin-7',
                'description': 'Bicicleta todo terreno con suspensión frontal.',
                'price': 849.99,
                'stock': 12,
                'rating': 4.6,
                'reviews_count': 567,
                'is_prime': False,
            },
            {
                'category': categories[4],
                'name': 'Reloj Deportivo Garmin Forerunner 245',
                'slug': 'garmin-forerunner-245',
                'description': 'Smartwatch GPS para running con métricas avanzadas.',
                'price': 299.99,
                'original_price': 349.99,
                'discount_percentage': 14,
                'stock': 45,
                'rating': 4.5,
                'reviews_count': 2345,
                'is_prime': True,
            },
            {
                'category': categories[4],
                'name': 'Set de Pesas Ajustables Bowflex',
                'slug': 'pesas-bowflex',
                'description': 'Mancuernas ajustables de 5 a 52.5 libras.',
                'price': 399.99,
                'stock': 28,
                'rating': 4.8,
                'reviews_count': 1234,
                'is_prime': True,
            },
            
            # Libros
            {
                'category': categories[5],
                'name': 'Cien Años de Soledad - Gabriel García Márquez',
                'slug': 'cien-anos-soledad',
                'description': 'Obra maestra de la literatura latinoamericana.',
                'price': 14.99,
                'stock': 234,
                'rating': 4.9,
                'reviews_count': 12345,
                'is_prime': True,
            },
            {
                'category': categories[5],
                'name': 'El Alquimista - Paulo Coelho',
                'slug': 'el-alquimista',
                'description': 'Novela sobre seguir tus sueños y encontrar tu destino.',
                'price': 12.99,
                'original_price': 16.99,
                'discount_percentage': 23,
                'stock': 345,
                'rating': 4.7,
                'reviews_count': 8765,
                'is_prime': True,
            },
            {
                'category': categories[5],
                'name': 'Sapiens: De animales a dioses - Yuval Noah Harari',
                'slug': 'sapiens-yuval-harari',
                'description': 'Una breve historia de la humanidad.',
                'price': 18.99,
                'stock': 167,
                'rating': 4.8,
                'reviews_count': 15678,
                'is_prime': True,
            },
        ]

        for product_data in products_data:
            product = Product.objects.create(**product_data)
            self.stdout.write(f'[OK] Producto creado: {product.name}')

        self.stdout.write(self.style.SUCCESS(f'\n¡Datos cargados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'Total de categorías: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total de productos: {Product.objects.count()}'))
