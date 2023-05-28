from django import template
register = template.Library()


def change_tags(teg):
    if teg == '\n':
        return '<br>'
