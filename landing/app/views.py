from collections import Counter
import random
from django.shortcuts import render_to_response
from django.shortcuts import redirect

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    type_landing = request.GET.get('from-landing')
    if type_landing == 'original':
        counter_click['original'] += 1
        return render_to_response('index.html')
    elif type_landing == 'test':
        counter_click['test'] += 1
        return render_to_response('index.html')
    else:
        return redirect('landing')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    type_landing = request.GET.get('ab-test-arg', random.choice(('test', 'original')))
    if type_landing == 'original':
        counter_show['original'] += 1
        #counter_show.update({'original': 1})
        return render_to_response('landing.html')
    elif type_landing == 'test':
        counter_show['test'] += 1
        #counter_show.update({'test': 1})
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    if counter_click.get('test') and counter_show.get('test'):
        test_conversion = counter_click.get('test')/counter_show.get('test')
    else:
        test_conversion = 0
    if counter_click.get('original') and counter_show.get('original'):
        original_conversion = counter_click.get('original')/counter_show.get('original')
    else:
        original_conversion = 0
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
