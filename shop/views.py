from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .forms import ContactMessageForm
from .models import Category, Product


def index(request):
    featured = Product.objects.available().featured().select_related("category")[:6]
    categories = (
        Category.objects.annotate(
            product_count=Count("products", filter=Q(products__is_available=True))
        )
        .order_by("-product_count", "name")
    )
    context = {
        "featured": featured,
        "categories": categories,
    }
    return render(request, "shop/index.html", context)


def menu(request):
    categories = Category.objects.all()
    products = Product.objects.available().select_related("category")

    active_slug = request.GET.get("kateqoriya")
    active_category = None
    if active_slug:
        active_category = get_object_or_404(Category, slug=active_slug)
        products = products.in_category(active_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.search(query)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "categories": categories,
        "products": page_obj,
        "page_obj": page_obj,
        "active_category": active_category,
        "query": query,
        "result_count": paginator.count,
    }
    return render(request, "shop/menu.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related = (
        Product.objects.available()
        .in_category(product.category)
        .exclude(pk=product.pk)
        .select_related("category")[:3]
    )
    context = {"product": product, "related": related}
    return render(request, "shop/product_detail.html", context)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    welcome_message = {
        "role": "agent",
        "text": "Salam! Sifarişiniz üçün nə lazımdır? Məhsul adını, miqdarını və çatdırılma tarixini yazın.",
    }
    conversation = request.session.setdefault("chat_conversation", [welcome_message])

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if form.is_valid():
            form.save()
            conversation.append({"role": "user", "text": form.cleaned_data["message"]})
            conversation.append(
                {
                    "role": "agent",
                    "text": "Mesajınız qeydə alındı. Sifarişinizlə bağlı ən qısa zamanda sizinlə əlaqə saxlayacağıq.",
                }
            )
            request.session["chat_conversation"] = conversation
            messages.success(request, "Mesajınız alındı. Tezliklə cavab verəcəyik.")
            if is_ajax:
                return JsonResponse({"success": True, "conversation": conversation})
            form = ContactMessageForm()
        elif is_ajax:
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data(escape_html=True)},
                status=400,
            )
    else:
        form = ContactMessageForm()

    context = {
        "form": form,
        "conversation": conversation,
    }
    return render(request, "shop/contact.html", context)
