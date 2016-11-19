from django import template

register = template.Library()

@register.simple_tag
def collection_field_value(row, field):
    if field in row:
        return row[field]