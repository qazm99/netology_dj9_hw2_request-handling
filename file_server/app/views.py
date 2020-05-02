from datetime import datetime
from django.shortcuts import render
from app.settings import FILES_PATH
from os import listdir, stat


def file_list(request, date=None):
    set_date = datetime.strptime(date, '%Y-%m-%d') if date else None
    # if date:
    #     set_date = datetime.strptime(date, '%Y-%m-%d')
    # else:
    #     set_date = None
    template_name = 'index.html'
    files = []
    for file in listdir(FILES_PATH):
        ctime = datetime.fromtimestamp(stat(f'{FILES_PATH}\\{file}').st_ctime)
        mtime = datetime.fromtimestamp(stat(f'{FILES_PATH}\\{file}').st_mtime)
        if not date or str(ctime.date()) == date or str(mtime.date()) == date:
            files.append(dict(name=file, ctime=ctime, mtime=mtime))

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    context = {
        'files': files,
        'date': set_date  # Этот параметр необязательный
    }
    return render(request, template_name, context)


def file_content(request, name):
    with open(f'{FILES_PATH}\\{name}', encoding='utf-8') as file:
        str_content = file.read()
        #str_content = '<br> '.join(file)
        print(str_content)

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    return render(
        request,
        'file_content.html',
        context={'file_name': f'{name}', 'file_content': str_content}
    )

