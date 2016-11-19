from django import template

register = template.Library()

@register.simple_tag
def collection_field_value(row, field):
    if field in row:
        return row[field]


@register.inclusion_tag(
    "django_pymongo_admin/includes/pagination.html", takes_context=True)
def pymongo_pagination(context):
    page = context['page']
    total_count = context['total_count']

    return {
        "page": page,
        "total_count": total_count,
        "r5": range(-2, 3),
    }

@register.filter
def sub(n, x):
    return n-x

@register.simple_tag(takes_context=True)
def get_param_value(context, field):
    if field in context:
        return context[field]
    else:
        return ''