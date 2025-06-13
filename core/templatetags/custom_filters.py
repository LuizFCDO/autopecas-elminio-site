from django import template

register = template.Library()

@register.filter
def divided_by(value, arg):
    """Divide o valor pelo argumento."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return value
    
@register.filter
def multiply(value, arg):
    """Multiplica o valor pelo argumento."""
    try:
        return float(value) * float(arg)
    except ValueError:
        return value