from django.http import HttpResponse

from django.shortcuts import render
import xlrd
import xlwt
from xlutils.copy import copy
from .forms import NumberCatalogInput
from .models import Product


# Create your views here.


def hat(name):
    book = xlwt.Workbook('utf8')
    # Добовляем лист
    sheet = book.add_sheet('Лист 1')
    alignment = xlwt.Alignment()
    alignment.wrap = 1
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER,
    # HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM,
    # VERT_JUSTIFIED, VERT_DISTRIBUTED
    # Устанавливаем шрифт
    font = xlwt.Font()
    font.name = 'Arial Cyr'
    font.bold = True
    # Устанавливаем границы
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    # Создаем стиль с нашими установками

    style = xlwt.XFStyle()
    style.font = font
    style.alignment = alignment
    style.borders = borders

    # Заполняем ячейку (Строка, Колонка, Текст, Шрифт)

    sheet.write(0, 0, 'Каталожный номер', style)
    sheet.write(0, 1, 'Бренд', style)
    sheet.write(0, 2, 'Название Детали', style)
    sheet.write(0, 3, 'Цена товара', style)
    sheet.write(0, 4, 'Время доставки', style)
    sheet.row(0).height = 800
    sheet.col(0).width = 5000
    sheet.col(1).width = 3000
    sheet.col(2).width = 5000
    sheet.col(3).width = 3500
    sheet.col(4).width = 3500
    sheet.portrait = False
    sheet.set_print_scaling(85)

    book.save('/home/berluskuni/web_project/alex_script/files/{}.xls'.format(name))


def index(request):
    if request.method == 'POST':
        form = NumberCatalogInput(request.POST)
        if form.is_valid():
            catalog = form.cleaned_data['catalog_number'].rsplit(',')
            catalog_number = []
            for item in catalog:
                catalog_number.append(item.strip())
            hat(catalog_number[0])
            count = 1
            for item in catalog_number:
                try:
                    qs = Product.objects.filter(number_catalog=item).values()
                    # Открываем эксельник, в который будет производиться записб, делаем его копию для редактирования
                    readbook = xlrd.open_workbook(r'/home/berluskuni/web_project/alex_script/files/{}.xls'
                                              .format(catalog_number[0]), on_demand=True, formatting_info=True)
                    readsheet = readbook.sheet_by_index(0)  # Указание на индекс листа книги.
                    writebook = copy(readbook)
                    writesheet = writebook.get_sheet(0)  # Указание на индекс листа книги.
                    # Устанавливаем перенос по словам, выравнивание
                    alignment = xlwt.Alignment()
                    alignment.wrap = 1
                    alignment.horz = xlwt.Alignment.HORZ_CENTER
                    alignment.vert = xlwt.Alignment.VERT_CENTER
                    # Устанавливаем шрифт
                    font = xlwt.Font()
                    font.name = 'Arial Cyr'
                    font.bold = True
                    # Устанавливаем границы
                    borders = xlwt.Borders()
                    borders.left = xlwt.Borders.THIN
                    borders.right = xlwt.Borders.THIN
                    borders.top = xlwt.Borders.THIN
                    borders.bottom = xlwt.Borders.THIN
                    # Создаём стиль с нашими установками
                    pattern = xlwt.Pattern()
                    protection = xlwt.Protection()
                    style = xlwt.XFStyle
                    style.font = font
                    style.alignment = alignment
                    style.borders = borders
                    style.num_format_str = 'general'
                    style.pattern = pattern
                    style.protection = protection
                    # Задаём цикл поиска первой пустой строки и записи в неё нужных нам данных
                    writesheet.write(count, 0, qs[0]['number_catalog'], style)
                    writesheet.write(count, 1, qs[0]['brand'], style)
                    writesheet.write(count, 2, qs[0]['name_detail'], style)
                    writesheet.write(count, 3, qs[0]['price'], style)
                    writesheet.write(count, 4, qs[0]['time_shipping'], style)
                    readbook.release_resources()
                    writebook.save('/home/berluskuni/web_project/alex_script/files/{}.xls'.format(catalog_number[0]))
                    count += 1
                except:
                    continue
            file = '/{}.xls'.format(catalog_number[0])
            return render(request, 'index.html', {'catalog': catalog_number, 'file': file})
    return render(request, 'index.html', {})


def my_view(request, filename):
    f = open('/home/berluskuni/web_project/alex_script/files/{}.xls'.format(filename), 'rb')
    return HttpResponse(f, content_type='application/octet-stream')