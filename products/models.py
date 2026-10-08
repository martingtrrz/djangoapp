from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=225, verbose_name='Nombre')
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=225, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='get_products', 
                                 verbose_name='Categoría', null=True, blank=True)
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']
        
    def __str__(self):
        return self.name

    # ── Patron Creacional: Factory Method ────────────────────────────────────
    @classmethod
    def crear_con_categoria_default(cls, name, description, price):
        """Crea un producto asignando 'Sin categoría' si no se especifica una."""
        categoria_default, _ = Category.objects.get_or_create(name='Sin categoría')
        return cls.objects.create(
            name=name,
            description=description,
            price=price,
            category=categoria_default
        )
