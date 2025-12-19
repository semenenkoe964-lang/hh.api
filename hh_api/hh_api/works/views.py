"""Views-модули для сайта."""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Vacancies


ELEMENTS_ON_PAGES = 10


# Create your views here.
def index(request):
    """GET-запросы на получение списка ваканский."""
    # Номер странички передаем в виде комментария
    # Пагинатор хранит в vacancies информацию для
    # постраничного скролла
    page_number = request.GET.get("page", 1)

    # Получаем все вакансии
    vacancies = Vacancies.objects.select_related(
        "category", "city", "employer"
    )

    vacancies_count = vacancies.count()
    # Создаём пагинатор: 10 вакансий на страницу (константа)
    paginator = Paginator(vacancies, ELEMENTS_ON_PAGES)

    try:
        vacancies = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не целое число — первая страница
        vacancies = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше максимального — последняя страница
        vacancies = paginator.page(paginator.num_pages)

    return render(request, "works/index.html", {
        "vacancies": vacancies,
        "vacancies_count": vacancies_count
    })


def work_detail(request, pk):
    """GET-запросы для получения деталей о вакансии."""
    vacancies = Vacancies.objects.select_related(
        "category", "city", "employer"
    )
    vacancy = get_object_or_404(vacancies, pk=pk)
    return render(request, 'works/detail.html', {"vacancy": vacancy})


def search_work(request):
    """GET-запросы для поиска ваканский."""
    # Получаем условия запроса.
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "")

    vacancies = Vacancies.objects.select_related(
        "category", "city", "employer"
    )
    # Фильтрация по ключевому слову (в названии и, опционально, в описании)
    if query:
        vacancies = vacancies.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Сортировка
    if sort == "popularity":
        # Тут можно вставить фильтрацию по чему-то
        # Но я не стал пока что
        vacancies = vacancies.order_by("-id")  # условно
    elif sort == "newest":
        vacancies = vacancies.order_by("-id")
    elif sort == "salary_desc":
        vacancies = vacancies.order_by("-salary_lower", "-salary_upper")
    elif sort == "salary_asc":
        vacancies = vacancies.order_by("salary_lower", "salary_upper")

    vacancies_count = vacancies.count()
    # Пагинация — те же принципы
    paginator = Paginator(vacancies, ELEMENTS_ON_PAGES)
    page_number = request.GET.get("page")
    try:
        vacancies = paginator.page(page_number)
    except PageNotAnInteger:
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(paginator.num_pages)

    # Пагинатор сам хранит номера предыдущих и след. страничек
    # vacancies содержит необходимое
    return render(request, "works/search.html", {
        "vacancies": vacancies,
        "vacancies_count": vacancies_count,
        "query": query,
        "sort": sort,
    })
