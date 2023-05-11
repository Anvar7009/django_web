from django.shortcuts import render, redirect
from . models import Category, Product, Cart
from . import models
from .forms import SearchForm
from telebot import TeleBot

bot = TeleBot('6142713646:AAHdeN08kBV2X57idrgHylkvXWTv6TUx46Q', parse_mode='HTML')



# Create your views here.
def index(request):
    # taking all category of products from db
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()
    search_bar = SearchForm()

    context = {'products': all_products,
               'all_categories': all_categories,
               'form': search_bar}

    search_bar = SearchForm()
    if request.method =='POST':
        product_find = request.POST.get('search_product')
        try:
            search_result = models.Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')
    return render(request, 'index.html', context)




    # making a dictionary for correct display in front end
    # context = {'all_categories': all_categories, 'product': all_products}
    # # return rendered version to front
    # return render(request, 'index.html', context)

"""def current_category(request,pk):
    products = models.Product.objects.get(id=pk)
    context = {
        'products' : products
    }

    return render(request, 'current_category.html', context)"""

# Получить определенный продукт
def get_exact_category(request, pk):
    # get single object from db by id
    exact_category = models.Category.objects.get(id=pk)
    #  using filter picking all product data by filter
    category_products = models.Product.objects.filter(product_category=exact_category)
    categories = models.Category.objects.all()

    return render(request, 'categrory_products.html', {'category_products': category_products,
                                                       'categories': categories})


#получить определенный продукт


# Получить определенный продукт
def get_exact_product(request, pk):
    product = models.Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        models.Cart.objects.create(user_id=request.user.id,
                    user_product=product,
                    user_product_quantity=request.POST.get('user_product_quantity'),
            total_for_product=product.product_price*int(request.POST.get('user_product_quantity')))
        return redirect('/cart')

    return render(request, 'about_product.html', context)

def get_user_cart(request):
    user_cart = models.Cart.objects.filter(user_id=request.user.id)
    total= sum([i.total_for_product for i in user_cart])

    context = {'cart': user_cart, 'total': total}

    return render(request, 'user_cart.html',context)


#оформления заказа
def complete_order(request):
    #получаем корзину пользователя
    user_cart= models.Cart.objects.filter(user_id=request.user.id)

    #Формируем сообшения для тг админа
    result_massage = 'Новый заказ(Сайт)\n\n'
    total_for_all_cart = 0
    for cart in user_cart:
        result_massage += f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} sum\n'

        total_for_all_cart += cart.total_for_product

    result_massage += f'\n----------\n<b>Итого: {total_for_all_cart} sum</b>'


    #отправляем админу сообшения в тг
    bot.send_message(2183610, result_massage)


    return redirect('/')




""" #Получим значение введенное в поисковой строке сайта
    from_frontend = request.GET.get('exact_product')

    #было ли введено что то в поиске
    if from_frontend is not None:
        all_products = models.Product.objects.filter(product_name__contains=from_frontend)
        print(all_products)"""