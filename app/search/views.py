from django.shortcuts import render, get_list_or_404
from app.search.models import Sub
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render



CONTENTS_NUM = 10
def main(request):
    return render(request, "home.html", {"mode":"home"})

def search_list(request, emotion):
    results_list = get_list_or_404(Sub, emotion=emotion)
    total_len = len(results_list)

    paginator = Paginator(results_list, CONTENTS_NUM)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 integer아니면 첫번째 페이지
        results = paginator.page(1)
    except EmptyPage:
        # 페이지 범위 넘어가면 마지막 페이지
        results = paginator.page(paginator.num_pages)

    index = results.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    context = {'results':results, 'mode':emotion, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2}

    return render(request, 'result/search_list.html', context)
