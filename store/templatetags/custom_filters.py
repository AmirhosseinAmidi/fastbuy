from django import template
import persian

register = template.Library()

@register.filter
def persian_price(value):
    try:
        value = int(value)
        formatted = "{:,}".format(value)
        return persian.convert_en_numbers(formatted)
    except Exception:
        return value

@register.filter
def modulo(value, arg):
    return value % arg

@register.filter
def persian_numbers(value):
    english_nums = '0123456789'
    persian_nums = '۰۱۲۳۴۵۶۷۸۹'
    for en, fa in zip(english_nums, persian_nums):
        value = str(value).replace(en, fa)
    return value
